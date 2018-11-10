#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
red = (255, 0, 0)
blue = (19, 80, 178)
green = (17, 191, 37)

class Text:
    
    def __init__(self):
        print('Go to Portfolio Page')
        self.font = pygame.font.Font(None, 25)
        self.holding = 0
        to_print = p.To_print()
        self.portfolio = to_print.portfolio()
        self.watchlist = to_print.watchlist()
        self.account = to_print.account()
        self.markets = to_print.markets()
        print('Information updated')
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
b_add = Button('Watchlist: Add/Delete', 460, 475, 200, 30)


def portfolio_page():
    t = Text()
    t.display_portfolio(surface)
    print('portfolio displayed')
    t.display_watchlist(surface)
    print('watchlist displayed')
    t.display_account(surface)
    print('account displayed')
    t.display_markets(surface)
    print('market displayed')
    b_info.display(surface)
    b_action.display(surface)
    b_add.display(surface)
    
def main():
    
    t = 0
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
                elif b_add.button.collidepoint(mouse_pos):
                    choice = 3
                    return choice
                    
        
        if t == 0:
            surface.fill((0, 0, 0))
            portfolio_page()    
            c_time = time.time()
            t += 1
        
        if (time.time() - c_time) > 60:
            c_time = time.time()
            portfolio_page()               
        pygame.display.update()

    pygame.display.quit()
    
