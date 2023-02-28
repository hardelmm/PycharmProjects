# -*- coding: utf-8 -*-
import json
import string
from tools.log4j import *

class CheckProcess:
    def CheckProcess(self,result_list):
        try:
            case_text = result_list[0]
            case_audio = result_list[1]
            res_tmp = result_list[2]
            #print(res_tmp)
            expectedRes = result_list[3]
            time1 = result_list[4]
            #time2 = result_list[5]
            time3 = result_list[5]
            strsession = result_list[6]
            exp_res = json.loads(expectedRes)
            act_res = json.loads(res_tmp)
            #print(act_res)
            if act_res['asr_recongize'].replace(" ", "").replace("，", "") == exp_res['asr_recongize'].replace(" ", "").replace("，", ""):
                if act_res['code'] == exp_res['code']:
                    if act_res['service'] == exp_res['service']:
                        if act_res['general']['text'].replace(" ", "") == exp_res['general']['text'].replace(" ", ""):
                            ret_list = [case_text, case_audio, res_tmp, expectedRes, time1, time3, strsession, "pass"]
                            log.info(case_text + ' ===> ' + 'pass')
                        else:
                            ret_list = [case_text, case_audio, res_tmp, expectedRes, time1, time3, strsession,"fail"]
                            log.info(case_text + ' ===> ' + 'fail')
                    else:
                        ret_list = [case_text, case_audio, res_tmp, expectedRes, time1, time3, strsession, "fail"]
                        log.info(case_text + ' ===> ' + 'fail')
                else:
                    ret_list = [case_text, case_audio, res_tmp, expectedRes, time1, time3, strsession, "fail"]
                    log.info(case_text + ' ===> ' + 'fail')
            else:
                ret_list = [case_text, case_audio, res_tmp, expectedRes, time1, time3, strsession, "fail"]
                log.info(case_text + ' ===> ' + 'fail')
        except BaseException as err:
            ret_list = [case_text, case_audio, res_tmp, expectedRes, time1, time3, strsession, "fail"]
            print(err)
        return ret_list
