class Globals:
    __instance = None
    @staticmethod
    def getInstance():
        if Globals.__instance == None:
            Globals()
        return Globals.__instance
    def __init__(self,l):
        if Globals.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Globals.__instance = self
            self.UyeListesi = l
    def setObject(self,Key,Object):
        if(isinstance(Key,str)):
            self.Database[Key] = Object
        else:
            raise Exception("Key parameter should be an instance of String at setObject function.")
    def getObject(self,Key):
        if(isinstance(Key,str)):
            return self.Database[Key]
        else:
            raise Exception("Key parameter should be an instance of String at setObject function.")
            return False
    def getUyeListesi(self):
        return self.UyeListesi
    def getUye(self):
        return self.UyeListesi.pop(0)
    def getLen(self):
        return len(self.UyeListesi)
    def getNumUser(self,num):
        eksi = -1 * num
        list = self.UyeListesi[eksi:]
        del self.UyeListesi[eksi:]
        return list
