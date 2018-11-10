#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:38:16 2018
@author: liuxixuan
"""

"""
A version of two separate portfolio pages...takes forever
"""
import portfolio_data as p
import pygame
import sys
import datetime
import pygame_portfolio1 as portfolio
import pygame_portfolio2 as portfolio2
import pygame_trading as trading
import pygame_info as infor


pygame.init()
surface = pygame.display.set_mode((1280, 720))
choice = 0
Symbol = ''
clock = pygame.time.Clock()

    
while True:
    if choice == 0:
        choice = portfolio.main()
    elif choice == 1:
        choice = infor.main()
    elif choice == 2:
        choice = trading.main()
    elif choice ==3:
        choice = portfolio2.main()
    clock.tick(30)  
    pygame.display.update()
    
pygame.display.quit()