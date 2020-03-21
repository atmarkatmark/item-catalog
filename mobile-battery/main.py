# coding: utf-8

import json

import anker
import aukey
import cheero
import ravpower

filename = './data.json'

data = []
data.extend(anker.crawl())
data.extend(aukey.crawl())
data.extend(cheero.crawl())
data.extend(ravpower.crawl())

with open(filename, 'w') as f:
    f.write(json.dumps(data))
