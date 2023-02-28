# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 12:20
# @Author  : huangyl
# @FileName: readConfig.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


import os
import codecs
import configparser

configPath = './config.ini'


class ReadConfig:
    def __init__(self):
        fd = open(configPath,"rb")
        #fd = open(configPath)
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath,encoding='UTF-8-sig')

    def get_url(self, name):
        value = self.cf.get("serverurl", name)
        return value

    def get_header(self, name):
        value = self.cf.get("header", name)
        return value

    def get_email(self,name):
        value = self.cf.get("email",name)
        return value

    def get_sql(self,name):
        value = self.cf.get("sqlserver",name)
        return value

    def get_path(self, name):
        value = self.cf.get("path", name)
        return value

    def get_sleep_time(self, name):
        value = self.cf.get("time", name)
        return value

    def get_task_name(self, name):
        value = self.cf.get("task_name", name)
        return value

    def get_errorRate(self, name):
        value = self.cf.get("errorRate", name)
        return value

    def get_test_type(self, name):
        value = self.cf.get("test_type", name)
        return value

    def get_all(self,*args):
        #secs = self.cf.sections()
        confs = {}
        for sec in args:
            options = self.cf.options(sec)
            for i in options:
                confs[i] = self.cf.get(sec,i)
        return confs
