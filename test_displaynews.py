import pygame
import requests
import sys
import datetime
import time
import pandaplot as pd
black = (0,0,0)
white = (255,255,255)
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
    fonttext = pygame.font.Font(None, 22)
    font1 = pygame.font.SysFont('Helvetica', 32)
    counter = 0
    surface.fill(black)
    info_page = font1.render('Company Information & Quotes'.upper(),True, white)
    surface.blit(info_page, (400,20))
    
    for i in json_file:
        counter += 25
        value_t= json_file[i]

        key = fonttext.render(i.upper(),True, white)
        surface.blit(key, (x,130+counter))

        if len(value_t) > 6:
            value_t = value_t.split(' ')
            value_t = split_len(value_t, 6)
            
            for j in value_t:
                j = ' '.join(j)
                value = fonttext.render(j,True, white)
                surface.blit(value, (x+180,130+counter))
                counter+= 25
            counter -= 25
          
        else:
            value = fonttext.render(value_t,True, white)
            surface.blit(value, (x+180,130+counter))
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
def get_news(symbol):
    url = 'https://api.iextrading.com/1.0/stock/'
    url_b = '/news/last/3'
    f_url = url + str(symbol) + url_b
    r = requests.get(f_url)
    json_file= r.json()
    return json_file
def display_news(json_file, surface):
    x = 100
    fonttext = pygame.font.Font(None, 22)
    font1 = pygame.font.SysFont('Helvetica', 32)
    counter = 0
    surface.fill(black)
    info_page = font1.render('Company News'.upper(),True, white)
    surface.blit(info_page, (100,600))
    counter = 0
    for i in json_file:
        counter+=25
        timetext = i['datetime'][5:10] + i['datetime'][11:19]
        headlinetext = i['headline'].split(' ')
        headlinetext = split_len(headlinetext,7)[0] + '...'
        timetext_r = fonttext.render(timetext, True, white)
        headlinetext_r = fonttext.render(headlinetext, True, white)
        surface.blit(timetext_r,(x, 625+counter))
        surface.blit(headlinetext_r, (x+300, 625+counter))
    

pygame.init()
surface = pygame.display.set_mode((1280, 720))
get_info_done = False
c_time = time.time()
news_time = time.time()
t = 0
while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    choice = 0
                    
        surface.fill(black)
        
        if get_info_done == False:
            fonttext = pygame.font.Font(None, 32)
            symbol = fonttext.render('Company Symbol',True, white)
            info_page = fonttext.render('Company Information & Quotes',True, white)
            surface.blit(symbol, (20,80))
            surface.blit(info_page, (400,20))
            company_symbol = textbox(surface,250,75)
            company_symbol_text = fonttext.render(company_symbol,True, white)
            surface.blit(company_symbol_text, (20,80))
            print('xxxxx')
            r = get_info(company_symbol)
            get_info_done = True
        else:
            display_info(r, surface)
            print('info displayed')

        if t == 0:
            fig = display_chart(company_symbol,'1m')
            a = get_news(company_symbol)
        t+=1
        if (time.time() - c_time) > 5:
            c_time = time.time()
            print('Update Completed')
            fig = display_chart(company_symbol,'1m')
            a = get_news(company_symbol)
            print('News Update Completed')
        display_news(a,surface)
        surface.blit(fig,(10,70))#blit the chart
        clock = pygame.time.Clock()
        clock.tick(30)
        pygame.display.update()