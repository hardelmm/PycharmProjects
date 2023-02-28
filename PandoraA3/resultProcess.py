# -*- coding: utf-8 -*-
import time
import xlwt
from readConfig import ReadConfig
class ResultProcess:
    def __init__(self):
        localReadConfig = ReadConfig()
        self.task_name = localReadConfig.get_task_name('name')
        self.run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))
        self.open_excel = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.open_sheet = self.open_excel.add_sheet('Sheet1')

        self.open_sheet.write(0, 0, u'测试语料')
        self.open_sheet.write(0, 1, u'测试音频')
        self.open_sheet.write(0, 2, u'期望res')
        self.open_sheet.write(0, 3, u'实际res')
        self.open_sheet.write(0, 4, u'all_time')
        #self.open_sheet.write(0, 5, u'last_time')
        self.open_sheet.write(0, 5, u'ASR_session')
        self.open_sheet.write(0, 6, u'结果')

    def SaveResult(self,x,ret_list):
        print("保存结果中...")
        case_text = ret_list[0]
        case_audio = ret_list[1]
        res_tmp = ret_list[2]
        expectedRes = ret_list[3]
        time1 = ret_list[4]
        #time2 = ret_list[5]
        time3 = ret_list[5]
        strsession = ret_list[6]
        result = ret_list[7]

        #all_time = round(float(time2) - float(time1), 3) * 1000
        all_time = round(float(time3) - float(time1), 3) * 1000
        run_time = self.run_time
        open_excel = self.open_excel
        open_sheet = self.open_sheet

        open_sheet.write(x + 1, 0, case_text)
        open_sheet.write(x + 1, 1, case_audio)
        open_sheet.write(x + 1, 2, expectedRes)
        open_sheet.write(x + 1, 3, res_tmp)
        open_sheet.write(x + 1, 4, all_time)
        #open_sheet.write(x + 1, 5, last_time)
        open_sheet.write(x + 1, 5, strsession)
        open_sheet.write(x + 1, 6, result)
        open_excel.save('./result/' + self.task_name +'_result_' + str(run_time) + '.xls')
        print("结果保存完成")