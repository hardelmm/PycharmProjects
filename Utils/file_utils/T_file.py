# -*- coding: utf-8 -*-
# @Time    : 2023/2/17 12:52
# @Author  : huangyl
# @FileName: T_file.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


import codecs
import configparser
configPath = ''

class ReadConfig:
    def __int__(self):
        fd = open(configPath,"rb")
        data = fd.read()

        #remove BOM

        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath,"w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath,encoding='UTF-8-sig')

    def get_configOne(self,name):
        value = self.cf.get("configOne",name)
        return value

    #......

    def get_all(self,*args):
        confs = {}
        for sec in args:
            options = self.cf.options(sec)
            for i in options:
                confs[i] = self.cf.get(sec,i)
        return  confs

