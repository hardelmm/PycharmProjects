# -*- coding: utf-8 -*-
# @Time    : 2019/12/04 17:42
# @Author  : huangyl
# @FileName: UnitConversion_test.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


from tools.log4j import *
from readConfig import ReadConfig
import requests
import json
import jsonpath
import xlwt
import xlrd
import itertools
import time

localReadConfig = ReadConfig()
url = localReadConfig.get_url('url')
appkey = localReadConfig.get_header('appkey')
udid = localReadConfig.get_header('udid')
ver = localReadConfig.get_header('ver')
method = localReadConfig.get_header('method')
appsig = localReadConfig.get_header('appsig')
#case_path = localReadConfig.get_case_path('case_path')
result_path = localReadConfig.get_path('result_path')

def getcase(input_path):
    list_case = []
    case_data = xlrd.open_workbook(input_path)
    for i in range(len(case_data.sheets())):
        table = case_data.sheets()[i]
        case = table.col_values(0, start_rowx=0, end_rowx=None)  # 语料
        list_case.append(case)
    #print(list_case)
    return list_case

def generateText(testA,testB):
    text = '一' + testA + '等于多少' + testB
    return text

def generateNLUresult(caseText):
    full_url = (url + '?appkey=' + appkey + '&udid=' + udid + '&ver=' + ver + '&method=' + method + '&appsig=' + appsig + '&text=' + caseText)
    print(full_url)
    #case_res = []
    try:
        ret = requests.get(full_url).text
        #print(str(ret))
    except Exception as e:
        print(e)
        ret = '请求异常！'
    case_res = [caseText,ret]
    #case_res.append([caseText, ret])
    #print(case_res)
    return case_res

def actProcess(case_res):
    textS = case_res[0]
    ret = case_res[1]
    try:
        act_res = json.loads(ret)
        textR = act_res["general"]["text"]
        result = [textS,ret,textR]
    except BaseException as err:
        print(err)
    return result

def resultProcess(x,i,result):

    case_text = result[0]
    res = result[1]
    Ans = result[2]

    open_sheet.write(i+1, 0, case_text)
    open_sheet.write(i+1, 2, res)
    open_sheet.write(i+1, 1, Ans)
    open_excel.save('./result/' + 'NLU_result_' + str(run_time) +  '.xls')

def singleMain(x):
    #ls = itertools.combinations(list_case[x], 2)
    ls = itertools.permutations(list_case[x],2)
    i = 0
    for l in ls:
        testA = l[0]
        testB = l[1]
        caseText = generateText(testA, testB)
        case_res = generateNLUresult(caseText)
        result = actProcess(case_res)
        resultProcess(x,i, result)
        i += 1

if __name__ == '__main__':
    case_path = './case/unitCase.xlsx'
    list_case = getcase(case_path)
    run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))
    open_excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
    for i in range(len(list_case)):
        open_sheet = open_excel.add_sheet('Sheet'+str(i))
        open_sheet.write(0, 0, u'语料')
        open_sheet.write(0, 2, u'实际res')
        open_sheet.write(0, 1, u'答案')
        singleMain(i)




