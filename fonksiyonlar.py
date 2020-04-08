from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest,InviteToChannelRequest
from telethon.tl.types import InputPeerChannel, InputPeerUser
from telethon.tl.functions.contacts import AddContactRequest
import globals,time
from telethon import errors
import socks, random,asyncio
def getCode(hesap,client):
    if not client.is_user_authorized():
        client.send_code_request(hesap["phone"], force_sms=hesap["forcesms"])
        str = "[{}] SMS Şifrenizi girin :".format(hesap["phone"])
        client.sign_in(hesap["phone"], input(str))
        return client
    else:
        print("Hesap sessionu zaten mevcut. Şifre gerekmeyecek.")
        return client
def startAuth(hesap):
    if hesap["proxy"]["aktif"]:
        c = TelegramClient(hesap["phone"], hesap["api_id"], hesap["api_pass"], proxy=(socks.SOCKS5, hesap["proxy"]["proxyip"], hesap["proxy"]["proxyport"], True, hesap["proxy"]["proxyusername"],hesap["proxy"]["proxypassword"]))
        c.connect()
        return getCode(hesap,c)
    else:
        c = TelegramClient(hesap["phone"], hesap["api_id"], hesap["api_pass"])
        c.connect()
        return getCode(hesap, c)
async def startAuthLoop(hesap,l):
    if hesap["proxy"]["aktif"]:
        c = TelegramClient(hesap["phone"], hesap["api_id"], hesap["api_pass"], proxy=(socks.SOCKS5, hesap["proxy"]["proxyip"], hesap["proxy"]["proxyport"], True, hesap["proxy"]["proxyusername"],hesap["proxy"]["proxypassword"]),loop=l)
        await c.connect()
        return c
    else:
        c = TelegramClient(hesap["phone"], hesap["api_id"], hesap["api_pass"],loop=l)
        await c.connect()
        return c
def startHandler(ekl,ckl,c):
    cekilecek = c.get_entity(ckl)
    eklenecek = c.get_entity(ekl)
    c(JoinChannelRequest(cekilecek))
    time.sleep(5)
    c(JoinChannelRequest(eklenecek))
    cekilecek_uyeler = getUserList(c, cekilecek)
    e_cekilecek =getTargetGroupEntity(cekilecek.id,cekilecek.access_hash)
    e_eklenecek = getTargetGroupEntity(eklenecek.id,eklenecek.access_hash)
    random.shuffle(cekilecek_uyeler)
    random.shuffle(cekilecek_uyeler) #listeyi karıştırdım.
    return cekilecek_uyeler,e_cekilecek,e_eklenecek

async def getidhash(c,eklenecek):
    eklenecek = await c.get_entity(eklenecek)
    e_eklenecek = getTargetGroupEntity(eklenecek.id,eklenecek.access_hash)
    return e_eklenecek

def getUserList(c,grup):
    l = c.get_participants(grup, aggressive=True)
    a = getAddableUserlist(l)
    return a

def disconnect(clilist):
    for c in clilist:
        c.disconnect()

def getAddableUserlist(l):
    a = []
    for u in l:
        if u.bot == False and u.username != None:
            t = Uye(u.id, u.access_hash, u.username, u.first_name, u.last_name, u.bot,
                    u.mutual_contact)
            a.append(t)
    return a

def getTargetGroupEntity(id,hash):
    return InputPeerChannel(id,hash)

async def addUserToMutualContact(client,user,name,secname,phone,id,hash):
    try:
        if name == None:
            name = ""
        if secname == None:
            secname = ""
        await client(AddContactRequest(user,name,secname,"+145055554953"))
        return InputPeerUser(id,hash)
    except errors.FloodWaitError as e:
        print('Flood uyarısı alındı.', e.seconds, ' saniye bekleniyor')
        return FloodReturn(True,e.seconds)
    except Exception as e:
        print("Bilinmeyen hata")
        print(e)
        return None
async def addUsersToGroup(client,group,users):
    try:
        x = await client(InviteToChannelRequest(group,users))
        print("Eklenen kişi sayısı : {}".format(len(x.users) -1))
    except errors.FloodWaitError as e:
        print('Flood uyarısı verdi[addUsers.', e.seconds, ' saniye bekleniyor')
        time.sleep(e.seconds)
    except Exception as er:
        print("Error at addUsers")
        print(er)
async def ThreadHandler(c,eklenecek_entity,uyesayisi,hsp,loop,eklenecek):
    asyncio.set_event_loop(loop)
    i = 0
    print("Starting.")
    print(hsp["phone"])
    cl = await startAuthLoop(hsp,loop)
    ex = await getidhash(cl,eklenecek)
    if globals.Globals.getInstance().getLen() >= uyesayisi:
        uyelist = globals.Globals.getInstance().getNumUser(uyesayisi)
        entity_list = []
        for uye in uyelist:
            print("{} - i : {}".format(hsp["phone"],i))
            e = await addUserToMutualContact(cl,uye.Username,uye.Name,uye.SecName,uye.Phone,uye.ID,uye.AccessHash)
            if e != None and not isinstance(e,FloodReturn):
                entity_list.append(e)
                i +=1
            if isinstance(e,FloodReturn):
                print("{}Flood bekleniyor. {}".format(hsp["phone"],e.Time))
                time.sleep(e.Time)
            if i % 5 == 0 and i > 0:
                await addUsersToGroup(cl,ex,entity_list)
                entity_list.clear()
                i = 0
            time.sleep(2)
    else:
        print(globals.Globals.getInstance().getLen())
        print(uyesayisi)
        print("Üye sayısı yetersiz.")

def addAllToMutual(c):
    e_list = []
    for uye in globals.Globals.getInstance().getUyeListesi():
        e = addUserToMutualContact(c,uye.Username,uye.Name,uye.SecName,uye.Phone,uye.ID,uye.AccessHash)
        if isinstance(e,FloodReturn):
            time.sleep(e.Time)
        if e != None:
            e_list.append(e)
    return e_list
class Uye:
    def __init__(self,_id,_hash,username,name,secname,isBot,isMutual):
        self.ID = _id
        self.AccessHash = _hash
        self.Username = username
        self.Name = name
        self.SecName = secname
        self.Phone = "" #mutual contact sonrası eklenmeli
        self.isBot = isBot
        self.isMutual = isMutual

class FloodReturn:
    def __init__(self,isflood,time):
        self.IsFlood=isflood
        self.Time = time

class HesapUyeList:
    def __init__(self,list,hesap):
        self.List = list
        self.Hesap = hesap
        self.Client = None
    def setClient(self,c):
        self.Client = c
