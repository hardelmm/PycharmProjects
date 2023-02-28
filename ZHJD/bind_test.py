import time

from interface_test import InterfaceTest

# check_bind_url = 'http://47.103.69.208:9096/engine/check'
# bind_url = 'http://47.103.69.208:9096/engine/bind'
# un_bind_url = 'http://47.103.69.208:9096/engine/unbind'
# get_fm_url = 'http://47.103.69.208:9096/engine/rate'
# reg_imei_url = 'http://47.103.69.208:9096/engine/court'
check_bind_url = 'http://47.103.69.208:9096/engine/check'
bind_url = 'http://47.103.69.208:9096/engine/bind'
un_bind_url = 'http://47.103.69.208:9096/engine/unbind'
get_fm_url = 'http://47.103.69.208:9096/engine/rate'
reg_imei_url = 'http://47.103.69.208:9096/engine/court'
time_stp = str(time.time())
# imei = time_stp.replace('.', '')
imei = '866309000198927'
mobile = '111'
name = 300
interface_test = InterfaceTest()

reg_imei_param = 'courtCaseId=003&imei=' + imei + '&name=' + str(name)

reg_imei_res = interface_test.Post(reg_imei_url,reg_imei_param)
print(reg_imei_res)
check_bind_param = 'imei=' + str(imei)

un_bind_res = interface_test.Post(un_bind_url , check_bind_param)
print(un_bind_res)

check_bind_res = interface_test.Post(check_bind_url,check_bind_param)
print(check_bind_res)

bind_param = 'imei=' + imei + '&' + 'mobile=' + mobile
bind_res = interface_test.Post(bind_url,bind_param)
print(bind_res)
bind_param = 'imei=' + imei + '&' + 'mobile=' + mobile
bind_res = interface_test.Post(bind_url,bind_param)
print(bind_res)

check_bind_res = interface_test.Post(check_bind_url,check_bind_param)
print(check_bind_res)
# check_bind_res = interface_test.Post(check_bind_url,check_bind_param)
# print(check_bind_res)
#
# un_bind_res = interface_test.Post(un_bind_url , check_bind_param)
# print(un_bind_res)
#
# check_bind_res = interface_test.Post(check_bind_url,check_bind_param)
# print(check_bind_res)
#
# bind_res = interface_test.Post(bind_url,bind_param)
# print(bind_res)
#
# check_bind_res = interface_test.Post(check_bind_url,check_bind_param)
# print(check_bind_res)
#
# get_fm_res = interface_test.Post(get_fm_url, check_bind_param)
# print(get_fm_res)