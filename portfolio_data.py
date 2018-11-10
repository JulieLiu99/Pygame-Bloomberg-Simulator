#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 09:22:19 2018

@author: liuxixuan
"""
# Current price online
import requests
import time

"""
Sample data

"""
"""
# Personal account
account = {'NetWorth':1000000,
           'Cash':550,
           'Gains':33,
           'Returns':7,
           'Short Reserve':23}
items_account= [account]

# Watchlist
watchlist= {'Symbol':'djia',
            'Price':10,
            'CHG':20,
            'CHG %':70}
items_watchlist= [watchlist]

# Portfolio list in CSV file
item = {'Symbol':'aapl',
        'Shares':100,
        'Type':5,
        'Price': 2,
        'Value': 3000
        }
items_portfolio = [item]
"""
"""
items_markets = [{
                    "mic": "TRF",
                    "tapeId": "-",
                    "venueName": "TRF Volume",
                    "volume": 589171705,
                    "tapeA": 305187928,
                    "tapeB": 119650027,
                    "tapeC": 164333750,
                    "marketPercent": 0.37027,
                    "lastUpdated": 1480433817317
                      }]
"""

"""
Write a list to csv file
"""

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
    
"""
Get a list form csv file, all values are string
"""

def get_from_csv(filename):
    item_list = []
    fp = open(filename)
    header = fp.readline().strip().split(',')
    for line in fp:
        row = line.strip().split(',')
        item = {}
        for i in range(len(header)):
            item[header[i]] = str(row[i])
        item_list.append(item)
    fp.close()
    return item_list

"""
Functions for specific values
"""
def get_price(Symbol):
    response = requests.get('https://api.iextrading.com/1.0/stock/'+Symbol.lower()+'/quote')
    if response.status_code == 200:
        dic = response.json()
        return dic['latestPrice']
    
def get_all_price():
    items_portfolio = get_from_csv('portfolio.csv')
    items_watchlist = get_from_csv('watchlist.csv')
    price_dic = {}
    for item in items_portfolio:
        price_dic[item['Symbol']] = get_price(item['Symbol'])
    for item in items_watchlist:
        price_dic[item['Symbol']] = get_price(item['Symbol'])
    return price_dic
    
def get_all_change():
    items_watchlist = get_from_csv('watchlist.csv')
    change_dic = {}
    for item in items_watchlist: 
        response = requests.get('https://api.iextrading.com/1.0/stock/'+item['Symbol'].lower()+'/previous')
        if response.status_code == 200:
            dic = response.json()
            change = dic['change']
            change_percent = dic['changePercent']
            change_dic[item['Symbol']] = [change, change_percent]
    return change_dic

def get_market(): #returns a list of dictionaries
    response = requests.get('https://api.iextrading.com/1.0/market')
    if response.status_code == 200:
        markets = response.json()
        return markets
        
#def AccountValues():
#    
#    networth = 0
#    short_reserve = 0
#    items_portfolio = get_from_csv('portfolio.csv')
#    items_account = get_from_csv('account.csv')
#    for item in items_portfolio:
#        if item['Type'] == 'Buy':
#            item_networth= float(item['Shares']) * float(item['Price'])
#            networth += item_networth
#        elif item['Type'] == 'Sell Short':
#            item_short = float(item['Shares']) * float(item['Price'])
#            short_reserve += item_short
#    for item in items_account:
#        networth += float(item['Cash'])
#    gain = (networth - 100000) / 100000 * 100
#    return_value = networth - 100000
#    account_values = [networth, gain, return_value, short_reserve]
#    return account_values


"""
Make a list of strins from csv file
"""


class To_print():
    
    def __init__(self):
        self.change_dic = get_all_change()
        self.price_dic = get_all_price()
        self.items_portfolio = get_from_csv('portfolio.csv')
        self.items_watchlist = get_from_csv('watchlist.csv')
        
    def portfolio(self):
   
        to_print = [' '*int(38/2) + '[Portfolio]', 'Symbol | Shares | Type | Price | Value'] 
        for item in self.items_portfolio:
            price = self.price_dic[item['Symbol']]
            sep = ' | '
            value = price * float(item['Shares'])
            value = format(value,'.2f')  
            line = item['Symbol'] + sep + item['Shares'] + sep+ item['Type'] + sep+ str(price) + sep+ str(value)
            to_print.append(line)
        return to_print

    def watchlist(self):
        
        to_print = [' '*int(27/2) + '[Watchlist]', 'Symbol | Price | CHG | CHG%'] 
        for item in self.items_watchlist: 
            price = self.price_dic[item['Symbol']]
            change = self.change_dic[item['Symbol']]
            CHG = change[0]
            CHG_percent = change[1]
            sep = ' | '
            line = item['Symbol'] + sep + str(price) + sep+ str(CHG)+ sep+ str(CHG_percent)
            to_print.append(line)
        return to_print

    def account(self):
        networth = 0
        short_reserve = 0
        items_account = get_from_csv('account.csv')
        for item in self.items_portfolio:
            if item['Type'] == 'Buy':
                item_networth= float(item['Shares']) * float(self.price_dic[item['Symbol']])
                networth += item_networth
            elif item['Type'] == 'Sell Short':
                item_short = float(item['Shares']) * float(self.price_dic[item['Symbol']])
                short_reserve += item_short
        for item in items_account:
            networth += float(item['Cash'])
        gain = (networth - 100000) / 100000 * 100
        return_value = networth - 100000
               
        to_print = [' '*int(49/2) + '[Account]', 'NetWorth | Cash | Gains | Returns | Short Reserve']
        networth = format(networth,'.2f')        
        gains = format(gain,'.2f')       
        returns = format(return_value,'.2f')  
        short_reserve = format(short_reserve,'.2f') 
        for item in items_account:
            cash = format(float(item['Cash']),'.2f')  
            sep = ' | '
            line = str(networth) + sep + str(cash) + sep + str(gains)+ sep + str(returns) + sep + str(short_reserve)
            to_print.append(line)
        return to_print  
    
    def markets(self):
        items_market = get_market()
        to_print = [' '*int(44/2) + '[Market Volume]', 'Venue Name | Tape A | Tape B | Tape C | Mkt%'] 
        for item in items_market: 
            sep = ' | '
            line = item['venueName'] + sep + str(item['tapeA']) + sep+ str(item['tapeB']) + sep+ str(item['tapeC']) + sep + str(item['marketPercent'])            
            to_print.append(line)
        return to_print
