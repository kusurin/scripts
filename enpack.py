import os
import shutil
import re

antRE = '^.+?(?=[_])' #public ante title of files
formRE = '.png$' #file type
renameRE = '[^_]+$' #new name of files

class filepack(object):
    def __init__(self,__name):
        self.__name = __name
        self.__arr = [str]
        self.__arr.clear()

    def getname(self):
        return self.__name
    
    def getfiles(self):
        return self.__arr
    
    def apendfile(self,filename):
        self.__arr.append(filename)
    
class filepacks(object):
    def __init__(self):
        self.__packs = [filepack]
        self.__packs.clear()

    def empty(self):
        if(len(self.__packs)==0):
            return True
        return False
    
    def getLen(self):
        return len(self.__packs)
    
    def listPackByNumber(self,number:int) -> list[str]:
        if(number>=self.getLen()):
            return None
        return self.__packs[number].getfiles()
    
    def getPackNameByNumber(self,number:int) -> str:
        if(number>=self.getLen()):
            return False
        return self.__packs[number].getname()
    
    #def findPackByName(self,name:str):
    #    for pack in self.__packs:
    #        if(name == pack.getname()):
    #            return True
    #    return False
    
    def listPackByName(self,name:str):
        for pack in self.__packs:
            if(name == pack.getname()):
                return pack.getfiles()
        return False
    
    def apendPack(self,pack:filepack):
        self.__packs.append(pack)
        return True
    
    def apendFile(self,filename:str,anteRE:str):
        for pack in self.__packs:
            if(re.search(anteRE,filename).group()==pack.getname()):
                pack.apendfile(filename)
                return True
        pack_infun = filepack(re.search(anteRE,filename).group())
        pack_infun.apendfile(filename)
        self.apendPack(pack_infun)
        del pack_infun
        return False
            

files = os.listdir('./')

for file in files[:]:
    if re.search(antRE,file) == None or re.search(formRE,file) == None :
        files.remove(file)
        print('rm',file)

packs = filepacks()


for file in files:
    packs.apendFile(file,antRE)

for i in range(0,packs.getLen()):
    print('dir',packs.getPackNameByNumber(i))
    if not os.path.exists('./'+packs.getPackNameByNumber(i)):
        print('mkdir',packs.getPackNameByNumber(i))
        os.mkdir('./'+packs.getPackNameByNumber(i))
    for file in packs.listPackByNumber(i):
        print('mv',file)
        shutil.move('./'+file,'./'+packs.getPackNameByNumber(i)+'/'+re.search(renameRE,file).group())