#-*- coding=utf-8 -*-
from multiprocessing import Pool, Manager
from TTSClient import *
from ResultProcess import *
from case_avg import *
from readConfig import *
def main(list_res):

    ttsclient  = TTSClient()
    file_list = os.listdir("./avg_tmp/")
    try:
        p = Pool(len(file_list))
        # log_tmp.error(len(file_list))
        for z in range(len(file_list)):
            p.apply_async(ttsclient.ttsclient_main, args=(file_list[z],list_res))
        p.close()
        p.join()
    except Exception as err_msg:
        print("main():error mesage=%s" % str(err_msg))
    return list_res

if __name__ == '__main__':
    i = 0
    print('start..')
    #list_tmp = courtcase()
    localReadConfig = ReadConfig()
    input_path = localReadConfig.get_path("case_path")
    result_path = localReadConfig.get_path("result_path")
    thread_num = localReadConfig.get_thread_config("thread_num")
    all_num = case_avg(input_path, i, thread_num)
    list_tmp = Manager().list()
    main(list_tmp)
    ResultProcessc = ResultProcess(i)
    ResultProcessc.SaveResult(list_tmp)
    print('done..')