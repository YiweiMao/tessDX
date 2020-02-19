#! usr/bin/env python

# Author: Yiwei Mao
# Last updated: 2020/02/19
# File: pytess.py

'''
Contains methods to run the DX11 reference code and 
plot the tessellated output given tessellation factors
Requires the cpp code to be compiled first
>>> make

Usage:
from pytess import *

Tessellator(partition=PART_INT,outputPrim=OUTPUT_TRIANGLE_CW,tfs=[1,2,3,4]).doTess()
'''

PART_INT = 0
PART_POW2 = 1
PART_FRAC_ODD = 2
PART_FRAC_EVEN = 3

OUTPUT_POINT = 0
OUTPUT_LINE = 1
OUTPUT_TRIANGLE_CW = 2
OUTPUT_TRIANGLE_CCW = 3

ISOLINE_DOMAIN = 0
TRI_DOMAIN = 1
QUAD_DOMAIN = 2

import subprocess
import numpy as np
import matplotlib.pyplot as plt

from ipywidgets import interact, interact_manual

class Tessellator():
    """ methods to generate uv coordinates given tessellation factors """
    def __init__(self,partition=PART_FRAC_EVEN,outputPrim=OUTPUT_TRIANGLE_CW,tfs=[2,2,2,1]):
        """ record tessellation parameters """
        self.partition = partition
        self.outputPrim = outputPrim
        self.tfs = tfs

    def bary2cart(self,b):
        """ converts barycentric coordinates to cartesian [within the unit square] """
        t = np.transpose(np.array([[0,0],[1,0],[1/2,np.sqrt(3)/2]])) # Triangle vertices
        cart = np.zeros(b.shape)
        for i in range(len(b)):
            bb = np.array([b[i,0],b[i,1],1-b[i,0]-b[i,1]])
            cart[i,:] = t.dot(bb)
        return cart

    def doTess(self,show=True):
        """ run the DX11 tessellator """
        # write the settings into a file for the C++ executable
        with open("settings.txt",'w',encoding = 'utf-8') as f:
            f.write(f"{self.partition}\n") # partition scheme
            f.write(f"{self.outputPrim}\n") # output primitive type
            f.write(f"{len(self.tfs)//2-1:d}\n") # domain type
            f.write(f"{len(self.tfs)}\n") # number or tessellation factors
            for i in range(len(self.tfs)):
                f.write(f"{self.tfs[i]:.16f}\n")
        
        # run the DX11 tessellator
        subprocess.call(r"./tess_exp")
        
        # read the generated points
        self.points = []
        with open("points.csv","r",encoding = 'utf-8') as f:
            for line in f:
                self.points.append([float(line[:18]),float(line[19:-1])])
        self.points = np.array(self.points)
        
        # read the generated indexes
        self.indexes = []
        with open("indexes.csv","r",encoding = 'utf-8') as f:
            for line in f:
                self.indexes.append(int(line[:-1]))
        self.indexes = np.array(self.indexes)

        if len(self.tfs)==4:
            self.points = bary2cart(self.points)
        
        # plot the generated primitives
        if show:
            fig,ax = plt.subplots(figsize=(6,6))
            for i in range(len(self.points)):
                ax.text(self.points[i,0]+0.01,self.points[i,1]+0.01,str(i))

            if len(self.tfs) > 2: # tri and quad domain
                for i in np.arange(0,len(self.indexes),3):
                    ax.plot([*self.points[self.indexes[i:i+3],0],self.points[self.indexes[i],0]],
                            [*self.points[self.indexes[i:i+3],1],self.points[self.indexes[i],1]],':')
            else: 
                for i in np.arange(0,len(self.indexes),2):
                    ax.plot(self.points[self.indexes[i:i+2],0],self.points[self.indexes[i:i+2],1],'--')
            plt.xlabel('u'); plt.ylabel('v'); plt.axis('tight')




@interact(partition=(0,3,1),outputPrim=(0,3,1),outTF0=(1,64,0.1),outTF1=(-1,64,0.1),
                 outTF2=(-1,64,0.01),outTF3=(-1,64,0.1),inTF0=(1,64,0.1),inTF1=(-1,64,0.1))
def showTess(partition=0,outputPrim=2,outTF0=1,outTF1=1,outTF2=1,outTF3=1,inTF0=1,inTF1=1):
    """ interactive widget """
    tfs = np.array([outTF0,outTF1,outTF2,outTF3,inTF0,inTF1])
    tfs = tfs[tfs>0]

    print('Partition: \t\t',end="")
    if partition == PART_INT: print('integer')
    elif partition == PART_POW2: print('pow2')
    elif partition == PART_FRAC_ODD: print('frac odd')
    elif partition == PART_FRAC_EVEN: print('frac even')

    print('Output Primitive: \t',end="")
    if outputPrim == OUTPUT_POINT: print('point')
    elif outputPrim == OUTPUT_LINE: print('line')
    elif outputPrim == OUTPUT_TRIANGLE_CW: print('tri cw')
    elif outputPrim == OUTPUT_TRIANGLE_CCW: print('tri ccw')

    print('Tess Domain: \t\t',end="")
    if len(tfs)-2 == ISOLINE_DOMAIN: print('isoline')
    elif len(tfs)-3 == TRI_DOMAIN: print('tri')
    elif len(tfs)-4 == QUAD_DOMAIN: print('quad')
    else: print('invalid domain')

    if np.mod(len(tfs),2) == 0:
        Tessellator(partition,outputPrim,tfs).doTess()
