#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 16:22:15 2018

@author: enshucheng
"""

# #Trade: get the stock information, 
#get the order information from the system input, write the order information in the portfolio csv file
#
'''
Info 
essentially, Info Panel is a window that displays all the information of the company 
the company displayed is decided by the user input/ or carried from the portfolio trading page upon interaction with the trading button
Information includes: Company's name, recent price, price chart (pyplot),

Main loop:
    main block should only consist of conditions that lead to specific functions so that the functions are only run upon demand
    moreover, methods should be used to change variables or update parts of the screen
    the screen should never be updated entirely unless a different panel is being shown 
    while True:
        for event....
        
        if info is requested:
            input(....)
            info(input(..))\
        if trade is requested:
            input()
            trade()
'''
# Trading Panel Base Code
import portfolio_data
import json
import datetime
import requests
def get_price(symbol): # get the current price, return only a float
    url = 'https://api.iextrading.com/1.0/stock/'
    url_b = '/price'
    f_url = url + str(symbol) + url_b
    r = requests.get(f_url)
    r= r.json()
    return r
    
class Order:
    def __init__(self, symbol):
        self.shares = 1
        self.term = 'Day Order'
        self.symbol = symbol
        self.price = 1.0
        self.final_price = False
        self.commission = 10 #default commission fee for every order made
        self.price_type = 'Market'
        self.order_type = 'Buy'
        self.tstamp = ''
        self.status = False # True: executed, False: pending
        self.cost = 0
        self.shortreserve = 0
    def getSymbol_Price(self): # a method to get the wanted symbol to execute transaction
        if self.symbol == '':
            self.symbol = input('[Trade] Please Enter the company symbol: ')
        self.price = get_price(self.symbol)
    
    def getTerm(self): # to get the wanted trading term, basically set self.term to either day order or good till cancelled
        t = ['Day Order', 'Good Till Cancelled']
        number = int(input('Please choose the order term [0: Day Order; 1: Good Till Cancelled]: '))
        self.term = t[number]
    
    def getShares(self):
        self.shares = int(input('How many shares do you wish to trade [Enter an integer]: '))
    
    def getOrderType(self):
        t= ['Buy', 'Sell Short', 'Sell', 'Buy to Cover']
        number = int(input('Please Choose the Order Type [0: Buy; 1: Sell Short; 2: Sell; 3: Buy to Cover]: '))
        self.order_type = t[number]
        
    def getPriceType(self):
        t = ['Market', 'Limit', 'Stop']
        number = int(input('Please Choose the Price Type [0: Market Price; 1: Limit Order; 2: Stop Order]'))
        self.price_type = t[number]
    def display(self):
        print(
            self.shares,self.term,self.symbol,self.price, self.commission, self.price_type, self.order_type, self.final_price,self.status
                )
    def getTime(self):
        self.tstamp = str(datetime.datetime.now())
def getTradingStatus(symbol):
    url = 'https://api.iextrading.com/1.0/deep/trading-status?symbols='
    f_url = url + str(symbol)
    r = requests.get(f_url)
    r= r.json()
    return r


#Write Account: update the capital, deal with the payment
def writeAccount(order):
    fp = open('account.csv','r')
    header = fp.readline().strip().split(',')
    account = fp.readline().strip().split(',')
    fp.close()
    account_d = {}
    for i in range(len(header)):
        key = header[i]
        value= account[i]
        account_d[key] = value
    # account_d has the values
    if order.order_type != 'Sell Short':
        account_d['NetWorth'] = float(account_d['NetWorth'])
        account_d['NetWorth'] -= float(order.cost)
    account_l = [account_d]
    portfolio_data.write_to_csv(account_l, 'account.csv')
    
    
    
    '''
    This module is not working, the order went through but it is not reflected on the portfolio.csv
    
    
    '''
# Portfolio Update
def PortfolioUpdate(order):
    fp = open('portfolio.csv','r')
    header = fp.readline().strip().split(',')
    d = []
    for u in fp:
        portfolio = u.strip().split(',')
        port_d = {}
        for i in range(len(header)):
            key = header[i]
            value= portfolio[i]
            port_d[key] = value
        d.append(port_d)
    fp.close()
    
#    if order.status == True:
    if order.order_type == 'Buy':
        for i in d:
            if i['Symbol'] == order.symbol:
                i['Shares'] = int(i['Shares']) + order.shares
                i['Cost'] = str(i['Cost']) + (','+ str(order.price))
                i['Type'] = 'Buy'
                break
            else:
                new_stock = {}
                new_stock['Symbol'] = order.symbol
                new_stock['Shares'] = order.shares
                new_stock['Cost'] = order.cost # bUG
                new_stock['Price'] = 0 # set as 0 for now, this should be updated with real price when displayed
                new_stock['Type'] = order.order_type
                d.append(new_stock)
    
    if order.order_type == 'Sell':
        for i in d:
            if i['Symbol'] == order.symbol:
                if int(i['Shares']) > order.shares:
                    i['Shares'] = int(i['Shares']) - order.shares
                    i['Cost'] = str(i['Cost']) + (','+ str(order.price))
                    i['Type'] = 'Sell'
                    break
                else:
                    print('You do not have '+str(order.shares)+ ' shares.')
    if order.order_type == 'Sell Short':
        pass
    if order.order_type == 'Buy to Cover':
        pass
    portfolio_data.write_to_csv(d,'portfolio.csv')
                    
def executeOrder(order):#take in pending order, change the order cost or order reserve and update payment in the account CSV file
    current_price = get_price(order.symbol)
    status = getTradingStatus(order.symbol) #needs an update to correct the return value for stock status because it does not return proper value as of now due to API issue
    if status[order.symbol.upper()]['status'] == 'T':
        if order.price_type == 'Market':
            if order.order_type == 'Buy': 
                if order.price >= current_price: # if order price is higher than market price, buy at order price
                    order.cost = order.shares * order.price
                    order.final_price = order.price
                else: # if not buy at order price
                    order.cost = order.shares * current_price
                    order.final_price = current_price
            if order.order_type == 'Sell': # if order price is lower than market price, sell at order price
                if order.price<= current_price:
                    order.cost = order.shares * order.price * -1
                    order.final_price = order.price
                else: # if order price is higher than market price, sell at market price
                    order.cost = order.shares * current_price *-1
                    order.final_price = current_price
            if order.order_type == 'Sell Short': # money gained from sell short is transferred to short reserve, no matter the final profit or loss, the short reserve will be added to the capital, while the cost of buying back is deducted from the capital 
                if order.price <= current_price:
                    order.shortreserve = order.shares * order.price
                    order.final_price = order.price
                else:
                    order.shortreserve = order.shares * current_price
                    order.final_price = current_price
            if order.order_type == 'Buy to Cover':
                if order.price >= current_price:
                    order.cost = order.shares * order.price * -1
                    order.final_price = order.price
                else:
                    order.cost = order.shares * current_price*-1
                    order.final_price = current_price
        writeAccount(order)
        PortfolioUpdate(order)
        order.status = True
    else:
        print('The stock is not tradable at the moment.')
    return order

#write the entered text into a csv file so that pygame can read the csv file and blit each text onto the screen after typing
def writeordertext(attribute):
    fp = open('order_text.csv','a')
    s = str(attribute) 
    print(s, file = fp)
    fp.close()
def resetorder_text(csvfile):
    fp = open(csvfile, 'w')
    fp.close()
#def getOrder(symbol): #if a company has already been chosen, symbol has the symbol of the company, if not, symbol is a place holder ''
#    resetorder_text('order_text.csv')
#    order = Order(symbol)
#    order.getSymbol_Price()
#    writeordertext(order.symbol)
#    writeordertext(order.price)
#    order.getOrderType()
#    writeordertext(order.order_type)
#    order.getShares()
#    writeordertext(order.shares)
#    order.getTerm()
#    writeordertext(order.term)
#    order.getPriceType()
#    writeordertext(order.price_type)
#    order.getTime()
#    writeordertext(order.tstamp)
#    return order


    
#Write Order into csv file
def writeOrder(order):
    fp = open('Portfolio_Transactions.csv', 'a') #without deleting the file content
    order_list = [order.symbol,order.tstamp,order.order_type, str(order.shares), str(order.price), str(order.final_price),str(order.status)]
    order_str = ','.join(order_list)+'\n'
    print(order_str, file = fp)
    fp.close()





#testing out the writing and executing
#def getInput_order():
#    symbol = ''
#    x = getOrder(symbol)
#    executeOrder(x)
#    writeOrder(x)    
    

    

    
    
        
        
    
    
    