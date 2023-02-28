# -*- coding: utf-8 -*-
import os
from ctypes import *
import time
import threading
import json
import jsonpath
import string
import linecache
import xlwt
import xlrd
import codecs
import platform
from log4j import *
from multiprocessing import Pool, Manager
from readConfig import ReadConfig
from case_avg import caseAvg
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))
localReadConfig = ReadConfig()
sysstr = platform.system()

sys_str = platform.system()
if sys_str == "Windows":
    usc = cdll.LoadLibrary("./libs/amd64/libusc.dll")
elif sys_str == "Linux":
    usc = cdll.LoadLibrary("./libs/linux64/libusc.so")
else:
    log_tmp.error("Other System tasks")
    exit()
audio_path = str(localReadConfig.get_case_path('asr_audio_path'))
ip = localReadConfig.get_url('ip')
port = localReadConfig.get_url('port')
appkey = localReadConfig.get_header('appkey')
udid = localReadConfig.get_header('udid')
audioFormat = localReadConfig.get_header('audioFormat')
best_result_return = localReadConfig.get_header('best_result_return')
modelType = localReadConfig.get_header('modelType')
oneshot_key = localReadConfig.get_header('oneshot_key')
oneshot = localReadConfig.get_header('oneshot')
#productLine = localReadConfig.get_header('productLine')
#sampleRate = localReadConfig.get_header('sampleRate')
textFormat = localReadConfig.get_header('textFormat')
variable = localReadConfig.get_header('variable')
voiceField = localReadConfig.get_header('voiceField')
chunk = int(localReadConfig.get_header('chunk'))
#closeVad = localReadConfig.get_header('closeVad')
punctuated = localReadConfig.get_header('punctuated')
punctuated_type = localReadConfig.get_header('punctuated_type')
serviceType = localReadConfig.get_header('serviceType')
sleeptime = float(localReadConfig.get_sleep_time('sleep_time'))
tr_param = localReadConfig.get_header('tr_param')
nlu_param = localReadConfig.get_header('nlu_param')

test_type = localReadConfig.get_test_type('type')
usc.usc_get_version.restype = c_uint64
usc.usc_get_result.restype = c_uint64

def transData( result):
    tmp = string_at(result, -1).decode("utf-8")
    # log_tmp.error("USC_RECOGNIZER : " + tmp)
    return tmp

def asr_test(case_list, result_list):
    #传入音频、语料，pass条件同时满足"好的，已为您操作"且识别结果和语料文本一致，输出result_list
    for i in range(len(case_list)):
        try:
            file_content_tmp = case_list[i].split('||')
            audio_list = file_content_tmp[0].strip()
            expectedTexts  = file_content_tmp[1].strip()
            handle = c_longlong()
            ret = usc.usc_create_service_ext(byref(handle), str(ip), int(port))

            if ret == 0:
                log_tmp.info("usc_create_service_ext is ok")
            else:
                log_tmp.error(transData(ret))
                result_list.append(
                    str(audio_list) + '||' + "error" + '||' + str(transData(ret)) + '||' + str(0) + '||' + str(0)
                    + str(0) + '||' + str(0) + '||' + 'no session' + '||' + "创建识别接口失败")
                continue
            ret = usc.usc_set_option(handle, 9, str(appkey))
            ret = usc.usc_set_option(handle, 22, str(udid))
            ret = usc.usc_set_option_str(handle, 'audioFormat', str(audioFormat))
            ret = usc.usc_set_option_str(handle, 'best_result_return', str(best_result_return))
            ret = usc.usc_set_option_str(handle, 'productLine', 'normal')
            ret = usc.usc_set_option(handle, 18, str(modelType))
            ret = usc.usc_set_option_str(handle, 'oneshot', str(oneshot))
            ret = usc.usc_set_option_str(handle, 'oneshot_key', str(oneshot_key))
            ret = usc.usc_set_option(handle, 1006, str(textFormat))
            ret = usc.usc_set_option(handle, 35, str(variable))
            ret = usc.usc_set_option_str(handle, 'voiceField', str(voiceField))
            ret = usc.usc_set_option_str(handle, 'punctuated', str(punctuated))
            ret = usc.usc_set_option_str(handle, 'punctuated_type', str(punctuated_type))
            ret = usc.usc_set_option(handle, 201, str(tr_param))
            ret = usc.usc_set_option(handle, 1015, str(serviceType))
            #ret = usc.usc_set_option_str(handle,'filterUrl', str(filterUrl))
            #ret = usc.usc_set_option(handle, 22, 'LTE3Nzg0MjcyMTUwMDVhN2JlNWUxN2JlMQ')

            #ret = usc.usc_login_service(handle)
            ret = usc.usc_start_recognizer(handle)
            session = usc.usc_get_option(handle, 21)#获取参数值
            strsession = transData(session)
            log_tmp.error(str(audio_list) + ' session is ' + str(strsession))
            f = open(audio_path + audio_list, 'rb')
            if (audio_list.endswith('.wav')):
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
            time3 = round(time.time(), 3)
            res_tmp = transData(ret)
            asr_res = json.loads(res_tmp)
            log_tmp.error("||"+res_tmp)
            expectedText = str(expectedTexts).strip()
            if jsonpath.jsonpath(asr_res, '$..text'):
                actualText = str(asr_res['text']).strip().replace(' ', '')
                if jsonpath.jsonpath(asr_res, '$..asr_recongize'):
                    asr_recongize = str(asr_res['asr_recongize']).strip().replace(' ','')
                    #if expectedText in asr_recongize and expectedText in actualText:#判断语料和文本识别结果是否一致
                    if expectedText in asr_recongize:  # 判断语料和文本识别结果是否一致
                        result_list.append(str(audio_list) + '||' + expectedText + '||' + actualText + '||' + str(res_tmp) + '||' + str(time1) + '||' + str(time2) + '||' + str(time3) + '||' + str(strsession) + '||' + "成功")
                    else:
                            result_list.append(str(audio_list) + '||' + expectedText + '||' + actualText + '||' + str(res_tmp) + '||' + str(time1) + '||' + str(time2) + '||' + str(time3) + '||' + str(strsession) + '||' + "失败")
                else:
                    result_list.append(str(audio_list) + '||' + expectedText + '||' + actualText + '||' + str(res_tmp) + '||' + str(time1) + '||' + str(time2) + '||' + str(time3) + '||' + str(strsession) + '||' + "音频识别错误")
            else:
                result_list.append(str(audio_list) + '||' + expectedText + '||' + "识别结果为空" + '||' + str(res_tmp) + '||' + str(time1) + '||' + str(time2) + '||' + str(time3) + '||' + str(strsession) + '||' + "识别结果为空")
        except BaseException as err:
            log_tmp.error(err + '====' +strsession)
            result_list.append(str(audio_list) + '||' + expectedText + '||' + actualText + '||' + str(res_tmp) + '||' + str(time1) + '||' + str(time2) + '||' + str(time3) + '||' + str(strsession) + '||' + "异常失败")
        finally:
            f.close()
    #log_tmp.error(str(result_list))
    return result_list



