# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 15:31
# @Author  : zhangjixu

from pymongo import MongoClient

conn = MongoClient('192.168.23.204', 20001)
db = conn.test
today_news = db.today_news


def operation_mongodb():
    users = [{"name": "zhangsan", "age": 18}, {"name": "lisi", "age": 20}]
    today_news.insert(users)


if __name__ == '__main__':
    operation_mongodb()
