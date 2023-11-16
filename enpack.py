# 导入os, shutil, re模块，分别用于操作系统，文件复制和移动，正则表达式
import os
import shutil
import re

# 定义antRE, formRE, renameRE三个正则表达式，分别用于匹配文件的前缀名，后缀名，和去掉下划线后的部分
antRE = '^.+?(?=[_])' #public ante title of files
formRE = '.png$' #file type
renameRE = '[^_]+$' #new name of files

# 定义一个filepack类，用于封装文件的信息和操作
class filepack(object):
    # 初始化方法，接受一个文件名作为参数，用antRE匹配文件的前缀名，并创建一个空的文件列表
    def __init__(self,__name):
        self.__name = __name
        self.__arr = [str]
        self.__arr.clear()

    # 获取文件的前缀名
    def getname(self):
        return self.__name
    
    # 获取文件的列表
    def getfiles(self):
        return self.__arr
    
    # 向文件列表中添加一个文件名
    def apendfile(self,filename):
        self.__arr.append(filename)
    
# 定义一个filepacks类，用于存储不同的filepack对象
class filepacks(object):
    # 初始化方法，创建一个空的filepack列表
    def __init__(self):
        self.__packs = [filepack]
        self.__packs.clear()

    # 判断filepack列表是否为空
    def empty(self):
        if(len(self.__packs)==0):
            return True
        return False
    
    # 获取filepack列表的长度
    def getLen(self):
        return len(self.__packs)
    
    # 根据索引返回一个filepack的文件列表，如果索引超出范围，返回None
    def listPackByNumber(self,number:int) -> list[str]:
        if(number>=self.getLen()):
            return None
        return self.__packs[number].getfiles()
    
    # 根据索引返回一个filepack的前缀名，如果索引超出范围，返回False
    def getPackNameByNumber(self,number:int) -> str:
        if(number>=self.getLen()):
            return False
        return self.__packs[number].getname()
    
    #def findPackByName(self,name:str):
    #    for pack in self.__packs:
    #        if(name == pack.getname()):
    #            return True
    #    return False
    
    # 根据前缀名返回一个filepack的文件列表，如果没有找到对应的filepack，返回False
    def listPackByName(self,name:str):
        for pack in self.__packs:
            if(name == pack.getname()):
                return pack.getfiles()
        return False
    
    # 向filepack列表中添加一个filepack对象，返回True
    def apendPack(self,pack:filepack):
        self.__packs.append(pack)
        return True
    
    # 向filepack列表中添加一个文件名，如果已经存在相同前缀名的filepack，则添加到该filepack的文件列表中，否则创建一个新的filepack并添加到filepack列表中，返回False
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
            

# 获取当前目录下的所有文件名，赋值给files变量
files = os.listdir('./')

# 使用列表推导式来过滤files列表中不符合antRE或formRE的文件名，只保留以.png结尾且有下划线的文件名
files = [file for file in files if re.search(antRE,file) and re.search(formRE,file)]

# 创建一个filepacks对象，用于存储不同的filepack对象，每个filepack对象封装了同一个前缀名的文件列表
packs = filepacks()

# 遍历files列表中的每个文件名，调用filepacks对象的apendFile方法，将文件名添加到相应的filepack对象中，如果不存在相同前缀名的filepack对象，就创建一个新的filepack对象并添加到filepacks对象中
for file in files:
    packs.apendFile(file,antRE)

# 遍历filepacks对象中的每个filepack对象，打印出dir和前缀名，表示创建一个子目录，如果子目录不存在，就用os模块的mkdir方法创建一个子目录，然后遍历filepack对象中的每个文件名，打印出mv和文件名，表示移动该文件，用shutil模块的move方法将文件移动到子目录中，并用re模块的search方法和renameRE的正则表达式去掉文件名中的下划线前的部分
for i in range(0,packs.getLen()):
    print('dir',packs.getPackNameByNumber(i))
    if not os.path.exists('./'+packs.getPackNameByNumber(i)):
        print('mkdir',packs.getPackNameByNumber(i))
        os.mkdir('./'+packs.getPackNameByNumber(i))
    for file in packs.listPackByNumber(i):
        print('mv',file)
        shutil.move('./'+file,'./'+packs.getPackNameByNumber(i)+'/'+re.search(renameRE,file).group())