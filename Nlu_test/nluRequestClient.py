# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 10:33
# @Author  : huangyl
# @FileName: nluRequestClient.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


from tools.log4j import *
from readConfig import ReadConfig
import requests
import hashlib
class NluRequestClient:
    def __init__(self):
        localReadConfig = ReadConfig()
        self.url = localReadConfig.get_url('url')
        self.appkey = localReadConfig.get_header('appkey')
        self.udid = localReadConfig.get_header('udid')
        self.ver = localReadConfig.get_header('ver')
        self.method = localReadConfig.get_header('method')
        #self.appsig = localReadConfig.get_header('appsig')
        self.case_path = localReadConfig.get_path('case_path')
        self.result_path = localReadConfig.get_path('result_path')
        self.confs = localReadConfig.get_all("header")

    def _getsignature(self, params_dict):
        secret = ''
        for k in params_dict.keys():
            if k.lower() == 'secret':
                secret = params_dict[k]
        point_keys = []
        for key in params_dict.keys():
            if key.lower() in params_dict.items():
                point_keys.append(key)
        sorted_point_keys = sorted(point_keys)
        s = secret + '&'
        for i in sorted_point_keys:
            try:
                s += "%s=%s" % (i, params_dict[i])
                s += '&'
            except Exception as e:
                print(e)
        s += secret
        signature = hashlib.sha1(s.encode('utf-8')).hexdigest().upper().strip()
        return signature

    def _generateUrl(self,text):
        # url = appkey=nmugoqugf3ikbhkhbaixhefxdinqcmgyhobsvjiv&city=&ver=3.2&udid=JUnit-test-All.txt-15&text=%E6%89%93%E5%BC%80%E4%B8%BB%E5%8D%AB%E7%81%AF&appver=&time=&voiceid=&history=&method=iss.getTalk&dpi=&gps=&appsig=6DFB324B5A8B2C27338E2E777A5B4886ACFBFA45
        #ver语义协议版本
        #appsig签名
        appsig = NluRequestClient._getsignature(self, self.confs)
        full_url = (self.url + '?appkey=' + self.appkey + '&udid=' + self.udid + '&ver=' + self.ver + '&method=' + self.method + '&appsig=' + appsig + '&text=' + text)
        return full_url


    def generateNLUresult(self,case):
        case_tmp = case.split('||')
        text = case_tmp[0]
        expect = case_tmp[1]
        url = NluRequestClient._generateUrl(self, text)
        print(url)
        try:
            #log.info('begin ' + text + '...')
            ret = requests.get(url).text
            #print(str(ret))
            #log.info('end ...')
        except Exception as e:
            print(e)
            ret = '请求异常！'
        case_res = [text,expect,ret]
        return case_res





