# -*- coding: utf-8 -*-
# @Time    : 2019/12/16 10:31
# @Author  : huangyl
# @FileName: log4j.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com
import logging

log_format = "%(asctime)s - %(levelname)s - %(message)s"
#logging.basicConfig(filename='run.log',level=logging.DEBUG,format=log_format)
logging.basicConfig(level=logging.ERROR,format=log_format)
log = logging.getLogger()