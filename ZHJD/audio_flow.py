# -*- coding: utf-8 -*
import contextlib
import math
import os
import time
import wave
import json
import jsonpath
import pyaudio
import requests
import xlwt
from interface_test import InterfaceTest
from log4j import *
from readConfig import ReadConfig

def get_time():
    time_stp = str(time.time())
    time_stp = time_stp.replace('.', '')
    return time_stp

def get_session_id(courtCaseId):
    # 1.检查绑定（案场/用户）
    check_bind_param = 'imei=' + str(imei)
    check_bind_res = interface_test.Post(check_bind_url, check_bind_param)
    # sessionId = str(jsonpath.jsonpath(check_bind_res, '$..sessionId')[0])
    log_tmp.error('检查绑定： ' + str(json.dumps(check_bind_res, ensure_ascii=False)))
    if str(check_bind_res['data']['bindState']) == 'True':  # 如果是绑定状态，则解绑
        un_bind_res = interface_test.Post(un_bind_url, check_bind_param)
        log_tmp.error('设备解绑： ' + str(json.dumps(un_bind_res, ensure_ascii=False)))

    # 2.注册案场
    reg_imei_param = 'courtCaseId=' + courtCaseId + '&imei=' + imei + '&name=' + name
    reg_imei_res = interface_test.Post(reg_imei_url, reg_imei_param)
    log_tmp.error('注册案场： ' + str(json.dumps(reg_imei_res, ensure_ascii=False)))

    # 3.设备绑定用户
    bind_param = 'imei=' + imei + '&' + 'mobile=' + mobile
    bind_res = interface_test.Post(bind_url, bind_param)
    log_tmp.error('设备绑定用户：  ' + str(json.dumps(bind_res, ensure_ascii=False)))

    # 4.获取sessionId
    if bind_res['message'] == '绑定成功':
        check_bind_res = interface_test.Post(check_bind_url, check_bind_param)
        sessionId = str(jsonpath.jsonpath(check_bind_res, '$..sessionId')[0])
        log_tmp.error('sessionId：  ' + check_bind_res['data']['sessionId'])
    else:
        log_tmp.error("获取sessionId失败，请检查绑定")

    return sessionId


def rate_time(audio_path):
    if audio_path[-3:] == 'wav':
        with contextlib.closing(wave.open(audio_path, 'r')) as f:
            frames = f.getnframes()
        rate = f.getframerate()
        #log_tmp.error('frames:'+ str(frames))
        #log_tmp.error('rate:'+str(rate))
        #duration = frames / float(rate)
        duration = frames / float(rate)
        #log_tmp.error('duration:'+str(duration))
        duration_final = math.ceil(duration)
        #log_tmp.error('duration_final:'+str(duration_final))
        return duration_final
    else:
        return 0

def get_audio(url, path):
    try:
        pre_content_length = 0
        print('begin to get ' + path)
        res = requests.get(url, stream=True)
        print('get data...')
        while True:
            content_length = int(res.headers['content-length'])
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                print(path + ' playing...')
                break
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d   total size:%d' % (os.path.getsize(path), content_length))
                if os.path.getsize(path) > content_length:
                    file.close()
                    os.remove(path)
                    res = requests.get(url, stream=True)
    except Exception as e:
        print(e)

def play_audio(audio_path):
    chunk = 1024
    f = wave.open(audio_path, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)

    data = f.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = f.readframes(chunk)
    print('play audio ' + str(audio_path) + ' done.')
    stream.stop_stream()
    stream.close()

url = 'http://47.103.69.208:9096/audio/next'
url_next = 'http://47.103.69.208:9096/audio/advance'

run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))

time_stp = str(time.time())
time_stp = time_stp.replace('.', '')

def audio_test(session_id):
    list_res = []
    count = 0#统计音频数量
    while True:
        post_data = 'sessionId=' + str(session_id)
        r = interface_test.Post(url, post_data)
        r_next = interface_test.Post(url_next, post_data)
        res_text = jsonpath.jsonpath(r, '$..text')[0].strip()
        res_audio = jsonpath.jsonpath(r, '$..url')[0]
        res_duration = jsonpath.jsonpath(r, '$..duration')[0]
        log_tmp.error(str(r_next))
        if jsonpath.jsonpath(r_next, '$..text'):
            res_text_next = jsonpath.jsonpath(r_next, '$..text')[0].strip()
        else:
            res_text_next = 'Null'
        if jsonpath.jsonpath(r_next, '$..url'):
            res_audio_next = jsonpath.jsonpath(r_next, '$..url')[0]
        else:
            res_audio_next = 'Null'
        if jsonpath.jsonpath(r, '$..isEnd'):
            if jsonpath.jsonpath(r, '$..isEnd')[0] == 0:
                count += 1
                get_audio(jsonpath.jsonpath(r, '$..url')[0], audio_path + str(count) + '.wav')
                audio_name = str(count) + '.wav'
                audio_duration = rate_time(audio_path + str(count) + '.wav')
                #play_audio(str(count) + '.wav')
                list_res.append(audio_name + '||' + res_text + '||' + res_audio + '||' + str(res_duration) + '||' + str(audio_duration) + '||' + res_audio_next + '||' + res_text_next)
            elif jsonpath.jsonpath(r, '$..isEnd')[0] == 1:
                count += 1
                get_audio(jsonpath.jsonpath(r, '$..url')[0], audio_path + str(count) + '.wav')
                audio_name = str(count) + '.wav'
                audio_duration = rate_time(audio_path + str(count) + '.wav')
                #play_audio(str(count) + '.wav')

                list_res.append(audio_name + '||' + res_text + '||' + res_audio + '||' + str(res_duration) + '||' + str(audio_duration) + '||' + res_audio_next + '||' + res_text_next)
                break
            #list_res.append(audio_name + '||' + res_text + '||' + res_audio + '||' + str(res_duration) + '||' + str(audio_duration) + '||' + res_audio_next)
        else:
            print('error')
            print(str(r))
            break

    return list_res

