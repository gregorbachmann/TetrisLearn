#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 20:41:59 2018

@author: gregorbachmann
"""
import numpy as np
import matplotlib.pyplot as plt

#Choose initial dimensions of tetris grid
n = 20
m = 22

#Initialize empty array and set edges to 5 
tetris = np.zeros(shape=(n,m))
tetris[0,:] = 5
tetris[n-1,:] = 3
tetris[:,0] = 5
tetris[:,m-1] = 5

#Testing movements for bricks
a = brick(shape=1)
#a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)
a.gravity()
a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)
a.translate_right()
a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)   
a.translate_right()
a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)   
a.translate_right()
a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)   


#Testing if brick indeed stops when reaching border 0
tetris_test = np.zeros(shape=(n,m))
tetris_test[0,:] = 5
tetris_test[n-1,:] = 3
tetris_test[:,0] = 5
tetris_test[:,m-1] = 5
b = brick(shape=1)
b.project(tetris_test)   
for i in range(0,30):
    b.gravity()
    b.check_if_valid(tetris_test)
    b.project(tetris_test)
    if b.freeze==True:
        break
        
plt.matshow(tetris_test)  


#Testing if two blocks merge
tetris_test_2 = np.zeros(shape=(n,m))
tetris_test_2[0,:] = 5
tetris_test_2[n-1,:] = 3
tetris_test_2[:,0] = 5
tetris_test_2[:,m-1] = 5
object1 = brick(shape=1)

object1.reset(shape=1)
object1.project(tetris_test_2) 
for i in range(0,30):
    object1.gravity()
    object1.check_if_valid(tetris_test_2)
    object1.project(tetris_test_2)
    if object1.freeze==True:
        break
        
plt.matshow(tetris_test_2)  
object1.reset(shape=1)
object1.project(tetris_test_2) 
for i in range(0,10):
    object1.gravity()
    object1.check_if_valid(tetris_test_2)
    object1.project(tetris_test_2)
    if object1.freeze==True:
        break
plt.matshow(tetris_test_2)