# -*- coding: utf-8 -*-
import requests
import os
import logging
import time
import wave
#import pyaudio
import linecache
import xlwt
from readConfig import ReadConfig
import sys
reload(sys)
sys.setdefaultencoding('utf8')

log_tmp = logging.getLogger()
log_tmp.setLevel(logging.WARNING)
screen_h = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(message)s')
screen_h.setFormatter(formatter)
log_tmp.addHandler(screen_h)

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

def get_audio(url, path):
    try:
        pre_content_length = 0
        log_tmp.warning('begin to get ' + path)
        res = requests.get(url, stream=True)
        log_tmp.warning('get data...')
        while True:
            content_length = int(res.headers['content-length'])
            if content_length < pre_content_length or (os.path.exists(path) and os.path.getsize(path) == content_length):
                log_tmp.warning(path + ' get done...')
                break
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                log_tmp.warning('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
                if os.path.getsize(path) > content_length:
                    file.close()
                    os.remove(path)
                    res = requests.get(url, stream=True)
    except Exception as e:
        print(e)


def load_media(text,save_path):
    full_url = (url + 'appkey=' + appkey + '&type=' + type + '&speed=' + speed + '&volume=' + volume +
                '&format=' + format + '&rate=' + rate + '&pitch=' + pitch + '&person=' + person +
                '&start_mute_length=' + start_mute_length + '&end_mute_length=' + end_mute_length + '&text=' + text)
    log_tmp.error(url)
    log_tmp.error(full_url)
    get_audio(full_url, save_path)
    pass

'''
def play_audio(path):
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
'''
def test_result(audio_list,text_list):
    result_path = localReadConfig.get_result_path('tts_result_path')
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    open_excel = xlwt.Workbook(encoding='utf-8')
    open_sheet = open_excel.add_sheet('Sheet1')
    open_sheet.write(0, 0, u'audio')
    open_sheet.write(0, 1, u'text')
    for i in range(len(audio_list)):
        open_sheet.write(i + 1, 0, audio_list[i])
        open_sheet.write(i + 1, 1, text_list[i])
    open_excel.save('./case/test/' + 'audio_text.xls')

case = localReadConfig.get_case_path("tts_case_path")
audio_path = localReadConfig.get_case_path("asr_audio_path")
case_content = linecache.getlines(case)
print('clean audio')
file_list = os.listdir('./case/audio/')
for fileName in file_list:
    os.remove('./case/audio/' + fileName)
print('clean done')
text_list = []
audio_list = []
for i in range(len(case_content)):
    pyth = audio_path + str(i+1) + '.' + format
    #log_tmp.error(case_content[i])
    #log_tmp.error(str(str(i+1) + '.' + format))
    load_media(case_content[i].strip(),pyth)
    text_list.append(case_content[i].strip())
    audio_list.append(str(str(i+1) + '.' + format))
    #play_audio(pyth)
    log_tmp.warning("play done...")

test_result(audio_list,text_list)