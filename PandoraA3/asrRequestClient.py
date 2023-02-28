# -*- coding: utf-8 -*-
import os
from ctypes import *
import time
import json
import platform
from tools.log4j import *
from readConfig import ReadConfig
import sys
reload(sys)
sys.setdefaultencoding('utf8')
run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))

class ASRequestClient:
    def __init__(self):
        print("读取ASR配置...")
        localReadConfig = ReadConfig()
        self.audio_path = str(localReadConfig.get_case_path('asr_audio_path'))
        self.ip = localReadConfig.get_url('ip')
        self.port = localReadConfig.get_url('port')
        self.appkey = localReadConfig.get_header('appkey')
        self.udid = localReadConfig.get_header('udid')
        self.audioFormat = localReadConfig.get_header('audioFormat')
        self.best_result_return = localReadConfig.get_header('best_result_return')
        self.modelType = localReadConfig.get_header('modelType')
        self.oneshot_key = localReadConfig.get_header('oneshot_key')
        self.oneshot = localReadConfig.get_header('oneshot')
        # self.productLine = localReadConfig.get_header('productLine')
        # self.sampleRate = localReadConfig.get_header('sampleRate')
        self.textFormat = localReadConfig.get_header('textFormat')
        self.variable = localReadConfig.get_header('variable')
        self.voiceField = localReadConfig.get_header('voiceField')
        self.chunk = int(localReadConfig.get_header('chunk'))
        # self.closeVad = localReadConfig.get_header('closeVad')
        self.punctuated = localReadConfig.get_header('punctuated')
        self.punctuated_type = localReadConfig.get_header('punctuated_type')
        self.serviceType = localReadConfig.get_header('serviceType')
        self.sleeptime = float(localReadConfig.get_sleep_time('sleep_time'))
        self.tr_param = localReadConfig.get_header('tr_param')
        self.nlu_param = localReadConfig.get_header('nlu_param')
        print("读取ASR配置完成...")

    '''
    @staticmethod
    def loadLibrary():
        sys_str = platform.system()
        if sys_str == "Windows":
            usc = cdll.LoadLibrary("./libs/amd64/libusc.dll")
        elif sys_str == "Linux":
            usc = cdll.LoadLibrary("./libs/linux64/libusc.so")
        else:
            log.error("Other System tasks")
            exit()
        return usc
    '''

    @staticmethod
    def transData(result):
        tmp = string_at(result, -1).decode("utf-8")
        return str(tmp)

    def generateASResult(self,case_list):
        result_list = []
        case_text = case_list[0]
        case_audio = case_list[1]
        expectedRes = case_list[2]

        ip = str(self.ip)
        port = int(self.port)
        appkey = str(self.appkey)
        udid = str(self.udid)
        audioFormat = str(self.audioFormat)
        best_result_return = str(self.best_result_return)
        modelType = str(self.modelType)
        onshot = str(self.oneshot)
        oneshot_key = str(self.oneshot_key)
        textFormat = str(self.textFormat)
        variable = str(self.variable)
        voiceField = str(self.voiceField)
        punctuated = str(self.punctuated)
        punctuated_type = str(self.punctuated_type)
        tr_param = str(self.tr_param)
        serviceType = str(self.serviceType)
        audio_path = self.audio_path
        chunk = self.chunk
        sleeptime = self.sleeptime

        sys_str = platform.system()
        if sys_str == "Windows":
            usc = cdll.LoadLibrary("./libs/amd64/libusc.dll")
        elif sys_str == "Linux":
            usc = cdll.LoadLibrary("./libs/linux64/libusc.so")
        else:
            log.error("Other System tasks")
            exit()
        #usc = ASRequestClient.loadLibrary()
        usc.usc_get_version.restype = c_uint64
        usc.usc_get_result.restype = c_uint64

        handle = c_longlong()
        ret = usc.usc_create_service_ext(byref(handle), ip, port)
        #print(ret)
        if ret == 0:
            log.info("usc_create_service_ext is ok")
        else:
            log.error(ASRequestClient.transData(ret))
        ret = usc.usc_set_option(handle, 9, appkey)
        #print(str(appkey)+"==="+str(ret))
        ret = usc.usc_set_option(handle, 22, udid)
        #print(str(udid) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'audioFormat', audioFormat)
        #print(str(audioFormat) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'best_result_return', best_result_return)
        #print(str(best_result_return) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'productLine', 'normal')
        #print('productLine' + "===" + str(ret))
        ret = usc.usc_set_option(handle, 18, modelType)
        #print(str(modelType) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'oneshot', onshot)
        #print('oneshot' + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'oneshot_key', oneshot_key)
        #print('oneshot_key' + "===" + str(ret))
        ret = usc.usc_set_option(handle, 1006, textFormat)
        #print(str(textFormat) + "===" + str(ret))
        ret = usc.usc_set_option(handle, 35, variable)
        #print(str(variable) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'voiceField', voiceField)
        #print(str(voiceField) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'punctuated', punctuated)
        #print(str(punctuated) + "===" + str(ret))
        ret = usc.usc_set_option_str(handle, 'punctuated_type', punctuated_type)
        #print(str(punctuated_type) + "===" + str(ret))
        ret = usc.usc_set_option(handle, 201, tr_param)
        #print(str(tr_param) + "===" + str(ret))
        ret = usc.usc_set_option(handle, 1015, serviceType)
        #print(str(serviceType) + "===" + str(ret))
        #ret = usc.usc_set_option_str(handle,'filterUrl', str(filterUrl))
        #ret = usc.usc_set_option(handle, 22, 'LTE3Nzg0MjcyMTUwMDVhN2JlNWUxN2JlMQ')

        ret = usc.usc_login_service(handle)
        #print(ret)
        ret = usc.usc_start_recognizer(handle)
        #print(ret)
        session = usc.usc_get_option(handle, 21)#获取参数值
        strsession = ASRequestClient.transData(session)
        log.info(str(case_audio) + ' session is ' + str(strsession))
        f = open((audio_path + case_audio).decode('utf-8'), 'rb')
        if (case_audio.endswith('.wav')):
            f.seek(44)
        data = f.read(chunk)#读取字节数
        time1 = round(time.time(), 3)
        while data != b'':
            f4 = usc.usc_feed_buffer(handle, data, len(data))#识别语音数据
            time2 = round(time.time(), 3)
            ret = usc.usc_get_result(handle)#获得识别结果
            data = f.read(chunk)
            time.sleep(sleeptime)
            if f4 < 0:
                break
        usc.usc_stop_recognizer(handle)#停止识别
        ret = usc.usc_get_result(handle)
        #print(ret)
        f.close()
        time3 = round(time.time(), 3)
        res_tmp = ASRequestClient.transData(ret)
        print(res_tmp)
        #asr_res = json.loads(res_tmp)
        result_list.append(str(case_text))
        result_list.append(str(case_audio))
        result_list.append(str(res_tmp))
        result_list.append(str(expectedRes))
        result_list.append(str(time1))
        #result_list.append(str(time2))
        result_list.append(str(time3))
        result_list.append(strsession)
        return result_list
