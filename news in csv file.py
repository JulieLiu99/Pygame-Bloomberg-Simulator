#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 09:22:19 2018

@author: liuxixuan
"""

# API Demo

import requests
response = requests.get('https://api.iextrading.com/1.0/stock/AAPL/news')
if response.status_code == 200:
    AAPL_news = response.json() #this is a list of dictionaries
    
# CSV file
fp = open('AAPL_news.csv', mode='w')

all_news = []
for item in AAPL_news:
    one_piece = []
    for j in item.values():
        one_piece.append(j)
    all_news.append(one_piece)

for row in all_news:
        print(','.join(row), file=fp)
fp.close()

    