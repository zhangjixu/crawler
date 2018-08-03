# _*_ coding=utf-8 _*_

import sys
import requests
from bs4 import BeautifulSoup
import time
import MySQLdb as mysql

reload(sys)
sys.setdefaultencoding('utf-8')
DOWNLOAD_URL = 'https://search.51job.com/list/020000,000000,0000,32,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='


def parse51_html(html):
    db = mysql.connect(host="127.0.0.1", port=3306, user="", passwd="", db="test", charset="utf8")
    cursor = db.cursor()

    soup = BeautifulSoup(html.text, 'html.parser')
    # 职业列表
    job_name_soup = soup.find('div', attrs={'id': 'resultList'})
    job_name_list = []
    for job_name_li in job_name_soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['el']):
        try:
            del job_name_list[:]
            url = job_name_li.find('p').find_all('span')[0].find('a')['href']
            job_name = job_name_li.find('span').find('a')['title']
            company_name = job_name_li.find('span', attrs={'class': 't2'}).get_text()
            comyany_contacts = parse_company_info(url)
            job_address = job_name_li.find('span', attrs={'class': 't3'}).get_text()
            job_salary = job_name_li.find('span', attrs={'class': 't4'}).get_text()
            release_date = job_name_li.find('span', attrs={'class': 't5'}).get_text()
            job_name_list.append(job_name)
            job_name_list.append(company_name)
            job_name_list.append(comyany_contacts)
            job_name_list.append(job_address)
            job_name_list.append(job_salary)
            job_name_list.append(release_date)

            sql = "insert into 51job(`job_name`, `company_name`, `company_contacts`, `job_address`, `job_salary`, `release_date`) values('" + \
                  job_name_list[0] + "','" + job_name_list[1] + "','" + job_name_list[2] + "','" + \
                  job_name_list[3] + "','" + job_name_list[
                      4] + "','" + job_name_list[5] + "')"

            print(sql)

            try:
                cursor.execute(sql)
                db.commit()
            except Exception, e:
                print e.message
                db.rollback()

            time.sleep(0.02)
        except Exception, e:
            print(e.message)
            continue

    db.close()

    # 下一页链接
    next_page = soup.find('div', attrs={'class': 'dw_page'}).find('div', attrs={'class': 'p_wp'}).find('div', attrs={
        'class': 'p_in'}).find('ul').find_all('li', attrs={'class': 'bk'})[1].find('a')
    if next_page:
        return next_page['href']
    return next_page


def parse_company_info(url):
    res = requests.get(url)
    res.encoding = 'gb18030'
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        comyany_contacts = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['bmsg', 'inbox']).find(
            'p').get_text()
        if comyany_contacts is not None:
            comyany_contacts = comyany_contacts.strip()
        return comyany_contacts
    except Exception, e:
        print e.message, url


def main():
    url = DOWNLOAD_URL
    while True:
        res = requests.get(url)
        res.encoding = 'gb18030'
        url = parse51_html(res)


if __name__ == '__main__':
    main()
