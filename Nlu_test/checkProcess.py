# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 14:26
# @Author  : huangyl
# @FileName: checkProcess.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

import json
import jsonpath
from tools.log4j import *
from tools.jsonTool import *

class CheckProcess:
    def _getparams(self,case_exp):
        params_dict = {}
        key_words = case_exp.split(";")
        for i in range(len(key_words)):
            key, value = key_words[i].split('=', 1)
            # key = key.lower()
            params_dict[key] = value

        return params_dict

    def _my_obj_pairs_hook(self,lst):
        result = {}
        count = {}
        for key, val in lst:
            if key in count:
                count[key] = 1 + count[key]
            else:
                count[key] = 1
            if key in result:
                if count[key] > 2:
                    result[key].append(val)
                else:
                    result[key] = [result[key], val]
            else:
                result[key] = val
        return result

    def CheckProcess(self,case_res):
        text = case_res[0]
        expect_chk = case_res[1]
        expect = self._getparams(case_res[1])
        ret = case_res[2]
        try:
            act_res = json.loads(ret)
            #act_res = json.loads(ret,object_pairs_hook = self._my_obj_pairs_hook(ret))
            #print(act_res)
            list_key = list(expect.keys())
            #ret_keys = act_res.keys()
            list_res = []
            for x in range(len(list_key)):
                e_k = list_key[x]
                if e_k == 'service':
                    e_v = expect.get(e_k)
                    #if e_k in act_res:
                    if e_k in dict_get(act_res, e_k):
                        #a_v = jsonpath.jsonpath(act_res, '$..' + e_k)[0]
                        a_v = jsonpath.jsonpath(act_res, '$..' + e_k)
                        if '|' in e_v:
                            e_v = e_v.split('|')
                            for i in range(len(e_v)):
                                e_v[i] = 'cn.yunzhisheng.' + e_v[i]
                                #print(e_v[i])
                                #print(a_v)
                                if e_v[i] in a_v:
                                    list_res.append('|' + e_k + '=' + e_v[i] + '=' + 'Pass' + '|')
                                    # exit_flag = 'true'
                                    break
                            else:
                                list_res.append('|' + e_k + '=' + e_v[i] + '=' + 'value错误' + '|')

                        else:
                            e_v = 'cn.yunzhisheng.' + e_v
                            #print(e_v)
                            #print(a_v)
                            #if e_v == a_v:
                            if e_v in a_v:
                                list_res.append('|' + e_k + '=' + e_v + '=' + 'Pass' + '|')
                            else:
                                list_res.append('|' + e_k + '=' + e_v + '=' + 'value错误' + '|')
                                #print("value错误")
                    else:
                        list_res.append('|' + e_k + '=' + e_v + '=' + 'key未匹配' + '|')
                        #print("key未匹配")
                else:
                    e_v = expect.get(e_k)
                    #if e_k in act_res:
                    if e_k in dict_get(act_res, e_k):
                        # a_v = jsonpath.jsonpath(act_res, '$..' + e_k)[0]
                        a_v = jsonpath.jsonpath(act_res, '$..' + e_k)
                        #a_v = ",".join(a_v)
                        a_v = ",".join('%s' % id for id in a_v)
                        if '|' in e_v:
                            e_v = e_v.split('|')
                            #exit_flag = 'false'
                            for i in range(len(e_v)):
                                #print(e_v[i])
                                #print(a_v)
                                # if e_v == a_v:
                                #a_v = ",".join(a_v)
                                print(a_v)
                                print(e_v[i])
                                if e_v[i] in a_v:
                                    list_res.append('|' + e_k + '=' + e_v[i] + '=' + 'Pass' + '|')
                                    #exit_flag = 'true'
                                    break
                            else:
                                list_res.append('|' + e_k + '=' + e_v[i] + '=' + 'value错误' + '|')
                                # print("value错误")
                                #if exit_flag == 'true':
                                #   break
                        else:
                            # if e_v == a_v:
                            if e_v == 'notNull':
                                list_res.append('|' + e_k + '=' + e_v + '=' + 'Pass' + '|')
                            elif str(e_v) in str(a_v):
                                list_res.append('|' + e_k + '=' + e_v + '=' + 'Pass' + '|')
                            else:
                                list_res.append('|' + e_k + '=' + e_v + '=' + 'value错误' + '|')
                                # print("value错误")
                    else:
                        list_res.append('|' + e_k + '=' + e_v + '=' + 'key未匹配' + '|')
                        #("key未匹配")
            print(list_res)

            for y in range(len(list_res)):
                ls = list_res[y].strip('|').split('=')
                if ls[2] != 'Pass':
                    result = [text,expect_chk,ret,list_res,'Fail']
                    break
                else:
                    result = [text,expect_chk,ret,list_res,'Pass']
            return result
        except BaseException as err:
            print(err)