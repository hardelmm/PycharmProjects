# -*- coding: utf-8 -*-
import requests
from tools.log4j import *
from readCase import *
from readConfig import *


class TTSRequestClient:
    def __init__(self):
        print("读取TTS配置...")
        localReadConfig = ReadConfig()
        self.real_url = localReadConfig.get_url("url_choise")
        self.url = localReadConfig.get_url(self.real_url)
        self.appkey = localReadConfig.get_tts_param("tts_appkey")
        self.type = localReadConfig.get_tts_param("type")
        self.speed = localReadConfig.get_tts_param("speed")
        self.volume = localReadConfig.get_tts_param("volume")
        self.format = localReadConfig.get_tts_param("format")
        self.rate = localReadConfig.get_tts_param("rate")
        self.pitch = localReadConfig.get_tts_param("pitch")
        self.start_mute_length = localReadConfig.get_tts_param("start_mute_length")
        self.end_mute_length = localReadConfig.get_tts_param("end_mute_length")
        self.person = localReadConfig.get_tts_param("person")
        self.case = localReadConfig.get_case_path("tts_case_path")
        self.audio_path = localReadConfig.get_case_path("asr_audio_path")
        self.result_path = localReadConfig.get_result_path("tts_result_path")
        print("读取TTS配置完成...")

        print('清除历史音频...')
        file_list = os.listdir('./case/audio/')
        for fileName in file_list:
            os.remove('./case/audio/' + fileName)
        print('清除历史音频完成...')


    def getcaseText(self):
        print('读取语料...')
        actcase = readXld(self.case)
        case_list = actcase.readFile()
        print('读取语料完成...')
        return case_list

    #@staticmethod
    def generateUrl(self,text):
        full_url = (self.url + 'appkey=' + self.appkey + '&type=' + self.type + '&speed=' + self.speed + '&volume=' + self.volume +
                    '&format=' + self.format + '&rate=' + self.rate + '&pitch=' + self.pitch + '&person=' + self.person +
                    '&start_mute_length=' + self.start_mute_length + '&end_mute_length=' + self.end_mute_length + '&text=' + text)
        return full_url

    def generateAudio(self,text):
        url = TTSRequestClient.generateUrl(self,text)
        path = self.audio_path + text + '.' + self.format
        try:
            pre_content_length = 0
            log.info('begin to get ' + path)
            res = requests.get(url, stream=True)
            log.info('get data...')
            while True:
                content_length = int(res.headers['content-length'])
                if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                    log.info(path + ' get done...')
                    break
                with open(path, 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    log.info('receive data，file size : %d  total size:%d' % (os.path.getsize(path), content_length))
                    if os.path.getsize(path) > content_length:
                        file.close()
                        os.remove(path)
                        res = requests.get(url, stream=True)
        except Exception as e:
            print(e)
        audioname = str(text.strip() + '.' + self.format)
        return audioname
