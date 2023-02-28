# -*- coding: utf-8 -*-
import os
import xlrd
from readConfig import ReadConfig
from log4j import *

localReadConfig = ReadConfig()


class caseAvg:
    def __init__(self):
        self.all_num = 0
        self.thread_num = localReadConfig.get_thread_config("thread_num")
        self.case = localReadConfig.get_case_path('asr_case_path')

    def case_avg(self):#多进行并发执行平均分配用例数目
        list_tmp = []
        case_path = self.case + 'audio_text.xls'#test.xlsx
        case_data = xlrd.open_workbook(case_path)
        table = case_data.sheets()[0]
        clo1 = table.col_values(0, start_rowx=1, end_rowx=None)
        clo2 = table.col_values(1, start_rowx=1, end_rowx=None)
        for x in range(len(clo1)):
            if clo2[x]:#过滤语料为空的数据
                list_tmp.append(clo1[x].strip() + '||' + clo2[x].strip())

        self.line_num_list = len(list_tmp)

        last_case_list = os.listdir("./case_avg/")
        for fileName in last_case_list:
            os.remove("./case_avg/" + fileName)

        if self.line_num_list < int(self.thread_num):
            print("并发数大于用例总数,程序退出")
            exit()


        # 根据并发数分配每个进程的用例数
        case_avg_path = './case_avg/'
        if not os.path.exists(case_avg_path):
            os.mkdir(case_avg_path)
        avg_tmp_list = os.listdir("./case_avg/")
        for i in range(len(avg_tmp_list)):
            os.remove(case_avg_path + avg_tmp_list[i])
        if self.line_num_list % int(self.thread_num) == 0:
            avg_num = self.line_num_list / int(self.thread_num)
            remainder = 0
        else:
            avg_num = self.line_num_list // int(self.thread_num)
            remainder = self.line_num_list % int(self.thread_num)

        case_list = []

        for i in range(int(self.thread_num)):
            if remainder == 0:
                case_list.append(int(avg_num))
            else:
                if i < remainder:
                    case_list.append(int(avg_num) + 1)
                else:
                    case_list.append(int(avg_num))
        # 将每个进程的用例数,写入文件
        min = 0
        for i in range(len(case_list)):
            if i == 0:
                avg_list = list_tmp[0:case_list[i]]
            else:
                min += case_list[i - 1]
                max = min + case_list[i]
                avg_list = list_tmp[min:max]
            avg_file = open(case_avg_path + str(i), 'w+')
            for xx in range(len(avg_list)):
                if xx == len(avg_list) - 1:
                    avg_file.write(str(avg_list[xx]))
                else:
                    avg_file.write(str(avg_list[xx]) + '\n')
            avg_file.close()
        log_tmp.info(len(list_tmp))
        return len(list_tmp)