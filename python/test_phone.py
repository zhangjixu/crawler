# -*- coding: utf-8 -*-
# @Time    : 2018/8/1 9:16
# @Author  : zhangjixu

import sys

import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')
DOWNLOAD_URL = 'http://is.snssdk.com/api/news/feed/v85/?fp=TSTqJlXMc2HuFlcbLSU1FYKSLlKW&version_code=6.8.2&app_name=news_article&vid=CFDA34EC-7507-4EA6-8B42-62B674908704&device_id=48306391981&channel=App%20Store&resolution=1242*2208&aid=13&ab_version=304490,261580,271178,424179,357703,377636,326524,326532,415914,409841,419998,429863,239097,420969,170988,424456,405357,432304,374119,409927,425898,430513,431216,276205,426879,430540,429719,396703,277769,431673,431876,381406,416055,431708,426617,426813,378450,423375,432781,425530,323233,415475,423308,419929,411773,423830,345191,427653,430089,424606,430548,431296,423994,424177,415631,214069,432945,423020,419777,424279,419836,430773,429157,432420,280448,425895,281294,371159,353053,325613,422143,295307,357401,432981,420789,386895,431336,430819,427044,432263,424017,419915,430647,425947,428863&ab_feature=201616,z2&ab_group=z2,201616&openudid=1b709cfff178bb816e44f308193720915750a6d0&idfv=CFDA34EC-7507-4EA6-8B42-62B674908704&ac=WIFI&os_version=11.4.1&ssmix=a&device_platform=iphone&iid=39114877791&ab_client=a1,f2,f7,e1&device_type=iPhone%207%20Plus&idfa=7706F05A-DB83-4657-9C60-5A64DA7C6870&language=zh-Hans-CN&support_rn=4&image=1&list_count=34&count=20&tt_from=pull&category=news_tech&city=&last_refresh_sub_entrance_interval=4045&refer=1&refresh_reason=1&concern_id=6215497899594222081&st_time=1054&session_refresh_idx=5&strict=0&LBS_status=deny&detail=1&min_behot_time=1533115980&loc_mode=0&cp=55B36b167dE5Dq1&as=a2c5d7961d75abfe210417&ts=1533115997'
conn = MongoClient('', )
db = conn.test
today_news = db.today_news


def parse_phone(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    datas = json.loads(soup.prettify())
    for data in datas['data']:
        try:
            title = json.loads(data['content'])['share_info']['title']
            url = json.loads(data['content'])['share_info']['share_url']
            # print url, title
            parse_html(url)
        except Exception, e:
            print e.message
            continue


def parse_html(url):
    driver = webdriver.PhantomJS('D:\\soft\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver.get(url)
    print(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find('h1', {'class': 'article-title'})
    json = {'url': url}
    arr = []
    if title is None:
        title = soup.find('h1', {'class': 'question-name'}).get_text().strip()
        answer_items = soup.find_all('div', {'class': 'answer-item'})
        json['title'] = title
        json['flag'] = 'question'
        for answer_item in answer_items:
            try:
                user_name = answer_item.find('a', {'class': 'answer-user-name'}).get_text()
                create_date = answer_item.find('div', {'class': 'answer-user'}).find('a', {
                    'class': 'answer-user-tag'}).string
                user_answer = answer_item.find('div', {'class': 'answer-text-full rich-text'}).get_text()
                arr.append({'user_name': user_name, 'create_date': create_date, 'user_answer': user_answer})
            except Exception, e:
                e
                continue
        json['answer_items'] = arr
    else:
        comment_items = soup.find_all('li', {'class': 'c-item'})
        org = soup.find('div', {'class': 'article-sub'}).find_all('span')[0].string
        release_date = soup.find('div', {'class': 'article-sub'}).find_all('span')[1].string
        # content_list = soup.find('div', {'class': 'article-content'}).find_all('p')
        contents = soup.find('div', {'class': 'article-content'}).get_text()
        # for content in content_list:
        #     contents += content.string + "\n"
        json['title'] = title.get_text()
        json['flag'] = 'news'
        json['org'] = org
        json['release_date'] = release_date
        json['contents'] = contents
        for comment_item in comment_items:
            try:
                user_name = comment_item.find('div', {'class': 'c-user-info'}).get_text()
                create_date = comment_item.find('span', {'class': 'c-create-time'}).string
                user_comment = comment_item.find('p').string
                arr.append({'user_name': user_name, 'create_date': create_date, 'user_comment': user_comment})
            except Exception, e:
                e
                continue
        json['answer_items'] = arr
    operation_mongodb(json)
    print "===================================================="


def operation_mongodb(json):
    try:
        today_news.insert(json)
    except Exception, e:
        print e.message


def main():
    url = DOWNLOAD_URL
    res = requests.get(url)
    res.encoding = 'utf-8'
    while True:
        parse_phone(res)


if __name__ == '__main__':
    main()
    # parse_html('https://www.toutiao.com/a6584711502614233613/')
