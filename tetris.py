#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:00:06 2018

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

class brick:
    def __init__(self, shape ,pos=[20,10],orientation=0,state=1,action="wait",game_over=False,freeze=False):
        self.pos = pos
        self.shape = shape
        self.orientation = orientation
        self.state = state
        self.action = action
        self.game_over = game_over
        self.freeze = freeze
    
    def check_if_valid(self,field):
        #Method to check if resulted position is valid after taking certain actions
        
        #######################################################################################
        #Implementation for stick with 0 orientation
        #######################################################################################
        
        if self.shape==1 and self.orientation==0:
            
            #First action gravity
            if self.action=="gravity":
                
                #If position is cutting a dead field, set state to -1, meaning check if one step 
                #ahead, we will hit a -1
                if np.sum(field[(self.pos[0]-5):(self.pos[0]-1),self.pos[1]])<3:
                    self.state = -1
                    self.freeze=True
                #If position is not touching anything, set state to 1
                else:
                    self.state = 1
            
            #Now actions translate_right and translate_left:
            if self.action=="trans_left" or self.action=="trans_right":
                
                #If position is cutting a dead field, set state to -1
                if np.sum(field[(self.pos[0]-5):(self.pos[0]-1),self.pos[1]])<0:
                    self.state = -1
                    self.freeze = True
                #If position is not touching anything, set state to 1
                else:
                    self.state = 1
        
        #####################################################################################
        #Implementation for stick with 1 orientation
        #####################################################################################
        
        """if self.shape==1 and self.orientation==1:
            
            #First action gravity
            if self.action=="gravity":
                
                #If position is cutting a dead field, set state to -1, meaning check if one step 
                #ahead, we will hit a -1
                if np.sum(field[self.pos[0],(self.pos[1]])<3:
                    self.state = -1
                    self.freeze=True
                #If position is not touching anything, set state to 1
                else:
                    self.state = 1
            
            #Now actions translate_right and translate_left:
            if self.action=="trans_left" or self.action=="trans_right":
                
                #If position is cutting a dead field, set state to -1
                if np.sum(field[(self.pos[0]-5):(self.pos[0]-1),self.pos[1]])<0:
                    self.state = -1
                    self.freeze = True
                #If position is not touching anything, set state to 1
                else:
                    self.state = 1"""
            
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
        
        #Implement motion of brick when not touching anything, hence staying "alive":
        
        #Projection on grid for wand in vertical orientation (orientation=0)
        if self.shape==1 and self.orientation==0 and self.state==1:
            field[(self.pos[0]-5):(self.pos[0]-1),self.pos[1]]=1
        
        
        #Implement projection when brick touches ground/other brick but it's not 
        #game over yet:
        
        #Projection on grid for stick in vertical orientation (orientation=0)
        if self.shape==1 and self.orientation==0 and self.state==-1:
            field[(self.pos[0]-4):(self.pos[0]),self.pos[1]]=-1
        
        return(field)
    
    def gravity(self):
        #Shift y argument of position one down, always needs to be followed by 
        #check_if_valid before using project to ensure we have a valid state
        #Needs no case distinction as all objects are characterized by their position
        self.pos[0] = self.pos[0]-1
        self.action = "gravity"
        return(self)
    
    #Actions the neural network can take:
    
    def translate_left(self):
        #Again we only have to shift x coordinate of position and need no case distinction
        #Also needs to be followed by a check_if_valid
        self.pos[1] = self.pos[1]-1
        self.action = "trans_left"
        return(self)
    
    def translate_right(self):
        #Again we only have to shift x coordinate of position and need no case distinction
        #Also needs to be followed by a check_if_valid
        self.pos[1] = self.pos[1]+1
        self.action = "trans_right"
        return(self)
    
    def wait(self):
        #Don't do anything
        self.action = "wait"
        return(self)
    
    def rotate(self):
        #Rotate in positive direction
        self.orientation = (self.orientation+1)%3
        self.action = "rotate"
        return(self)
    
    def lotate(self):
        #Rotate in negative direction
        self.orientation = (self.orientation-1)%3
        self.action = "lotate"
        return(self)
        
    def reset(self,shape):
        self.pos = [20,10]
        self.shape = shape
        self.orientation = 0
        self.state = 1
        self.action = "wait"
        self.game_over = False
        self.freeze = False
