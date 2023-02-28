# -*- coding: utf-8 -*-
import requests
import os
import logging
import wave
import pyaudio
import linecache
from readConfig import ReadConfig

log_tmp = logging.getLogger()
log_tmp.setLevel(logging.WARNING)
screen_h = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s')
screen_h.setFormatter(formatter)
log_tmp.addHandler(screen_h)

class TTSClient:
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False

    localReadConfig = ReadConfig()
    real_url = localReadConfig.get_url("url_choise")
    url = localReadConfig.get_url(real_url)
    appkey = localReadConfig.get_tts_param("tts_appkey")
    type = localReadConfig.get_tts_param("type")
    speed = localReadConfig.get_tts_param("speed")
    volume = localReadConfig.get_tts_param("volume")
    format = localReadConfig.get_tts_param("format")
    rate = localReadConfig.get_tts_param("rate")
    pitch = localReadConfig.get_tts_param("pitch")
    start_mute_length = localReadConfig.get_tts_param("start_mute_length")
    end_mute_length = localReadConfig.get_tts_param("end_mute_length")
    person = localReadConfig.get_tts_param('person')
    path = localReadConfig.get_path('result_path')

    def _generateUrl(self,text):
        full_url = (self.url + 'appkey=' + self.appkey + '&type=' + self.type + '&speed=' + self.speed + '&volume=' + self.volume +
                    '&format=' + self.format + '&rate=' + self.rate + '&pitch=' + self.pitch + '&person=' + self.person +
                    '&start_mute_length=' + self.start_mute_length + '&end_mute_length=' + self.end_mute_length + '&text=' + text)
        log_tmp.error(full_url)
        return full_url

    def generateAudio(self,text,list_res):
        url = self._generateUrl(text)
        #result_list = []
        path = self.path + 'audio/' + text.strip() + '.' + self.format
        audioname = text.strip() + '.' + self.format
        try:
            pre_content_length = 0
            log_tmp.warning('begin to get ' + path)
            res = requests.get(url, stream=True)
            log_tmp.warning('get data...')
            while True:
                content_length = int(res.headers['content-length'])
                if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                    log_tmp.warning(path + ' get done...')
                    break
                with open(path, 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    log_tmp.warning(
                        'receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
                    if os.path.getsize(path) > content_length:
                        file.close()
                        os.remove(path)
                        res = requests.get(url, stream=True)
            list_res.append([text,audioname ])
            #print(text)
        except Exception as e:
            print(e)
        return list_res

    def play_audio(self,path):
        chunk = 1024
        f = wave.open(path, "rb")
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        data = f.readframes(chunk)
        while data !=  b'':
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()


    def ttsclient_main(self,file_name,list_res):
        list_tmp = linecache.getlines('./avg_tmp/' + file_name)
        for i in range(len(list_tmp)):
            try:
                case_text = list_tmp[i].strip()
                list_res = self.generateAudio(case_text,list_res)
            except BaseException as err:
                log_tmp.error(err)
        return list_res

