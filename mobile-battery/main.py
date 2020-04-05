# coding: utf-8

import json
import re

import anker
import aukey
import cheero
import ravpower

filename = './front/src/assets/data.json'

data = []
data.extend(anker.crawl())
data.extend(aukey.crawl())
data.extend(cheero.crawl())
data.extend(ravpower.crawl())

# item.nameの【】で囲われた部分を取り除く
for i in data:
    i['name'] = re.sub('【.+】', '', i['name'])

# USB PDの判定
for i in data:
    if 'detail' not in i:
        continue
    
    pd = False
    for k, v in i['detail'].items():
        if k and v and ('PD' in k or 'PD' in v):
            pd = True
    
    if pd:
        i['pd'] = True

# jsonに書き出す
with open(filename, 'w') as f:
    f.write(json.dumps(data))
