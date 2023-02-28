# -*- coding: utf-8 -*-
# @Time    : 2023/2/18 19:05
# @Author  : huangyl
# @FileName: dbProcess.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

import time
import mysql.connector
class dbProcess:
    connection = None

    def __int__(self):
        #self.run_time = time.strftime('%Y-%m-%d.%H.%M.%S', time.localtime(time.time()))
        self.connection = None

        '''
        if self.connection is None:
            self.connection = mysql.connector.connect(host=h, user=u, password=p)
            print("DB connect successfully...")
            return self.connection
        else:
            print("DB has been connected...")
        '''

    def get_conn(self, h, u, p):
        if self.connection is None:
            self.connection = mysql.connector.connect(host=h, user=u, password=p)
            print("DB connect successfully...")
            return self.connection
        else:
            print("DB has been connected...")

    def close_conn(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("DB disconnected successfully...")
        else:
            print("DB has been disconnected...")

    def query_sql(self, sql):
        res = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print("DB query excep :" + str(e))
        finally:
            cursor.close()

    def exec_sql(self, sql):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            print("DB execute sql successfully...")
        except Exception as e:
            print(str(e))
            self.connection.rollback()
        finally:
            cursor.close()

    def exec_sqlmany(self, sql, val):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql,val)
            self.connection.commit()
            print("DB execute sql successfully...")
        except Exception as e:
            print(str(e))
            self.connection.rollback()
        finally:
            cursor.close()
