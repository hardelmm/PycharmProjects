# -*- coding: utf-8 -*-
# @Time    : 2023/2/12 15:20
# @Author  : huangyl
# @FileName: db_Opera.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

import mysql.connector

class DB_Opera:
    connection = None
    '''
    def __int__(self,x,y,z):
        if self.connection is None:
            self.connection = mysql.connector.connect(host=x,user=y,password=z)
            print("DB connect successfully...")
            return self.connection
        else:
            print("DB has been connected...")
    '''

    @classmethod
    def get_conn(cls,config_db):
        if cls.connection is None:
            cls.connection = mysql.connector.connect(host=config_db[0],user=config_db[1],password=config_db[2])
            print("DB connect successfully...")
            return cls.connection
        else:
            print("DB has been connected...")


    @classmethod
    def close_conn(cls):
        if cls.connection:
            cls.connection.close()
            cls.connection = None
            print("DB disconnected successfully...")
        else:
            print("DB has been disconnected...")

    @classmethod
    def query_sql(cls,sql):
        res = None
        cursor = None
        try:
            cursor = cls.connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print("DB query excep :" + str(e))
        finally:
            cursor.close()

    @classmethod
    def exec_sql(cls,sql):
        cursor = None
        try:
            cursor = cls.connection.cursor()
            cursor.execute(sql)
            cls.connection.commit()
            print("DB execute sql successfully...")
        except Exception as e:
            print(str(e))
            cls.connection.rollback()
        finally:
            cursor.close()
