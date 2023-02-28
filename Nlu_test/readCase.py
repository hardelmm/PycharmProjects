# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 12:05
# @Author  : huangyl
# @FileName: readCase.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


import os
import io
import xlrd
from tools.log4j import *
from readConfig import ReadConfig

localReadConfig = ReadConfig()
class ReadCase:
    def __init__(self):
        #self.filename = filename
        self.all_num = 0
        self.thread_num = '2'

    def add_case(self, domain):
        ''' 打开用例文件, 添加用例到domain.case_list.'''
        for ln in open(domain.case_file):
            ln_strip = ln.strip()
            if not ln_strip or ln_strip.startswith('#'):
                # skip注释&空行
                continue
            else:
                self._add_to_case_list(domain, ln)

    #def make_case(self,list_tmp):


class readXld:
    def __init__(self,input_path):
        self.input_path = input_path
    def readFile(self):
        list_tmp = []
        case_data = xlrd.open_workbook(self.input_path)
        table = case_data.sheets()[1]
        clo1 = table.col_values(0, start_rowx=1, end_rowx=None)#语料
        clo2 = table.col_values(1, start_rowx=1, end_rowx=None)#预期结果
        for i in range(len(clo1)):
            if clo1[i]:
                list_tmp.append(clo1[i].strip() + '||' + clo2[i].strip())
        return list_tmp

    def readFileMuti(self):
        list_case = []
        list_tmp = []
        case_data = xlrd.open_workbook(self.input_path)
        sheet_names = case_data.sheet_names()
        for i in range(len(sheet_names)):
            table = case_data.sheet_by_name(sheet_names[i])
            clo1 = table.col_values(0, start_rowx=1, end_rowx=None)  # 语料
            clo2 = table.col_values(1, start_rowx=1, end_rowx=None)  # 预期结果
            for i in range(len(clo1)):
                if clo1[i]:
                    list_tmp.append(clo1[i].strip() + '||' + clo2[i].strip())
            list_case.append(list_tmp)
        return list_case,sheet_names


    def readFile2(self):
        list_tmp = []
        case_data = xlrd.open_workbook(self.input_path)
        table1 = case_data.sheets()[5]
        #table2 = case_data.sheets()[1]
        clo1 = table1.col_values(0, start_rowx=1, end_rowx=None)#语料
        clo2 = table1.col_values(1, start_rowx=1, end_rowx=None)#预期结果
        #clo3 = table2.col_values(0, start_rowx=1, end_rowx=None)#语料
        #clo4 = table2.col_values(1, start_rowx=1, end_rowx=None)#预期结果
        for i in range(len(clo1)):
            if clo1[i]:
                list_tmp.append('cmd_exit_dialog' + '||' + 'text=cmd_exit_dialog')
                #list_tmp.append('常用地址设定下' + '||' + 'service=setting.map;operator=ACT_SET;operands=ATTR_LOC_COMMON')
                #list_tmp.append('我要设置公司地址' + '||' + 'service=setting.map;operator=ACT_SET;operands=ATTR_LOC_OFFICE')
                list_tmp.append('我要设置家里地址' + '||' + 'service=setting.map;operator=ACT_SET;operands=ATTR_LOC_HOME')
                list_tmp.append(clo1[i].strip() + '||' + clo2[i].strip())
                #list_tmp.append('我想把常用地址设置为新研大厦' + '||' + 'service=setting.map;confirm=TRUE;operator=ACT_SET;operands=ATTR_LOC_COMMON;value=新研大厦')
                #list_tmp.append('公司地址设置为新研大厦' + '||' + 'service=setting.map;confirm=TRUE;operator=ACT_SET;operands=ATTR_LOC_OFFICE;value=新研大厦')
                #list_tmp.append('我家的地址在新研大厦' + '||' + 'service=setting.map;confirm=TRUE;operator=ACT_SET;operands=ATTR_LOC_HOME;value=新研大厦')
                #list_tmp.append(clo3[i].strip() + '||' + clo4[i].strip())
                #print(list_tmp)
        return list_tmp


'''
if __name__ == '__main__':
    case_path = './case/FreqUsedAdd.xlsx'
    dd = readXld(case_path)
    dd.readFile2()
'''



