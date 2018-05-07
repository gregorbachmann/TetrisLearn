
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 13:15:44 2018

@author: gregorbachmann
"""

#File to simulate a tetris game
import numpy as np
from matplotlib import pyplot as plt
game = tetris()
game.reset()
counter=0
moves=3

while game.block!=None:
    for i in range(moves):
        action = np.random.randint(0,4)
        if action==0:
            game.translate_left()
        if action==1:
            game.translate_right()
        if action==2:
            game.rotate()
        if action==3:
            game.wait()
        if game.block==None:
            break
        game.project()
        plt.figure(1); plt.clf()
        plt.imshow(game.field)
        plt.title('Number ' + str(i+counter))
        plt.pause(0.02)

    counter+=1

    game.gravitate()
    if game.block == None:
        break
    game.project()
    plt.figure(1); plt.clf()
    plt.imshow(game.field)
    plt.title('Number ' + str(i+counter))
    plt.pause(0.02)
