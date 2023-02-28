# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 11:20
# @Author  : huangyl
# @FileName: main.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com


from readConfig import *
from readCase import *
from nluRequestClient import *
from checkProcess import *
from resultProcess import *
from sendEmail import *

def main():
    localReadConfig = ReadConfig()
    case_path = localReadConfig.get_path('case_path')
    sender_name = localReadConfig.get_email('sender_name')
    sender_pass = localReadConfig.get_email('sender_pass')
    receiver_name = localReadConfig.get_email('receiver_name')
    send_switch = localReadConfig.get_email('send_switch')
    saveDb_switch = localReadConfig.get_sql('Db_switch')
    db_host = localReadConfig.get_sql('host')
    db_user = localReadConfig.get_sql('user')
    db_password = localReadConfig.get_sql('password')
    #case_path = './case/NluCase.xlsx'
    act_case = readXld(case_path)
    act_req = NluRequestClient()
    act_check = CheckProcess()
    act_result = ResultProcess()
    case_list, versionNoList = act_case.readFileMuti()

    for i in range(len(versionNoList)):
        act_result.CreateS(versionNoList[i])
        result_tablename = act_result.CreateResultTb(versionNoList[i])
        for z in range(len(case_list[i])):
            ret = act_req.generateNLUresult(case_list[i][z])
            res= act_check.CheckProcess(ret)
            act_result.SaveResult(z, res)
            act_result.SaveDb(z,result_tablename,res)
    act_result.CloseDb()


    if send_switch == "YES":
        result_filename = act_result.get_result_filename()
        act_mail = SendEmail(sender_name,sender_pass)
        ret = act_mail.sendMail(receiver_name, result_filename)
        print(ret)
    elif send_switch == "NO":
        print("")
    else:
        print("邮件配置参数错误！")

if __name__ == '__main__':
    main()
