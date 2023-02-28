# -*- coding: utf-8 -*-
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

    def case_avg(self,list_tmp):
        file_list = os.listdir('./avg_tmp/')
        for fileName in file_list:
            os.remove('./avg_tmp/' + fileName)

        self.line_num_list = len(list_tmp)
        if self.line_num_list < int(self.thread_num):
            print("并发数大于用例总数,程序退出")
            exit()

        # 根据并发数分配每个进程的用例数
        case_avg_path = './avg_tmp/'
        if not os.path.exists(case_avg_path):
            os.mkdir(case_avg_path)
        avg_tmp_list = os.listdir("./avg_tmp/")
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

            #log_tmp.error(avg_list)
            avg_file = io.open(case_avg_path + str(i), 'w+', encoding='UTF-8')
            for xx in range(len(avg_list)):
                if xx == len(avg_list) - 1:
                    avg_file.write(avg_list[xx])
                else:
                    avg_file.write(avg_list[xx] + '\n')
                #log_tmp.error(str(avg_list[xx]))
            avg_file.close()
        return len(list_tmp)

class readTxt:
    def __init__(self,input_path):
        self.input_path = input_path
    def readFile(self):
        with open(self.input_path,'rb') as f:
            data = f.read()
            list_tmp = data.decode().split('\n')#按行分割或用splitlines()
            f.close()
        print(str(list_tmp))
        return list_tmp


class readXld:
    def __init__(self,input_path):
        self.input_path = input_path
    def readFile(self):
        list_tmp = []
        case_data = xlrd.open_workbook(self.input_path)
        table = case_data.sheets()[0]
        clo1 = table.col_values(0, start_rowx=1, end_rowx=None)#语料
        clo2 = table.col_values(1, start_rowx=1, end_rowx=None)#预期结果
        for i in range(len(clo1)):
            list_tmp.append(clo1[i].strip() + '||' + clo2[i].strip())
        return list_tmp