def test_result(courtCaseId,list_res):
    audio_name = []
    res_text = []
    res_audio = []
    audio_duration = []
    res_duration = []
    res_audio_next = []
    res_text_next = []

    pass_count = 0

    if len(list_res) > 0:
        for z in range(len(list_res)):
            save_tmp = list_res[z].split('||')
            audio_name.append(save_tmp[0])
            res_text.append(save_tmp[1])
            res_audio.append(save_tmp[2])
            res_duration.append(save_tmp[3])
            audio_duration.append(save_tmp[4])
            res_audio_next.append(save_tmp[5])
            res_text_next.append(save_tmp[6])

    open_excel = xlwt.Workbook(encoding='utf-8')
    open_sheet = open_excel.add_sheet('Sheet1')
    open_sheet.write(0, 0, u'AUDIO_NAME')
    open_sheet.write(0, 1, u'TEXT')
    open_sheet.write(0, 2, u'AUDIO_URL')
    open_sheet.write(0, 3, u'接口返回duration')
    open_sheet.write(0, 4, u'实际音频时长')
    open_sheet.write(0, 5, u'NEXT_AUDIO')
    open_sheet.write(0, 6, u'res_text_next')
    open_sheet.write(0, 7, u'result')
    if len(res_text) > 0:
        for x in range(len(res_text)):
            #if result[x] == 'Pass' or 'The final audio！':
             #   pass_count += 1

            #if res_duration[x] == audio_duration[x]:
            if x < len(audio_name) - 1:
                if res_audio_next[x] == res_audio[x + 1] and res_text_next[x] == res_text[x + 1]:
                    result = 'Pass'
                else:
                    result = 'next audio url wrong！'
            else:
                result = 'The final audio！'
            #else:
                #result = 'audio time not match duaration'
            if result == 'Pass' or 'The final audio！':
                pass_count += 1
            open_sheet.write(x + 1, 0, audio_name[x])
            open_sheet.write(x + 1, 1, res_text[x])
            open_sheet.write(x + 1, 2, res_audio[x])
            open_sheet.write(x + 1, 3, res_duration[x])
            open_sheet.write(x + 1, 4, audio_duration[x])
            open_sheet.write(x + 1, 5, res_audio_next[x])
            open_sheet.write(x + 1, 6, res_text_next[x])
            open_sheet.write(x + 1, 7, result)

        open_excel.save(result_path + './result_' + '案场' + courtCaseId + '音频流程_' + run_time + '.xls')


if __name__ == '__main__':
    interface_test = InterfaceTest()
    localReadConfig = ReadConfig()
    audio_path = localReadConfig.get_result_path("audio_flow_path") + 'audio/'
    result_path = localReadConfig.get_result_path("audio_flow_path") + 'result/'
    ip = localReadConfig.get_url('ip')
    imei = localReadConfig.get_req_param('imei')
    mobile = localReadConfig.get_req_param('phone')
    name = localReadConfig.get_req_param('name')
    courtCaseId = localReadConfig.get_req_param('courtCaseId')
    speechcraftId = localReadConfig.get_req_param('speechcraftId')

    check_bind_url = 'http://' + str(ip) + ':9096/engine/check'
    bind_url = 'http://' + str(ip) + ':9096/engine/bind'
    un_bind_url = 'http://' + str(ip) + ':9096/engine/unbind'
    reg_imei_url = 'http://' + str(ip) + ':9096/engine/court'
    reg_imei_param = 'courtCaseId=' + courtCaseId + '&imei=' + imei + '&name=' + name
    check_bind_param = 'imei=' + str(imei)
    bind_param = 'imei=' + imei + '&' + 'mobile=' + mobile

    print('clean audio')
    file_list = os.listdir(audio_path)
    for fileName in file_list:
        os.remove(audio_path + fileName)
    print('clean done')

    session_id = get_session_id(courtCaseId)
    list_res = audio_test(session_id)
    test_result(courtCaseId,list_res)

    log_tmp.error("案场" + courtCaseId + ' 音频流程 done!')

