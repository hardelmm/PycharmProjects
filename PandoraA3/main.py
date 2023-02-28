# -*- coding: utf-8 -*-
from ttsRequestClient import *
from asrRequestClient import *
from checkProcess import *
from resultProcess import *
def main():
    case_text_list = []
    case_expectRes_list = []
    case_list = []
    tts_client = TTSRequestClient()
    case_source_list = tts_client.getcaseText()
    asr_client = ASRequestClient()
    res_Process = ResultProcess()
    for x in range(len(case_source_list)):
        do_list = case_source_list[x].split('||')
        case_text = do_list[0]
        case_expectRes = do_list[1]
        audio = tts_client.generateAudio(case_text)
        case_list = [case_text,audio,case_expectRes]
        result_list = asr_client.generateASResult(case_list)
        chc_Process = CheckProcess()
        ret_list = chc_Process.CheckProcess(result_list)
        #print(str(ret_list))
        res_Process.SaveResult(x,ret_list)

if __name__ == '__main__':
    main()






