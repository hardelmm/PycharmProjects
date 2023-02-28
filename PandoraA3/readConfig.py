# -*- coding: utf-8 -*-
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
        value = self.cf.get("HTTP", name)
        return value

    def get_header(self, name):
        value = self.cf.get("header", name)
        return value

    def get_tts_param(self, name):
        value = self.cf.get("tts_param", name)
        return value


    def get_case_path(self, name):
        value = self.cf.get("case_path", name)
        return value

    def get_result_path(self, name):
        value = self.cf.get("result_path", name)
        return value

    def get_sleep_time(self, name):
        value = self.cf.get("time", name)
        return value

    def get_thread_config(self, name):
        value = self.cf.get("thread_config", name)
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