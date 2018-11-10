#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 09:22:19 2018

@author: liuxixuan
"""
# Current price online
import requests
request = input('Company symbol: ')
response = requests.get('https://api.iextrading.com/1.0/stock/'+request.lower()+'/price')
if response.status_code == 200:
    price = response.json() 

# Personal account
account = {'NetWorth':1000000,
           'Gains':550,
           'Returns':33}
items_account= [account]

# Watchlist
watchlist= {'Symbol':'DJIA',
            'Price':10,
            'CHG':20,
            'CHG %':70}
items_watchlist= [watchlist]

# Portfolio list in CSV file
item = {'Symbol':'AMZN',
        'Shares':100,
        'Cost':5,
        'Price': 2
        }
items_portfolio = [item]
    
 
def add_to_watchlist(items_watchlist, Symbol, Price, CHG, CHG_percent):
    
    item = {'Symbol':Symbol,
            'Price':str(Price),
            'CHG':str(CHG),
            'CHG %':str(CHG_percent)}
    items_watchlist.append(item)


def add_to_portfolio(items_portfolio, Symbol, Shares, Cost, Price):
    
    item = {'Symbol':Symbol,
            'Shares':str(Shares),
            'Cost':str(Cost),
            'Price':str(Price),
            }
    items_portfolio.append(item)  
    
    
def delete_item(listname, Symbol):
    
    for company in listname:
        if company['Symbol'] == Symbol:
            listname.remove(company)      


def write_to_csv(listname, filename):
    
    header = []
    for key in listname[0].keys():
        header.append(key)
    
    all_items=[]
    for item in listname:
        row = []
        for j in item.values():
            row.append(str(j))
        all_items.append(row)
        
    fp = open(filename, mode='w')
    print(','.join(header), file=fp)
    for row in all_items:
            print(','.join(row), file=fp)
    fp.close()    
    

# write_to_csv(items_portfolio,'portfolio.csv')
# add_to_portfolio(items_portfolio, 'aapl', 90, 9, price)
# write_to_csv(items_portfolio,'portfolio.csv')
# delete_item(items_portfolio, 'amzn')
# write_to_csv(items_portfolio,'portfolio.csv')

# write_to_csv(items_watchlist,'watchlist.csv')
# add_to_watchlist(items_watchlist, 'aapl', price, 2, 60)
# write_to_csv(items_watchlist,'watchlist.csv')
# delete_item(items_watchlist, 'aapl')
# write_to_csv(items_watchlist,'watchlist.csv')

# write_to_csv(items_account,'account.csv')