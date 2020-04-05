# coding: utf-8

# pip install beautifulsoup4 requests
from bs4 import BeautifulSoup as bs
import re

import utils

base_url = 'https://cheero.net/category/item/battery/'

def crawl(url:str=base_url):
    '''
        製品の一覧を取得する。
    '''
    data = utils.fetch(url)
    data_list = [data, ]
    soup = bs(data, 'lxml')
    
    # ページの一覧を順番に読み込む
    page_list = list(set([a['href'] for a in soup.find('nav', class_='pagination').ul.find_all('a')]))
    for page in page_list:
        d = utils.fetch(page)
        if d:
            data_list.append(d)

    # item list
    output = []
    for d in data_list:
        soup = bs(d, 'lxml')
        for item in soup.find_all('section'):
            if not item.find('div', class_='_entry-inner') or not item.find('div', class_='_entry-image'):
                continue
            
            o = { 'manufacture': 'cheero' }

            o['name'] = item.find('h2').string.strip()
            o['url'] = item.a['href']
            o['image'] = item.find('img')['data-src']
            o['price'] = int(re.sub(r'\D', '', item.find('p', class_='price').span.string))
            o['detail'] = crawl_detail(item.a['href'])

            # 製品名から容量を推測
            m = re.search(r'([1-9][0-9]*00)mAh', o['name'])
            if m:
                o['capacity'] = int(m.group(1))
            
            # USB PD最大出力の推測
            m = re.search(r'([1-9][0-9]+)W$', o['name'])
            if m:
                o['pd_w'] = int(m.group(1))
            
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
    # cheeroはJavaScriptでの埋め込みなのでBeautifulSoupが使えない
    pat = re.compile(r'https?://amzn\.to/[0-9a-zA-Z]+')
    amazon = list(set([s for s in pat.findall(data)]))
    for a in amazon:
        details['amazon'] = a

    # 仕様
    for h3 in soup.find_all('h3'):
        if h3 and h3.string != 'SPEC':
            continue
        
        for row in h3.find_next_sibling().find_all('div', class_='table_elem'):
            cols = row.find_all('div')
            if len(cols) != 2:
                continue
            
            details[cols[0].string] = cols[1].text
    
    return details

if __name__ == '__main__':
    crawl(base_url)
