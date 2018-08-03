# -*- coding: utf-8 -*-
# @Time    : 2018/7/31 15:36
# @Author  : zhangjixu

import MySQLdb as mysql

db = mysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="test", charset="utf8")
db.autocommit(True)
cursor = db.cursor()


class OperationDb:

    def execute_sql(self, sql):
        try:
            cursor.execute(sql)
        except Exception, e:
            print e.message
            db.rollback()
        finally:
            db.close()
