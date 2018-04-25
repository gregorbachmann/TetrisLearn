#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:00:06 2018

@author: gregorbachmann
"""

import numpy as np
import matplotlib.pyplot as plt

n = 20
m = 22

#Initialize empty array and set edges to 5 
tetris = np.zeros(shape=(n,m))
tetris[0,:] = 5
tetris[n-1,:] = 5
tetris[:,0] = 5
tetris[:,m-1] = 5

class brick:
    def __init__(self, shape ,pos=[20,10],orientation=0):
        self.pos = pos
        self.shape = shape
        self.orientation = orientation
        
    def check_if_valid(self,field):
        
        if self.shape==1 and self.orientation==0:
            #If position is cutting a dead field, set state to -1
            if np.sum(field[(self.pos[0]-2):(self.pos[0]+1),self.pos[1]])<0:
                self.state = -1
            #If position is not touching anything, set state to 1
            else:
                self.state = 1
            #Needs another state for game over
        
        return(self)
    
    def project(self,field):
        #First need to delete all current movement to overwrite it with new projection
        #So replace all 1's by 0.
        #Could be solved more elegantly P almost surely
        for i in range(0,n):
            for j in range(0,m):
                if field[i,j]==1:
                    field[i,j]=0
        
        if self.shape==1 and self.orientation==0 and self.state==True:
            field[(self.pos[0]-4):(self.pos[0]-1),self.pos[1]]=1
        
        if self.shape==1 and self.orientation==0 and self.state==False:
            field[(self.pos[0]-4):(self.pos[0]+2),self.pos[1]]=-1
        
        return(field)
    
    def gravity(self):
        #Shift y argument of position one down, always needs to be followed by 
        #check_if_valid before using project to ensure we have a valid state
        #Needs no case distinction as all objects are characterized by their position
        self.pos[0] = self.pos[0]-1
        
        return(self)
    
    def translate_left(self):
        #Again we only have to shift x coordinate of position and need no case distinction
        #Also needs to be followed by a check_if_valid
        self.pos[1] = self.pos[1]-1
        
        return(self)
    
    #def rotate(self):
        
        
a = brick(shape=1)
a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)
a.gravity()
a.check_if_valid(tetris)
a.project(tetris)
plt.matshow(tetris, cmap=plt.cm.Blues)
    
    
        
        
    