def main(list_res):
    file_list = os.listdir("./case_avg/")
    p = Pool(len(file_list))
    for i in range(len(file_list)):
        list_tmp = []
        file_content = linecache.getlines("./case_avg/" + file_list[i])
        for m in range(len(file_content)):
            list_tmp.append(file_content[m].strip())
        p.apply_async(asr_test, args=(list_tmp, list_res))
    p.close()
    p.join()
    return list_res

if __name__ == '__main__':
    audio_list = []
    expectedText_list = []
    actualText_list = []
    res_list = []
    res_time = []
    req_time_1 = []
    req_time_2 = []
    session_list = []
    result_list = []
    url_list = []
    krc_audio_list = []

    std_content = []
    rate = []
    asr_text = []
    do_case = caseAvg()
    do_case.case_avg()
    list_tmp = Manager().list()
    main(list_tmp)

    err_rate = localReadConfig.get_errorRate('switch')
    task_name = localReadConfig.get_task_name('name')
    test_type = localReadConfig.get_test_type('type')
    std_file = localReadConfig.get_result_path('stdfile')

    for z in range(len(list_tmp)):
        do_list = list_tmp[z].split('||')
        audio_list.append(do_list[0])
        expectedText_list.append(do_list[1])
        actualText_list.append(do_list[2])
        res_list.append(do_list[3])
        req_time_1.append(do_list[4])
        req_time_2.append(do_list[5])
        res_time.append(do_list[6])
        session_list.append(do_list[7])
        result_list.append(do_list[8])

    open_excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
    open_sheet = open_excel.add_sheet('Sheet1')
    open_sheet.write(0, 0, u'测试音频')
    open_sheet.write(0, 1, u'测试语料')
    open_sheet.write(0, 2, u'识别结果')
    open_sheet.write(0, 3, u'响应结果')
    open_sheet.write(0, 4, u'all_time')
    open_sheet.write(0, 5, u'last_time')
    open_sheet.write(0, 6, u'ASR_session')
    open_sheet.write(0, 7, u'结果')
    if len(audio_list) > 0:
        for x in range(len(audio_list)):
            open_sheet.write(x + 1, 0, audio_list[x])
            open_sheet.write(x + 1, 1, expectedText_list[x])
            open_sheet.write(x + 1, 2, actualText_list[x])
            open_sheet.write(x + 1, 3, res_list[x])
            open_sheet.write(x + 1, 4, round(float(res_time[x]) - float(req_time_1[x]), 3) * 1000)
            open_sheet.write(x + 1, 5, round(float(res_time[x]) - float(req_time_2[x]), 3) * 1000)
            open_sheet.write(x + 1, 6, session_list[x])
            open_sheet.write(x + 1, 7, result_list[x])
        open_excel.save('./result/' + str(task_name) + '_result_' + str(run_time) + '.xls')
    else:
        print('save none!')
'''
#生成结果日志
    res_file = codecs.open("./result/" + str(task_name) + '_' + run_time + '.log', 'ab','utf-8')
    for x in range(len(audio_list)):
        if x == len(audio_list) - 1:
            res_file.write(str(audio_list[x]) + '\t' + str(res_list[x]))
        else:
            res_file.write(str(audio_list[x]) + '\t' + str(res_list[x]) + '\n')
    res_file.close()
'''