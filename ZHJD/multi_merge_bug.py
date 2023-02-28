# -*- coding: utf-8 -*-
import requests
import json
import jsonpath
import linecache
import time
import xlwt
from merge_case_avg import *
from multiprocessing import Pool, Manager
from interface_test import InterfaceTest
from log4j import *
from courtCase import *


def get_time():
    time_stp = str(time.time())
    time_stp = time_stp.replace('.', '')
    return time_stp

def rate_time_sec(begin, now):
    seconds = now - begin
    return seconds

begin_time = int(time.time())
interface_test = InterfaceTest()
run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))
begin = int(time.time())

localReadConfig = ReadConfig()

ip = localReadConfig.get_url('ip')
port = localReadConfig.get_url('port')
imei = localReadConfig.get_req_param('imei')
mobile = localReadConfig.get_req_param('phone')
name = localReadConfig.get_req_param('name')
speechcraftId = localReadConfig.get_req_param('speechcraftId')

url = 'http://' + str(ip) + ':9099/test/nlu?sessionId='
check_bind_url = 'http://' + str(ip) + ':' + port + '/engine/check'
bind_url = 'http://' + str(ip) + ':' + port + '/engine/bind'
un_bind_url = 'http://' + str(ip) + ':' + port + '/engine/unbind'
reg_imei_url = 'http://' + str(ip) + ':' + port + '/engine/court'

check_bind_param = 'imei=' + str(imei)
bind_param = 'imei=' + imei + '&' + 'mobile=' + mobile

def get_session_id(courtCaseId):

    #1.检查绑定（案场/用户）
    check_bind_param = 'imei=' + str(imei)
    check_bind_res = interface_test.Post(check_bind_url, check_bind_param)
    #sessionId = str(jsonpath.jsonpath(check_bind_res, '$..sessionId')[0])
    log_tmp.error('检查绑定： ' + str(json.dumps(check_bind_res,ensure_ascii=False)))
    if str(check_bind_res['data']['bindState'])=='True':#如果是绑定状态，则解绑
        un_bind_res = interface_test.Post(un_bind_url, check_bind_param)
        log_tmp.error('设备解绑： '+str(json.dumps(un_bind_res,ensure_ascii=False)))

    # 2.注册案场
    reg_imei_param = 'courtCaseId=' + courtCaseId + '&imei=' + imei + '&name=' + name
    reg_imei_res = interface_test.Post(reg_imei_url, reg_imei_param)
    log_tmp.error('注册案场： '+ str(json.dumps(reg_imei_res,ensure_ascii=False)))

    #3.设备绑定用户
    bind_param = 'imei=' + imei + '&' + 'mobile=' + mobile
    bind_res = interface_test.Post(bind_url, bind_param)
    log_tmp.error('设备绑定用户：  '+ str(json.dumps(bind_res,ensure_ascii=False)))

    #4.获取sessionId
    if bind_res['message']=='绑定成功':
        check_bind_res = interface_test.Post(check_bind_url, check_bind_param)
        sessionId = str(jsonpath.jsonpath(check_bind_res, '$..sessionId')[0])
        log_tmp.error('sessionId：  '+ check_bind_res['data']['sessionId'])
    else:
        log_tmp.error("获取sessionId失败，请检查绑定")

    return sessionId

requests.adapters.DEFAULT_RETRIES = 5

def test_result(courtCaseId,list_res):
    conversation_list1 = []
    conversation_list2 = []
    conversation_list3 = []
    conversation_list4 = []
    conversation_list5 = []
    log_path = localReadConfig.get_result_path('ivn_test_path')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    fail_count = 0
    if len(list_res) > 0:
        for z in range(len(list_res)):
            save_tmp = list_res[z].split('||')
            conversation_list1.append(save_tmp[0])
            conversation_list2.append(save_tmp[1])
            conversation_list3.append(save_tmp[2])
            conversation_list4.append(save_tmp[3])
            conversation_list5.append(save_tmp[4])
            if save_tmp[4] == 'Fail':
                fail_count += 1
        log_tmp.error('案场' + courtCaseId + ' fail num is:' + str(fail_count))
        open_excel = xlwt.Workbook(encoding='utf-8')
        open_sheet = open_excel.add_sheet('Sheet1')
        open_sheet.write(0, 0, u'语料')
        open_sheet.write(0, 1, u'预期问题')
        open_sheet.write(0, 2, u'预期回答')
        #open_sheet.write(0, 3, u'实际问题')
        open_sheet.write(0, 3, u'实际回答')
        open_sheet.write(0, 4, u'执行结果')
        for excel_line in range(len(conversation_list1)):
            open_sheet.write(excel_line + 1, 0, conversation_list1[excel_line])
            open_sheet.write(excel_line + 1, 1, conversation_list2[excel_line])
            open_sheet.write(excel_line + 1, 2, conversation_list3[excel_line])
            open_sheet.write(excel_line + 1, 3, conversation_list4[excel_line])
            open_sheet.write(excel_line + 1, 4, conversation_list5[excel_line])
        open_excel.save(log_path + 'auto_test_result_' + courtCaseId + '_' + run_time + '.xls')

