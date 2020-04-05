# coding: utf-8

# pip install beautifulsoup4 requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import re

import utils

base_url = 'https://jp.aukey.com/list/index/id/57'

def crawl(url:str=base_url):
    '''
        製品の一覧を取得する。
    '''
    data = utils.fetch(url)
    
    soup = bs(data, 'lxml')
    output = []
    for item in soup.find_all('div', class_='uk-margin-bottom'):
        o = { 'manufacture': 'Aukey' }
        # 型番、製品名
        for p in item.div.find_all('p'):
            if p.find('a'):
                o['name'] = p.a.string
            else:
                o['model'] = p.string
        # 画像、URL
        item = item.figure
        parsed = urlparse(url)
        detail_url = '{}://{}{}'.format(parsed.scheme, parsed.hostname, item.a['href'])
        o['detail'] = crawl_detail(detail_url)
        o['image'] = item.a.img['src']

        # 製品名から容量を推測
        m = re.search(r'([1-9][0-9]*00)mAh', o['name'])
        if m:
            o['capacity'] = int(m.group(1))

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
    amazon = soup.find('div', class_='menu')
    if amazon:
        amazon = amazon.find('div', class_='item')
        if amazon:
            details['amazon'] = amazon['data-value']

    # 仕様
    for h2 in soup.find_all('h2'):
        if h2.string != '製品仕様':
            continue
        
        for row in h2.find_next_sibling().find_all('li'):
            cols = row.find_all('span')
            if len(cols) != 2:
                continue
            details[cols[0].string] = cols[1].string
    
    return details

if __name__ == '__main__':
    crawl(base_url)
