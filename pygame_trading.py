#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 19:24:25 2018
28/04/18 Finally knew what is going on with pygame, there is still minor bug with the header of portfolio.csv
in total, we still have to write code for other price type and order type
Textbox is generally fine however, only one inbox can be selected at the moment unless use object oriented lang
@author: enshucheng
"""

#action page
import pygame
import requests
import sys
#import pygame_textinput as pt
import datetime

# import pygame_page.py as p
#pygame initiation
import pandaplot 
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)
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
    def getSymbol_Price(self, string): # a method to get the wanted symbol to execute transaction
        if self.symbol == '':
            self.symbol = string
        self.price = get_price(self.symbol)
    
    def getTerm(self, number): # to get the wanted trading term, basically set self.term to either day order or good till cancelled
        t = ['Day Order', 'Good Till Cancelled']
        self.term = t[int(number)]
    
    def getShares(self, number):
        self.shares = int(number)
    
    def getOrderType(self,number):
        t= ['Buy', 'Sell Short', 'Sell', 'Buy to Cover']
        self.order_type = t[int(number)]
        
    def getPriceType(self, number):
        t = ['Market', 'Limit', 'Stop']
        self.price_type = t[int(number)]
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
        account_d['Cash'] = float(account_d['Cash'])
        account_d['Cash'] -= float(order.cost)
    account_l = [account_d]
    write_to_csv(account_l, 'account.csv')
    

# Portfolio Update

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

def PortfolioUpdate(order):
    Update_status = False
    fp = open('portfolio.csv','r')
    header = fp.readline().strip().split(',')
    d = []
    for u in fp:
        if not u.strip():
            break
        portfolio = u.strip().split(',')
        port_d = {}
        for i in range(len(header)):
            key = header[i]
            value= portfolio[i]
            port_d[key] = value
        d.append(port_d)
    fp.close()
    
    
    if order.order_type == 'Buy':
        found_existing_stock = False
        if d != []:
            for i in d:
                if i['Symbol'] == order.symbol:
                    i['Shares'] = int(i['Shares']) + order.shares
                    #i['Cost'] = str(i['Cost']) + (','+ str(order.price))
                    i['Type'] = 'Buy'
                    i['Price'] = 0
                    i['Value'] = 0
                    found_existing_stock = True
                    Update_status = True
                    break
        if found_existing_stock == False:
            new_stock = {}
            new_stock['Symbol'] = order.symbol
            new_stock['Shares'] = order.shares
            #new_stock['Cost'] = order.cost # bUG
            new_stock['Type'] = order.order_type
            new_stock['Price'] = 0 # set as 0 for now, this should be updated with real price when displayed
            new_stock['Value'] = 0# dum
            d.append(new_stock)
            Update_status = True
    
    if order.order_type == 'Sell':
        found_existing_stock = False
        if d != []:
            for i in d:
                if i['Symbol'] == order.symbol:
                    if int(i['Shares']) > order.shares:
                        i['Shares'] = int(i['Shares']) - order.shares
                        #i['Cost'] = str(i['Cost']) + (','+ str(order.price))
                        i['Type'] = 'Buy'
                        found_existing_stock = True
                        Update_status=True
                        break
        if found_existing_stock == False:
            print('You do not have '+str(order.shares)+ ' shares.')
    if order.order_type == 'Sell Short':
        found_existing_stock = False
        if d!= []:
            for i in d:
                if i['Symbol'] == order.symbol and i['Type'] == order.order_type:
                    i['Shares'] = int(i['Shares']) + order.shares
                    i['Type'] = 'Sell Short'
                    i['Price'] = 0
                    i['Value'] = 0
                    found_existing_stock = True
                    Update_status = True
                    break
        if found_existing_stock == False:
            new_stock = {}
            new_stock['Symbol'] = order.symbol
            new_stock['Shares'] = order.shares
            #new_stock['Cost'] = order.cost # bUG
            new_stock['Type'] = order.order_type
            new_stock['Price'] = 0 # set as 0 for now, this should be updated with real price when displayed
            new_stock['Value'] = 0# dum
            d.append(new_stock)
            Update_status = True
    if order.order_type == 'Buy to Cover':
        found_existing_stock = False
        if d!= []:
            for i in d:
                if i['Symbol'] == order.symbol and i['Type'] == 'Sell Short':
                    if int(i ['Shares']) > order.shares:
                        i['Shares'] = int(i['Shares']) - order.shares
                        i['Type'] = 'Sell Short'
                        i['Price'] = 0
                        i['Value'] = 0
                        found_existing_stock = True
                        Update_status = True
                        break
        if found_existing_stock == False:
            print('You do not have ' + str(order.shares)+' shares or you have not shorted the stock')
    write_to_csv(d,'portfolio.csv')
    return Update_status
def executeOrder(order):#take in pending order, change the order cost or order reserve and update payment in the account CSV file
    current_price = get_price(order.symbol)
    order.shares = int(order.shares)
    order.price = float(order.price)
    status = getTradingStatus(order.symbol) #needs an update to correct the return value for stock status because it does not return proper value as of now due to API issue
   
    '''
    this is to allow trading when the stock market is closed
    '''

    status = {order.symbol.upper():{'status':'T'}}
    status[order.symbol.upper()]['status'] = 'T'#to facilitate trading
    




    if status != {}:
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
            Update_status = PortfolioUpdate(order)
            if Update_status:
                print('Portfolio Updated')
                writeAccount(order)
                print('Account (Cash) updated')
            order.status = True
    else:
        print('The stock is not tradable at the moment.')
    return order
def writeOrder(order):#write order into transaction history
    fp = open('Portfolio_Transactions.csv', 'a') #without deleting the file content
    order_list = [order.symbol,order.tstamp,order.order_type, str(order.shares), str(order.price), str(order.final_price),str(order.status)]
    order_str = ','.join(order_list)+'\n'
    print(order_str, file = fp)
    fp.close()


'''
___________________________________
'''

'''
set up text box to accept input
'''
#symbol_input = pt.TextInput()
#order_type_input = pt.TextInput()
#shares_input = pt.TextInput()
#term_input = pt.TextInput()
#price_type_input = pt.TextInput()
def textupdate(vinput):
    vinput.update(pygame.event.get())
    
def display_prompt(surface):
    font = pygame.font.Font(None, 25)
    font1 = pygame.font.Font(None, 30)
    pygame.draw.line(surface,B_text,(400,60),(400,700),20)
    symbol_text = font1.render('Order Information', True, white)
    surface.blit(symbol_text, (550, 60))
    symbol_text = font.render('Company Symbol', True, white)
    surface.blit(symbol_text, (500, 120))
    symbol_text = font.render('Current Price', True, white)
    surface.blit(symbol_text, (500, 180))
    symbol_text = font.render('Order Type [0: Buy; 1: Sell Short; 2: Sell; 3: Buy to Cover]', True, white)
    surface.blit(symbol_text, (500, 240))
    symbol_text = font.render('Shares', True, white)
    surface.blit(symbol_text, (500, 300))
    symbol_text = font.render('Order Term [0: Day Order]', True, white)
    surface.blit(symbol_text, (500, 360))
    symbol_text = font.render('Price Type [0: Market Price; 1: Limit Order (N.A); 2: Stop Order (N.A)]', True, white)
    surface.blit(symbol_text, (500, 420))

def textbox(surface,x,y):

    fonttext = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(x,y,140,32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        pygame.draw.rect(surface, black, input_box)
        txt_surface = fonttext.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        surface.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(surface, color, input_box, 2)
        
        pygame.display.flip()
        clock.tick(30)
    surface.blit(txt_surface, (input_box.x+5,input_box.y+5))
    return text
def getOrder(symbol, surface): #if a company has already been chosen, symbol has the symbol of the company, if not, symbol is a place holder ''
    restart = True
    while restart == True:
        restart == False
        surface.fill(black)
        display_prompt(surface)
        order = Order(symbol)
        x=textbox(surface,500,140)
        order.symbol = x
        print(order.symbol)
        
        
        order.getSymbol_Price(order.symbol)
        fonttext = pygame.font.Font(None, 32)
        price = fonttext.render(str(order.price),True, pygame.Color('lightskyblue3'))
        surface.blit(price, (500,205))
        
        
        
        x = textbox(surface,500,260)
        order.getOrderType(x)
        print(order.order_type)
        
        x = textbox(surface,500,320)
        order.getShares(x)
        print(order.shares)
        
        x = textbox(surface,500,380)
        order.getTerm(x)
        print(order.term)
        
        x = textbox(surface,500,440)
        order.getPriceType(x)
        print(order.price_type)
        order.getTime()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                                done = True
                                restart =False
                    if event.key == pygame.K_BACKSPACE:
                                done = True
                                restart=True
            surface.fill(black)
            display_prompt(surface)
            font = pygame.font.Font(None, 25)
            font1 = pygame.font.Font(None, 30)
            symbol_text = font1.render('Order Information', True, white)
            surface.blit(symbol_text, (550, 60))
            symbol_text = font.render(order.symbol, True, white)
            surface.blit(symbol_text, (500, 150))
            symbol_text = font.render(str(order.price), True, white)
            surface.blit(symbol_text, (500, 210))
            symbol_text = font.render(order.order_type, True, white)
            surface.blit(symbol_text, (500, 270))
            symbol_text = font.render(str(order.shares), True, white)
            surface.blit(symbol_text, (500, 330))
            symbol_text = font.render(order.term, True, white)
            surface.blit(symbol_text, (500, 390))
            symbol_text = font.render(order.price_type, True, white)
            surface.blit(symbol_text, (500, 450))
            symbol_text = font.render('Do you confirm the order?', True, white)
            surface.blit(symbol_text, (500, 480))
            symbol_text = font.render('To Confirm: Press Enter; To Reset: Press Backspace', True, white)
            surface.blit(symbol_text, (500, 510))
            pygame.display.update()



    return order

def getInput_order(surface):
    symbol = ''
    x = getOrder(symbol, surface)
    print('Got Order')
    x = executeOrder(x)#
    print('executed, written into account and portfolio')
    writeOrder(x)
    print('Written into transaction history')
    global over  # toggle order status, if the order is filled up, stop showing textbox
    over = True
    return x
    
def display_order(order,surface):
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                            done = True
        surface.fill(black)
        display_prompt(surface)
        pygame.draw.line(surface,B_text,(400,60),(400,700),20)
        font = pygame.font.Font(None, 25)
        font1 = pygame.font.Font(None, 30)
        symbol_text = font1.render('Order Information', True, white)
        surface.blit(symbol_text, (550, 60))
        symbol_text = font.render(order.symbol, True, white)
        surface.blit(symbol_text, (500, 150))
        symbol_text = font.render(str(order.price), True, white)
        surface.blit(symbol_text, (500, 210))
        symbol_text = font.render(order.order_type, True, white)
        surface.blit(symbol_text, (500, 270))
        symbol_text = font.render(str(order.shares), True, white)
        surface.blit(symbol_text, (500, 330))
        symbol_text = font.render(order.term, True, white)
        surface.blit(symbol_text, (500, 390))
        symbol_text = font.render(order.price_type, True, white)
        surface.blit(symbol_text, (500, 450))
        symbol_text = font.render('Order Status', True, white)
        surface.blit(symbol_text, (500, 480))
        symbol_text = font.render(str(order.status), True, white)
        surface.blit(symbol_text, (500, 510))
        pygame.display.update()
    return 0
# def DISPLAY_ALL():
#     display_prompt(surface)
#     if not over:
#         getInput_order()
#     else:
#         display_order()
B_text = (243, 159, 65)
dark_blue = (19, 80, 178)
green = (17, 191, 37)
def DISPLAY_ALL(surface):
    
    order = getInput_order(surface)
    finish_display= display_order(order,surface)
    print('i am at line 495')
    return 0
    
#checker = 0 
'''
pygame main loop
'''  
def main(): 
    pygame.init()
    surface = pygame.display.set_mode((1280, 720))
    over = False
    
    while True:
        choice = DISPLAY_ALL(surface)
        print('Display done')
        surface.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    choice = 0
                    return 0
        if choice == 0:
            return choice
        clock = pygame.time.Clock()
        pygame.display.update()
        clock.tick(30)