def auto_test(bd, qa, sessionId, file_name, list_res, all_num):
    bd = json.loads(bd)
    qa = json.loads(qa)
    log_tmp.error(str(json.dumps(bd,ensure_ascii=False)))
    log_tmp.error(str(json.dumps(qa,ensure_ascii=False)))
    case_text = []
    questionFocus = []
    file_content_all = linecache.getlines('./avg_tmp/' + file_name)
    for i in range(len(file_content_all)):
        try:
            file_content_tmp = file_content_all[i].split('||')
            expectedQues = file_content_tmp[0].strip()
            case_text = file_content_tmp[1].strip()
            questionFocus = file_content_tmp[2].strip()
            response = requests.get(url + sessionId + '&text=' + case_text + '&speechcraftId=' + speechcraftId)
            response.enconding = "utf-8"
            r = json.loads(response.content.decode("utf-8"))
            if jsonpath.jsonpath(r, '$..audioText'):
                tmp_text = str(r['audioText']).replace("\n","").replace("\r","").strip()
                if bd.get(questionFocus):
                    if tmp_text == bd.get(questionFocus):
                        log_tmp.error(case_text.strip() + ' is Pass')
                        list_res.append(case_text + '||' + expectedQues + '||' + questionFocus + '||' + tmp_text + '||' + 'Pass')
                    else:
                        log_tmp.error(case_text.strip() + ' is Fail')
                        list_res.append(case_text + '||' + expectedQues + '||' + questionFocus + '||' + tmp_text + '||' + 'Fail')
                elif qa.get(tmp_text):
                    if expectedQues == qa.get(tmp_text).strip():
                        log_tmp.error(case_text.strip() + ' is Pass')
                        list_res.append(case_text + '||' + expectedQues + '||' + questionFocus + '||' + tmp_text + '||' + 'Pass')
                    else:
                        log_tmp.error(case_text.strip() + ' is Fail')
                        list_res.append(case_text + '||' + expectedQues + '||' + questionFocus + '||' + tmp_text + '||' + 'Fail')
                else:
                    log_tmp.error(case_text.strip() + ' is Fail')
                    list_res.append(case_text + '||' + expectedQues + '||' + questionFocus + '||' + tmp_text + '||' + 'Fail')
            else:
                log_tmp.error(case_text.strip() + ' is Fail')
                tmp_text = str(r)
                list_res.append(case_text + '||' + expectedQues + '||' + questionFocus + '||' + str(r) + '||' + 'Fail')
        except BaseException as err:
            list_res.append(case_text + '||' + 'Null' + '||' + questionFocus + '||' + str(err) + '||' + 'Excep')
            log_tmp.error(err)
        finally:
            now_time = int(time.time())
            cost_time = rate_time(begin_time, now_time)
           #log_tmp.error(str(len(list_res)) + '/' + str(all_num) + '|cost time:' + str(cost_time))
    return list_res

def main(courtCaseId,bd,qa,list_res,all_num):
    file_list = os.listdir("./avg_tmp/")
    try:
        p = Pool(len(file_list))
        for z in range(len(file_list)):
            session_id = get_session_id(courtCaseId)
            p.apply_async(auto_test, args=(bd, qa, session_id, file_list[z], list_res, all_num))
        p.close()
        p.join()
    except Exception as err_msg:
        print("main():error mesage=%s" % str(err_msg))
    return list_res

if __name__ == '__main__':


    courtCaseId = localReadConfig.get_req_param('courtCaseId')
    get_courtCase_list = courtCase()
    list_courtCase = get_courtCase_list.courtcase()
    courtCase = list_courtCase[int(courtCaseId)-1].split('||')
    bd = courtCase[1]
    qa = courtCase[2]
    log_tmp.error("案场" + courtCaseId + " prepare....")
    do_case = caseAvg()
    all_num = do_case.case_avg(courtCaseId)
    list_tmp = Manager().list()
    log_tmp.error("test begin")
    main(courtCaseId, bd, qa, list_tmp, all_num)
    log_tmp.error("test done")
    un_bind_res = interface_test.Post(un_bind_url, check_bind_param)
    end = int(time.time())
    if len(list_tmp) > 0:
        test_result(courtCaseId, list_tmp)
        log_tmp.error("案场" + courtCaseId + " save done!")
    else:
        log_tmp.error('nothing save!')
    '''
    for i in range(len(list_courtCase)):
        courtCase = list_courtCase[i].split('||')
        courtCaseId = courtCase[0]
        bd = courtCase[1]
        qa = courtCase[2]
        log_tmp.error("案场" + courtCaseId + " prepare....")
        do_case = caseAvg()
        all_num = do_case.case_avg(courtCaseId)
        list_tmp = Manager().list()
        log_tmp.error("test begin")
        main(courtCaseId,bd,qa,list_tmp,all_num)
        log_tmp.error("test done")
        un_bind_res = interface_test.Post(un_bind_url, check_bind_param)
        end = int(time.time())
        if len(list_tmp) > 0:
            test_result(courtCaseId,list_tmp)
            log_tmp.error("案场" + courtCaseId + " save done!")
        else:
            log_tmp.error('nothing save!')
    '''