# coding: utf-8

# pip install beautifulsoup4 requests
from bs4 import BeautifulSoup as bs
import re

import utils

base_url = 'https://www.ravpower.jp/product-category/battery'

def crawl(url:str=base_url):
    '''
        製品の一覧を取得する。
    '''
    data = utils.fetch(url)
    data_list = [data, ]
    soup = bs(data, 'lxml')
    
    # ページの一覧を順番に読み込む
    page_list = list(set([a['href'] for a in soup.find('ul', class_='page-numbers').find_all('a', class_='page-numbers')]))
    for page in page_list:
        d = utils.fetch(page)
        if d:
            data_list.append(d)

    # item list
    output = []
    for d in data_list:
        soup = bs(d, 'lxml')
        for item in soup.find('ul', class_='products').find_all('li'):
            if not item.find('div', class_='product_details'):
                continue
            
            o = { 'manufacture': 'RAVPower' }
            o['name'] = item.find('h3').string.strip()
            o['url'] = item.find('a', class_='product_item_link')['href']
            o['image'] = item.find('img')['src']
            o['detail'] = crawl_detail(item.a['href'])
            
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
    for a in soup.find('div', class_='woocommerce-product-details__short-description').find_all('a'):
        if a['href'].startswith('https://www.amazon.co.jp/'):
            details['amazon'] = a['href']

    # 仕様
    for p in soup.find_all('p') + soup.find_all('li'):
        if (p.text.find('：') != -1 or p.text.find(': ') != -1)and p.text.find('、') == -1 and p.text.find('。') == -1:
            for s in p.text.splitlines():
                # 1回半角':'で切って、駄目なら全角'：'で切ってみる
                cols = s.split(':')
                if len(cols) != 2:
                    cols = s.split('：')
                # それでも駄目なら飛ばす
                if len(cols) != 2:
                    continue
                
                # 空文字列も飛ばす
                if len(cols[1].strip()) == 0:
                    continue

                details[cols[0].strip()] = cols[1].strip()
    
    return details

if __name__ == '__main__':
    crawl(base_url)
