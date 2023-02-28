# -*- coding: utf-8 -*-
# @Time    : 2023/2/12 15:55
# @Author  : huangyl
# @FileName: T_Mysql.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

from Utils.sql_utils.db_Opera import DB_Opera

config_db = ("localhost","root","infosec2015")
querysql = "show databases"
DB_Opera.get_conn(config_db)
res = DB_Opera.query_sql(querysql)
print(res)
exec_sql = "use " + str(res[-1][0])
#print(exec_sql)
DB_Opera.exec_sql(exec_sql)
DB_Opera.close_conn()