# _*_ coding=utf-8 _*_
import codecs
import requests
from bs4 import BeautifulSoup
import time

from python.OperationDb import OperationDb

DOWNLOAD_URL = 'https://movie.douban.com/top250?start=0'


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }).content


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 电影列表
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    for movie_li in movie_list_soup.find_all('li'):
        movie_name = movie_li.find('span', attrs={'class': 'title'}).get_text()
        movie_info = movie_li.find('div', attrs={'class': 'bd'}).find('p').get_text()
        movie_star = movie_li.find('span', attrs={'class': 'rating_num'}).get_text()
        movie_name_list.append(movie_name)
        movie_name_list.append(movie_info)
        movie_name_list.append(movie_star)
        print(movie_name)
        print(movie_info)
        print(movie_star)
        # time.sleep(2)

    # 下一页链接
    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, next_page


def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb', encoding='utf-8') as f:
        while True:
            html = download_page(url)
            movies, url = parse_html(html)
            f.write(u'{movies}\n'.format(movies='\n'.join(movies)))


if __name__ == '__main__':
    main()
