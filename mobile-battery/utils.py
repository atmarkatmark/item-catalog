# coding: utf-8

import requests
import os
import base64
from hashlib import sha1

def load_cache(path: str):
    '''
        pathを読み込み、内容を返す。
        ファイルがない場合はNoneを返す。
    '''
    cache = None
    with open(path, 'r', encoding='utf-8') as f:
        cache = f.read()
    return cache

def save_cache(path, data: bytearray):
    '''
        pathにdataを書き出す。
    '''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)

def fetch(url:str, cache_dir:str='cache'):
    '''
        urlをGETした内容を返す。
        cache_dirにキャッシュがあったらそれを換える。
    '''
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    cache_path = os.path.join(cache_dir, sha1(url.encode('utf-8')).hexdigest())

    data = None
    # キャッシュがあったらキャッシュを読み込む
    if os.path.exists(cache_path):
        data = load_cache(cache_path)
    # キャッシュがなかったらリモートから取得する
    else:
        res = requests.get(url, verify=False)
        data = res.text
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(data)
    
    return data
