# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 13:51
# @Author  : huangyl
# @FileName: checkProcess.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


import time
import datetime
import xlwt
from dbProcess import *
from readConfig import *


class ResultProcess:
    localReadConfig = ReadConfig()
    saveDb_switch = localReadConfig.get_sql('Db_switch')
    db_host = localReadConfig.get_sql('host')
    db_user = localReadConfig.get_sql('user')
    db_password = localReadConfig.get_sql('password')

    def __init__(self):
        self.run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))
        self.time = datetime.datetime.now()
        self.open_excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.result_filename = 'NLU_result_' + str(self.run_time) + '.xls'
        if self.saveDb_switch == "YES":
            self.dbc = dbProcess()
            self.dbc.get_conn(self.db_host,self.db_user,self.db_password)

    def CreateS(self, SheetName):
        self.open_sheet = self.open_excel.add_sheet(SheetName)
        self.open_sheet.write(0, 0, u'测试语料')
        self.open_sheet.write(0, 1, u'期望结果')
        self.open_sheet.write(0, 2, u'实际res')
        self.open_sheet.write(0, 3, u'校验结果')
        self.open_sheet.write(0, 4, u'结果')

    def SaveResult(self, x, ret_list):
        # print("保存结果中...")
        case_text = ret_list[0]
        expectedRes = ret_list[1]
        res_tmp = ret_list[2]
        res_chk = ret_list[3]
        result = ret_list[4]

        run_time = self.run_time
        open_excel = self.open_excel
        open_sheet = self.open_sheet

        open_sheet.write(x + 1, 0, case_text)
        open_sheet.write(x + 1, 1, expectedRes)
        open_sheet.write(x + 1, 2, res_tmp)
        open_sheet.write(x + 1, 3, res_chk)
        open_sheet.write(x + 1, 4, result)
        self.open_excel.save('./result/' + self.result_filename)

        # print("结果保存完成")

    def get_result_filename(self):
        return self.result_filename

    def CreateResultTb(self, versionNo):
        result_tablename = 'NLU_result_' + versionNo + '_' + str(self.time)
        print(result_tablename)
        exec_sql = "create table `" + result_tablename + "` (id integer auto_increment primary key, case_text varchar(255), expectedRes varchar(255), res_tmp json, res_chk varchar(255), result varchar(255), time timestamp not null default CURRENT_TIMESTAMP)"
        #print(exec_sql)
        self.dbc.exec_sql("use TestDatabase1")
        self.dbc.exec_sql(exec_sql)
        return result_tablename

    def SaveDb(self, x, result_tablename, ret_list):
        # print("保存结果中...")
        case_text = ret_list[0]
        expectedRes = ret_list[1]
        res_tmp = ret_list[2]
        res_chk = ret_list[3]
        result = ret_list[4]
        sql = "insert into `" + result_tablename + "` (id, case_text, expectedRes, res_tmp, res_chk, result, time) values (%s, %s, %s, %s, %s, %s, %s)"

        val = [(x, case_text, expectedRes, res_tmp, str(res_chk), result, self.time)]
        print(sql)
        print(val)
        self.dbc.exec_sqlmany(sql, val)

    def CloseDb(self):
        self.dbc.close_conn()
