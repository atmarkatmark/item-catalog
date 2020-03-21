# coding: utf-8

# pip install beautifulsoup4 requests
from bs4 import BeautifulSoup as bs
import re

import utils

base_url = 'https://www.ankerjapan.com/category/BATTERY/'

def crawl(url:str=base_url):
    '''
        製品の一覧を取得する。
    '''
    data = utils.fetch(url)
    data_list = [data, ]
    soup = bs(data, 'lxml')
    
    # ページの一覧を順番に読み込む
    page_list = list(set([page['href'] for page in soup.find('p', class_='pagelink').find_all('a')]))
    for page in page_list:
        d = utils.fetch(page)
        if d:
            data_list.append(d)

    # item list
    output = []
    for d in data_list:
        soup = bs(d, 'lxml')
        for item in soup.find('div', class_='item_list').ul.find_all('li'):
            item = item.div.span
            # JSON出力用
            o = { 'manufacture': 'Akner' }
            # 製品名、製品画像
            o['name'] = item.a.img['alt']
            o['image'] = item.a.img['src']
            o['url'] = item.a['href']
            o['price'] = int(re.sub(r'\D', '', item.find('p', class_='price').string))
            # 詳細
            o['detail'] = crawl_detail(o['url'])

            output.append(o)

    return output

def crawl_detail(url):
    '''
        製品の詳細を取得する。
    '''
    data = utils.fetch(url)
    soup = bs(data, 'lxml')

    details = {}

    # Amazonへのリンク
    amazon = soup.find('a', class_='to_amazon_button')
    if amazon:
        details['amazon'] = amazon['href']

    # 仕様
    for row in soup.find('div', class_='item_detail_product').find_all('tr'):
        cols = row.find_all('td')
        # 「項目名 | 値」の形式(列が2)でなければスキップ
        if len(cols) != 2:
            continue
        details[cols[0].string] = cols[1].string
    
    return details

if __name__ == '__main__':
    crawl(base_url)
