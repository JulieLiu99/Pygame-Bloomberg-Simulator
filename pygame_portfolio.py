#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 00:38:57 2018

@author: liuxixuan
"""
"""
Created on Mon Apr 30 21:12:15 2018
@author: liuxixuan
"""

import portfolio_data as p
import pygame
import sys
import time

pygame.init()
surface = pygame.display.set_mode((1280, 720))
choice = 0
Symbol = ''
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)

class Text:
    
    def __init__(self):
        self.font = pygame.font.Font(None, 25)
        self.holding = 0
        self.portfolio = ''.encode('utf8')
        self.watchlist = ''.encode('utf8')
        self.account = ''.encode('utf8')
        
    def display_portfolio(self, surface):
        for i in range(len(p.portfolio())):
            self.portfolio = p.portfolio()[i].encode('utf8')
            text = self.font.render(self.portfolio, True, (255, 0, 0))
            surface.blit(text, (20, 120 + 30*i))

    def display_watchlist(self, surface):
    
        for i in range(len(p.watchlist())):
            self.watchlist = p.watchlist()[i].encode('utf8')
            text = self.font.render(self.watchlist, True, (255, 0, 0))
            surface.blit(text, (360, 120 + 30*i))
    
    def display_account(self, surface):

        for i in range(len(p.account())):
            self.account = p.account()[i].encode('utf8')
            text = self.font.render(self.account, True, (255, 0, 0))
            surface.blit(text, (220,20 + 30*i))
            
def textbox1(surface,x,y):
  
    fonttext = pygame.font.Font(None, 25)
    symbol = fonttext.render('Add to watchlist',True, white)
    surface.blit(symbol, (500,460))
    fonttext = pygame.font.Font(None, 28)
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
                        if text != '':
                            add_to_watchlist(text)
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


def textbox2(surface,x,y):
    
    fonttext = pygame.font.Font(None, 25)
    symbol = fonttext.render('Delete from watchlist (return to enter/pass)',True, white)
    surface.blit(symbol, (500,510))
    fonttext = pygame.font.Font(None, 28)
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
                        if text != '':
                            delete_from_watchlist(text)
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
#
#def search_box():
    
#    fonttext = pygame.font.Font(None, 25)
#    symbol = fonttext.render('Watchlist: search company symbol',True, white)
#    surface.blit(symbol, (500,430))
#    company_symbol = textbox(surface,500,475)
#    company_symbol_text = fonttext.render(company_symbol,True, white)
#    surface.blit(company_symbol_text, (540,420))
#    return company_symbol
        
def add_to_watchlist(Symbol):
    
    items_watchlist = p.get_from_csv('watchlist.csv')
    items_watchlist.append({'Symbol':Symbol,'Price':p.get_price(Symbol),'CHG': p.CHG(Symbol), 'CHG %':p.CHG_percent(Symbol)})
    p.write_to_csv(items_watchlist, 'watchlist.csv')
    p.price_dic[Symbol] = p.get_price(Symbol)
    
def delete_from_watchlist(Symbol):
    
    items_watchlist = p.get_from_csv('watchlist.csv')
    for item in items_watchlist:
        if item['Symbol'] == Symbol:
            items_watchlist.remove(item)
    p.write_to_csv(items_watchlist, 'watchlist.csv')
            
class Button:
    
    def __init__(self, text, x, y, length, width):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render(text.encode('utf8'), True, (255, 255, 255))
        self.button = pygame.Rect(self.x, self.y, length, width)
    
    def display(self, surface):
        pygame.draw.rect(surface, [255, 0, 0], self.button)
        surface.blit(self.text, (self.x, self.y))
        
t = Text()
b_info = Button('Information', 500, 620, 100, 30)
b_action = Button('Action', 700, 620, 100, 30)
#b_add = Button('Add', 720, 475, 60, 30)
#b_delete = Button('Delete', 850, 475, 60, 30)

def portfolio_page():
    t.display_portfolio(surface)
    print('p updated')
    t.display_watchlist(surface)
    print('w displayed')
    t.display_account(surface)
    b_info.display(surface)
    b_action.display(surface)
#    b_add.display(surface)
#    b_delete.display(surface)
    
    
def main():

    c_time = time.time()
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if b_info.button.collidepoint(mouse_pos):
                    choice = 1
                    return choice
                elif b_action.button.collidepoint(mouse_pos):
                    choice = 2
                    return choice
                    
        surface.fill((0, 0, 0))
        
        if (time.time() - c_time) > 5:
            c_time = time.time()
            portfolio_page()
            textbox1(surface,500,475)
            textbox2(surface,500,525)
#            
#        for event in pygame.event.get():
#            if event.type == pygame.MOUSEBUTTONDOWN:
#                mouse_pos = event.pos
#                if b_add.button.collidepoint(mouse_pos):
#                    add_to_watchlist(Symbol)
#                elif b_delete.button.collidepoint(mouse_pos):
#                    delete_from_watchlist(Symbol)
                
            pygame.display.update()

    pygame.display.quit()
    
    