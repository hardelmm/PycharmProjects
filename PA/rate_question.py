# -*- coding: utf-8 -*-
import requests
import json
import jsonpath
import time
import xlwt
import os
import xlrd
import uuid

run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))

url = 'http://192.168.3.241:8080/service/iss?appkey=z2r3dwbfhi3kx7wrvvtqgujnkyxe4uawtiyi5cym&city=&ver=3.2&scenario=&appver=&isdialog=True&time=2019-01-09-12:39:17&debug=true&voiceid=&gps=&method=iss.getTalk&dpi=&history=&appsig=E5D986C1AFFA37601E02ADE153F6A8F70BE3C18E&text='
path = './poc.xlsx'

conversation_list1 = []
conversation_list2 = []
conversation_list3 = []
conversation_list4 = []

requests.adapters.DEFAULT_RETRIES = 5


def test_result():
    if len(clo1) > 0:
        open_excel = xlwt.Workbook(encoding='utf-8')
        open_sheet = open_excel.add_sheet('Sheet1')
        open_sheet.write(0, 0, u'问题')
        open_sheet.write(0, 1, u'预期结果')
        open_sheet.write(0, 2, u'返回答案')
        open_sheet.write(0, 3, u'执行结果')
        for excel_line in range(len(conversation_list1)):
            open_sheet.write(excel_line + 1, 0, conversation_list1[excel_line])
            open_sheet.write(excel_line + 1, 1, conversation_list2[excel_line])
            open_sheet.write(excel_line + 1, 2, conversation_list3[excel_line])
            open_sheet.write(excel_line + 1, 3, conversation_list4[excel_line])
        open_excel.save('./auto_test_result_' + run_time + '.xls')


def auto_test(case_text, questionFocus):
    global conversation_list1
    global conversation_list2
    global conversation_list3
    global conversation_list4
    try:
        udid = str(uuid.uuid1())
        case_text = case_text.strip()
        response = requests.get(url + case_text + '&udid=' + udid)
        response.enconding = "utf-8"
        r = json.loads(response.content.decode("utf-8"))
        if jsonpath.jsonpath(r, '$..questionFocus') and jsonpath.jsonpath(r, '$..questionFocus')[0].strip() == questionFocus.strip():
            print(case_text.strip() + ' is Pass')
            conversation_list1.append(case_text)
            tmp_text = str(jsonpath.jsonpath(r, '$..questionFocus')[0])
            conversation_list2.append(questionFocus)
            conversation_list3.append(tmp_text)
            conversation_list4.append('Pass')
        else:
            print(case_text.strip() + ' is Fail')
            conversation_list1.append(case_text)
            tmp_text = str(r)
            conversation_list2.append(questionFocus)
            conversation_list3.append(tmp_text)
            conversation_list4.append('Fail')
    except BaseException as err:
        conversation_list1.append(case_text)
        conversation_list2.append(questionFocus)
        conversation_list3.append(str(err))
        conversation_list4.append('Excep')
        print(case_text)
        print(err)


case_data = xlrd.open_workbook(path)
table = case_data.sheets()[0]
clo1 = table.col_values(0,start_rowx=1, end_rowx=None)
clo2 = table.col_values(1,start_rowx=1, end_rowx=None)
for x in range(len(clo1)):
        auto_test(clo1[x].strip(),clo2[x].strip())
test_result()