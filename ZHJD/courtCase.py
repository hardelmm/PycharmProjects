# -*- coding: utf-8 -*-
import xlrd
import sys
from log4j import *
from readConfig import ReadConfig
#reload(sys)                      # reload 才能调用 setdefaultencoding 方法
#sys.setdefaultencoding('utf-8')   # 设置 'utf-8'

localReadConfig = ReadConfig()

class courtCase:
    def __init__(self):
        self.all_num = 0
        self.case = localReadConfig.get_case_path('ivn_courtcase_path')

    def courtcase(self):
        list_courtCase = []
        path = './case/' + self.case
        case_data = xlrd.open_workbook(path)
        table = case_data.sheets()[0]
        clo1 = table.col_values(0, start_rowx=1, end_rowx=None)#案场ID
        clo2 = table.col_values(1, start_rowx=1, end_rowx=None)#bd
        clo3 = table.col_values(2, start_rowx=1, end_rowx=None)#qa
        for x in range(len(clo1)):
            list_courtCase.append(str(clo1[x]).strip() + '||' + str(clo2[x]).strip() + '||' + str(clo3[x]).strip())
            #log_tmp.error(str(clo1[x]))
            #log_tmp.error(str(clo2[x]))
            #log_tmp.error(str(clo3[x]))
        return list_courtCase