# -*- coding: utf-8 -*-
# @Time    : 2020/2/13 17:39
# @Author  : huangyl
# @FileName: jsonTool.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

import types

def dict_get(dict, objkey):
    default = 'None'
    tmp = dict
    #print(tmp.items())
    for k,v in tmp.items():
        if k == objkey:
            return k
        else:
            #if type(v) is types.dict:
            if type(v) is type({}):
                ret = dict_get(v, objkey)
                if ret is not default:
                    return objkey
            elif type(v) is type([]):
                for val in v:
                    ret = dict_get(val, objkey)
                    if ret is not default:
                        return ret
    return default

#dict = {"rc":0,"text":"修改家庭地址","service":"cn.yunzhisheng.setting.map","code":"SETTING_EXEC","semantic":{"intent":{"operations":[{"operator":"ACT_MODIFY","operands":"ATTR_LOC_HOME"}]}},"general":{"quitDialog":"true","type":"T","text":"好的主人，已为你。"},"history":"cn.yunzhisheng.setting.map","responseId":"478355d1648c49409b1617fe8e92bdd2"}

#res = dict_get(dict,'operator')
#print(res)