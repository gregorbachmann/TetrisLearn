#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 22:33:59 2018

@author: gregorbachmann
"""

#################################################################
#File to define all bricks in plots
#################################################################

#Plot the figures with the characterization having white color

import numpy as np
import matplotlib.pyplot as plt


################################################################
#Stick with orientation 0
################################################################

stick_zero = np.zeros(shape=(5,5))
stick_zero[0:4,2]=1
stick_zero[4,2] = -1
plt.matshow(stick_zero, cmap=plt.cm.Blues)  


################################################################
#Stick with orientation 1
################################################################

stick_one = np.zeros(shape=(5,5))
stick_one[2,0:4]=1
stick_one[2,4] = -1
plt.matshow(stick_one, cmap=plt.cm.Blues)  


###############################################################
#Triangle with orientation 0
###############################################################

triangle_zero = np.zeros(shape=(5,5))
triangle_zero[2,1:4] = 1
triangle_zero[2,0] = -1
triangle_zero[1,2] = 1
plt.matshow(triangle_zero, cmap=plt.cm.Blues) 


###############################################################
#Triangle with orientation 1
###############################################################

triangle_one = np.zeros(shape=(5,5))
triangle_one[1:4,2] = 1
triangle_one[2,0] = -1
triangle_one[2,1] = 1
plt.matshow(triangle_one, cmap=plt.cm.Blues) 


###############################################################
#Triangle with orientation 2
###############################################################

triangle_two = np.zeros(shape=(5,5))
triangle_two[2,1:4] = 1
triangle_two[2,0] = -1
triangle_two[3,2] = 1
plt.matshow(triangle_two, cmap=plt.cm.Blues)


###############################################################
#Triangle with orientation 3
###############################################################

triangle_zero = np.zeros(shape=(5,5))
triangle_zero[1:4,2] = 1
triangle_zero[0,2] = -1
triangle_zero[2,3] = 1
plt.matshow(triangle_zero, cmap=plt.cm.Blues)    