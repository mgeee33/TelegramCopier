import json
import fonksiyonlar,globals
import threading
from telethon.sync import TelegramClient
import asyncio,socks
eklenecekgrup = None
cekilecekgrup = None
hesap_listesi = []
client_list =[]
loop_list = []
with open("hesaplar.json") as hesaplar:
    data = json.load(hesaplar)
    for h in data["hesaplar"]:
        hesap_listesi.append(h)
print("Hesaplar yüklendi. Hesaplara giriş için sms gönderilecek.")
for hesap in hesap_listesi:
    client = fonksiyonlar.startAuth(hesap)
    client_list.append(client)

with open("ayarlar.json") as ayar:
    d = json.load(ayar)
    eklenecekgrup = d["uyelerin_eklenecegi_grup"]
    cekilecekgrup = d["uyelerin_cekilecegi_grup"]


uyelist,cek,ekle = fonksiyonlar.startHandler(eklenecekgrup,cekilecekgrup,client_list[0])
globals.Globals(uyelist)
fonksiyonlar.disconnect(client_list)
# globals.Globals.getInstance().getUye().Username
hesap_sayisi = len(hesap_listesi)
hesap_basi_uye = (globals.Globals.getInstance().getLen() // hesap_sayisi)
i = 0
loop = asyncio.new_event_loop()
for h in hesap_listesi:
    loop.create_task(fonksiyonlar.ThreadHandler(client_list[i],ekle,hesap_basi_uye,h,loop,eklenecekgrup))
    print(i)
    #t = threading.Thread(target=fonksiyonlar.ThreadHandler,args=(client_list[i],ekle,hesap_basi_uye,h,loop,))
    i +=1
    #t.start()
loop.run_forever()



