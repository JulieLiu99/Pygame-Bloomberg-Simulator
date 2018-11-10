#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 00:06:17 2018

@author: liuxixuan
"""

import portfolio_data as p
import pygame
import sys

pygame.init()
surface = pygame.display.set_mode((1280, 720))
choice = 0
Symbol = ''
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)
red = (255, 0, 0)
blue = (19, 80, 178)
green = (17, 191, 37)

class Text:
    
    def __init__(self):
        self.font = pygame.font.Font(None, 25)
        self.holding = 0
        to_print = p.To_print()
        self.portfolio = to_print.portfolio()
        self.watchlist = to_print.watchlist()
        self.account = to_print.account()
        self.markets = to_print.markets()
        
    def display_portfolio(self, surface):
        for i in range(len(self.portfolio)):
            portfolio = self.portfolio[i].encode('utf8')
            text = self.font.render(portfolio, True, red)
            surface.blit(text, (80, 120 + 30*i))

    def display_watchlist(self, surface):

        for i in range(len(self.watchlist)):
            watchlist = self.watchlist[i].encode('utf8')
            text = self.font.render(watchlist, True, blue)
            surface.blit(text, (460, 120 + 30*i))
    
    def display_account(self, surface):

        for i in range(len(self.account)):
            account = self.account[i].encode('utf8')
            text = self.font.render(account, True, white)
            surface.blit(text, (200,20 + 30*i))

            
    def display_markets(self, surface):

        for i in range(len(self.markets)):
            markets = self.markets[i].encode('utf8')
            text = self.font.render(markets, True, grey)
            surface.blit(text, (760, 20 + 30*i))
            
def textbox1(surface,x,y):
  
    fonttext = pygame.font.Font(None, 25)
    symbol = fonttext.render('Add to watchlist (return to enter/pass)',True, white)
    surface.blit(symbol, (440,460))
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
    surface.blit(symbol, (440,510))
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

        
def add_to_watchlist(Symbol):
    
    items_watchlist = p.get_from_csv('watchlist.csv')
    items_watchlist.append({'Symbol':Symbol,'Price':0,'CHG': 0, 'CHG %':0})
    print('new item added')
    p.write_to_csv(items_watchlist, 'watchlist.csv')
    
def delete_from_watchlist(Symbol):
    
    items_watchlist = p.get_from_csv('watchlist.csv')
    for item in items_watchlist:
        if item['Symbol'] == Symbol:
            items_watchlist.remove(item)
            print(item, 'deleted')
    p.write_to_csv(items_watchlist, 'watchlist.csv')

            
class Button:
    
    def __init__(self, text, x, y, length, width):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 25)
        self.text = self.font.render(text.encode('utf8'), True, white)
        self.button = pygame.Rect(self.x, self.y, length, width)
    
    def display(self, surface):
        pygame.draw.rect(surface, green, self.button)
        surface.blit(self.text, (self.x, self.y))
        
b_info = Button('Information', 500, 620, 100, 30)
b_action = Button('Action', 700, 620, 100, 30)

def portfolio_page():
    b_info.display(surface)
    b_action.display(surface)
    textbox1(surface,460,475)
    textbox2(surface,460,525)

    
def main():
    
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

        portfolio_page()

        choice = 0
        return choice
        pygame.display.update()

    pygame.display.quit()
    