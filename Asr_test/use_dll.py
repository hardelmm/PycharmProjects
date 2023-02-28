# -*- coding: utf-8 -*-
import platform
from ctypes import *
import time
from log4j import *
from readConfig import ReadConfig

localReadConfig = ReadConfig()

ip = localReadConfig.get_url('ip')
port = localReadConfig.get_url('port')
appkey = localReadConfig.get_header('appkey')
audioFormat = localReadConfig.get_header('audioFormat')
domains = localReadConfig.get_header('domains')
serviceType = localReadConfig.get_header('serviceType')
voiceField = localReadConfig.get_header('voiceField')
sleeptime = float(localReadConfig.get_sleep_time('sleep_time'))
nlu_param = localReadConfig.get_header('nlu_param')
chunk = int(localReadConfig.get_header('chunk'))
punctuated = localReadConfig.get_header('punctuated')
test_type = localReadConfig.get_test_type('type')

sysstr = platform.system()
file_path = './case/faq_test/1.wav'


def transData(result):
    tmp = string_at(result, -1).decode("utf-8")
    log_tmp.error("USC_RECOGNIZER : " + tmp)
    return tmp


if (sysstr == "Windows"):
    usc = cdll.LoadLibrary("./libs/amd64/libusc.dll")
elif (sysstr == "Linux"):
    usc = cdll.LoadLibrary("./libs/linux64/libusc.so")
else:
    log_tmp.error("Other System tasks")

usc.usc_get_version.restype = c_uint64
usc.usc_get_result.restype = c_uint64

handle = c_longlong()
version = usc.usc_get_version()

ret = usc.usc_create_service_ext(byref(handle), str(ip), int(port))
if ret == 0:
    log_tmp.error("usc_create_service_ext is ok")

# oneshot_key = "你好黑方"

ret = usc.usc_set_option(handle, 9, str(appkey))
ret = usc.usc_set_option(handle, 1001, str(audioFormat))
ret = usc.usc_set_option(handle, 18, str(domains))
if test_type == '2':
    ret = usc.usc_set_option(handle, 201, 'filterName=nlu;returnType=json;')
ret = usc.usc_set_option(handle, 1015, str(serviceType))
ret = usc.usc_set_option_str(handle, 'voiceField', str(voiceField))
ret = usc.usc_set_option_str(handle, 'punctuated', str(punctuated))
# ret = usc.usc_set_option_str(handle, 'oneshot', 'true')
# ret = usc.usc_set_option_str(handle, 'oneshot_key', oneshot_key)
# ret = usc.usc_set_option(handle, 22, '03e038ed-e076-4361-af11-12345678')

ret = usc.usc_login_service(handle)
ret = usc.usc_start_recognizer(handle)
session = usc.usc_get_option(handle, 21)
strsession = transData(session)

f = open(file_path, 'rb')
if (file_path.endswith('.wav')):
    f.seek(44)

data = f.read(chunk)
while data != b'':
    f4 = usc.usc_feed_buffer(handle, data, len(data))
    ret = usc.usc_get_result(handle)
    data = f.read(chunk)
    time.sleep(sleeptime)
    if f4 < 0:
        break
f.close()
ret = usc.usc_stop_recognizer(handle)
ret = usc.usc_get_result(handle)
transData(ret)
