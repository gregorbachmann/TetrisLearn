#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:00:06 2018

@author: gregorbachmann
"""

import numpy as np


n = 18
m = 20

#Initialize empty array
tetris = np.zeros(shape=(n,m))

class brick:
    def __init__(self, pos=[9,20], shape ,orientation=0):
        self.pos = pos
        self.shape = shape
        self.orientation = orientation
        self.tetris = tetris
    
    def project(self):
        if shape==1:
            tetris[(self.pos[0]-2):(self.pos[0]+1),self.pos[1]]
    
    def rotate(self):
        
        
    
    
        
        
    
