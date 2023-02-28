# -*- coding: utf-8 -*-
# @Time    : 2023/2/11 12:50
# @Author  : huangyl
# @FileName: P_Mysql.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

import datetime
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "infosec2015",
    #auth_plugin = "mysql_native_password"
)
#print(mydb)
mycursor = mydb.cursor()
mycursor.execute("show databases")
a = mycursor.fetchall()
mycursor.execute("drop database if exists TestDatabase1")
mycursor.execute("create database TestDatabase1")
print(a)
mycursor.execute("use TestDatabase1")
'''mycursor.execute("create table test2 (id integer auto_increment primary key, name varchar(255), path varchar(255),"
                 "create_time timestamp not null default CURRENT_TIMESTAMP, update_time timestamp not null default "
                 "CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP)")'''
mycursor.execute("create table test2 (id integer auto_increment primary key, case_text varchar(255), expectedRes varchar(255), res_tmp json, res_chk varchar(255), result varchar(255), time timestamp not null default CURRENT_TIMESTAMP)")
time = datetime.datetime.now()
#time = datetime.datetime.strftime('%Y-%m-%d.%H.%M.%S',datetime.datetime.now())
#sql = "INSERT INTO test1 (id, name, path, create_time, update_time) VALUES (%s, %s, %s, %s, %s)"
sql = "insert into test2 (id, case_text, expectedRes, res_tmp, res_chk, result, time) values (%s, %s, %s, %s, %s, %s, %s)"
val = [(1,'路由器密码多少','service=hotel.information;code=QUERY;focus=WIFI;targetType=hotel','{"rc":0,"text":"路由器密码多少","service":"cn.yunzhisheng.hotel.information","code":"QUERY","semantic":{"intent":{"focus":"WIFI","targetType":"hotel"}},"history":"cn.yunzhisheng.hotel.information","responseId":"2cbc923803b749ffb4e7a8a218b628b4","source":"nlu","originIntent":{"nluSlotInfos":[]}}','|service=cn.yunzhisheng.hotel.information=Pass||code=QUERY=Pass||focus=WIFI=Pass||targetType=hotel=Pass|', 'Pass',time)]
print(sql)
print(val)
mycursor.executemany(sql,val)
mydb.commit()
mycursor.execute("select * from test2")
table2 = mycursor.fetchall()
#table1 = mycursor.fetchone()
#table1 = mycursor.fetchmany(2)
for row in table2:
    print(row)
mycursor.close()
mydb.close()


