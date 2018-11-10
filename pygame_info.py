import pygame
import requests
import sys

import datetime
import time
import portfolio_data 
import pandaplot as pd
from decimal import Decimal, getcontext
getcontext().prec = 2
B_text = (243, 159, 65)
dark_blue = (19, 80, 178)
green = (17, 191, 37)
def get_news(symbol):
    url = 'https://api.iextrading.com/1.0/stock/'
    url_b = '/news/last/5'
    f_url = url + str(symbol) + url_b
    r = requests.get(f_url)
    json_file= r.json()
    return json_file
def display_news(json_file, surface):
    x = 10
    fonttext = pygame.font.Font('Financial.ttf', 22)
    font1 = pygame.font.SysFont('Financial.ttf', 25)
    counter = 0
    
    info_page = font1.render('Company News'.upper(),True, white)
    surface.blit(info_page, (x,560))
    counter = 0
    for i in json_file:
        counter+=25
        timetext = i['datetime'][5:10] +' ' +i['datetime'][11:19]
        headlinetext = i['headline'].split(' ')
        headlinetext = ' '.join(split_len(headlinetext,10)[0])
        headlinetext += '...'
        timetext_r = fonttext.render(timetext, True, B_text)
        headlinetext_r = fonttext.render(headlinetext, True, white)
        surface.blit(timetext_r,(x, 570+counter))
        surface.blit(headlinetext_r, (x+200, 570+counter))


def get_quote(symbol):
   url = 'https://api.iextrading.com/1.0/stock/'
   url_b = '/quote'
   f_url = url + str(symbol) + url_b
   r = requests.get(f_url)
   r= r.json()
   return r
def display_price(json_file, surface):
    x = 660
    y = 30
    price_font = pygame.font.Font("Financial.ttf", 28)
    latest_price = json_file['latestPrice']
    change = json_file['change']
    change_percent = str(Decimal(json_file['changePercent']) * 100)+'%'
    if str(change)[0] == '-':
        price_text= str(latest_price) + '     CHG: '+ str(change) + '     CHG%: ' + change_percent
    else:
        price_text= str(latest_price) + '     CHG: +'+ str(change) + '     CHG%: +' + change_percent
    price_r = price_font.render(price_text, True, green)
    surface.blit(price_r, (x,y))


def get_info(symbol): # get the current price, return only a float
    url = 'https://api.iextrading.com/1.0/stock/'
    url_b = '/company'
    f_url = url + str(symbol) + url_b
    r = requests.get(f_url)
    r= r.json()
    
    return r
def split_len(seq,length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]
def display_info(json_file, surface):
    x = 660
    fonttext = pygame.font.Font("Financial.ttf", 22)
    font1 = pygame.font.SysFont("Financial.ttf", 32)
    counter = 0
    surface.fill(black)
    #info_page = font1.render('Company Information & Quotes'.upper(),True, white)
    #surface.blit(info_page, (400,20))
    symbol_font = pygame.font.Font(None, 50)
    company_name = json_file['companyName']
    company_symbol = json_file['symbol']
    title = company_symbol + ': ' + company_name
    Title = symbol_font.render(title.upper(), True, dark_blue)
    surface.blit(Title, (5,30))
    pygame.draw.line(surface,B_text,(10,70),(1270,70),6)
    for i in json_file:
        counter += 25
        value_t= json_file[i]

        key = fonttext.render(i.upper(),True, B_text)
        surface.blit(key, (x,100+counter))

        if len(value_t) > 6:
            value_t = value_t.split(' ')
            value_t = split_len(value_t, 5)
            
            for j in value_t:
                j = ' '.join(j)
                value = fonttext.render(j,True, white)
                surface.blit(value, (x+180,100+counter))
                counter+= 25
            counter -= 25
          
        else:
            value = fonttext.render(value_t,True, white)
            surface.blit(value, (x+180,100+counter))
    # pygame.display.update()
def display_chart(symbol,Range):
    if Range =='1m':
        pd.plot_chart_1m(symbol)
    if Range == '1d':
        pd.plot_chart_1d(symbol)
    if Range == '1y':
        pd.plot_chart_1y(symbol)
    if Range == 'd':
        pd.plot_chart_dynamic(symbol)
    fig = pygame.image.load('display.png')
    return fig
    

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
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)


def main():
    
    pygame.init()
    surface = pygame.display.set_mode((1280, 720))
    get_info_done = False
    c_time = time.time()
    t = 0
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    choice = 0
                    return choice
        surface.fill(black)
        
        if get_info_done == False:
            fonttext = pygame.font.Font("Financial.ttf", 32)
            symbol = fonttext.render('Company Symbol',True, white)
            info_page = fonttext.render('Company Information & Quotes',True, white)
            surface.blit(symbol, (350,80))
            surface.blit(info_page, (450,20))
            company_symbol = textbox(surface,650,85)
            company_symbol_text = fonttext.render(company_symbol,True, white)
            surface.blit(company_symbol_text, (20,80))
            print('Initiation Started')
            r = get_info(company_symbol)
            fig = display_chart(company_symbol,'1m')
            print('Chart Update Completed')
            a = get_news(company_symbol)
            print('News Update Completed')
            p = get_quote(company_symbol)
            print('Price Update Completed')
            display_info(r,surface)
            display_news(a,surface)
            display_price(p,surface)
            surface.blit(fig,(10,80))#blit the chart
            get_info_done = True
            print('Initiation Completed')
        else:
            display_info(r, surface)
            display_news(a,surface)
            display_price(p,surface)
            surface.blit(fig,(10,80))#blit the chart


        # if t == 0:
        #     fig = display_chart(company_symbol,'1m')
        # t+=1
        # display_news(a,surface)
        # display_price(p,surface)
        # surface.blit(fig,(10,70))#blit the chart


        if (time.time() - c_time) > 20:
            c_time = time.time()
            print('Time to Update')
            fig = display_chart(company_symbol,'1m')
            print('Chart Update Completed')
            a = get_news(company_symbol)
            print('News Update Completed')
            p = get_quote(company_symbol)
            print('Price Update Completed')
            print('Update Completed (20s)')
        
        clock = pygame.time.Clock()
        clock.tick(30)
        pygame.display.update()

