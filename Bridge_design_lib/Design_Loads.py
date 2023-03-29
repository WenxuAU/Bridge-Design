# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 15:58:51 2023

@author: wenxuli
"""


''' rail traffic loads-vertical forces'''
import os
print(os.path.realpath(__file__))
from matplotlib import pyplot as plt
import numpy as np
#%% vertical rail traffic load: 300LA model
def M300LA(Lv,x_shift=0):
    '''
    Rail traffic load model: 300LA, Section 9.2 of AS5100.2
    Lv: the span betwen centres of axle groups,i.e. vehicle lengths, <=20m and >=12m
    Lv can be a vector, # of elements = nv; when there is one axle group on the bridge
    Lv=0
    x_shift: the shift of the first axle group starting point longitudinally along the bridge
    '''
    
    if type(Lv) is list:
        if Lv[0]>0 and len(Lv)>=1:
            Lv = [0]+[float(i) for i in Lv]
    elif Lv>0:
        Lv = [0,Lv]
        # print(Lv)
    else:
        Lv=[0]
    if len(Lv)>1:
        for i in Lv[1:]:        
            # print(i)
            if i >20 or i <12:
                raise ValueError("Error: each axle group distance has to be between 12 and 20m")
            
    pos = [0,1.7,1.1,1.7,2]
    pos = [sum(pos[:i+1]) for i in range(len(pos))]
    loads = 4*[300e3]+[360e3]   
    if len(Lv)>1:        
        pos1 = []
        for i in range(len(Lv)):
            pos1 = pos1+list(map(lambda x: x+sum(Lv[:i+1])+pos[-1]*i, pos))
        loads = loads*len(Lv) 
        pos=pos1      
    return {'pos':[k+x_shift for k in pos],'loads':loads}
#% test code 
Lv = [12,12]
x_shift = 20
traffic_loads = M300LA(Lv,x_shift)
theta = np.linspace(0,2*np.pi,20)
# plt.rcParams['figure.figsize']=(6,5)
for i in range(len(traffic_loads['pos'])):
    x = traffic_loads['pos'][i]+0.45*np.cos(theta)
    y = 0.45+0.45*np.sin(theta)    
    plt.arrow(traffic_loads['pos'][i],3,0,-1.5,width=0.05,head_width=0.2,color='r')
    plt.plot(x,y,'k')
plt.ylim([0,8])
plt.plot(traffic_loads['pos'],traffic_loads['loads'],'ko')
plt.xlabel('x,m')
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.draw()

#%% Horizontal Forces-vertical direction
'''the empirical models are used here'''
# LLF: total length of the bridge, in metres
# BF: longitudinal braking force, in kN
# TF: longitudinal traction force, in kN
# a: multiple co

def CoexistFactor(n):
    '''
    n: number of rail vehicles
    
        '''
    if n == 1:
        CF = [1]
    elif n == 2:
        CF = [1,1]
    elif n == 3:
        CF = [1,1,0.5]
    else:
        CF = [1,1,0.5]+[0.25]*n
    return CF

def BrakeForce(LLF,n):
    '''applied to the driving axles, in the longitudinal direction'''
    
    BF = 200+15*LLF
    CF = CoexistFactor(n)
    return BF*CF

def TractionForce(LLF,n):
    ''' Section 9.7.2.2 Empirical model
    LLF: total length of the bridge, in metres
    n: the number of vehicles on the birdge at the same 
    applied to all axles uniformly, in the longitudinal direction'''
    print(LLF)
    if LLF>250:
        TF = 2700+5*(LLF-250)
    elif LLF<=250 and LLF>50:
        TF = 1200+7.5*(LLF-50)
    elif LLF<=25:
        TF = 200+25*LLF
    else:
        TF = 825+15*(LLF-25) 
        
    print('trial')
    CF = CoexistFactor(n)
    return [TF*i*1e3 for i in CF]   #change the unit to Newton from kN


def NosingLoad(x):
    ''' Section 9.7.3 of AS5100.2
    Nosing load is applied in the lateral direction at a single point at any location along the track
    x: the location of the load applied along the track
    1. In the case of lateral rail, rail_type=1, the load is 0.5 of the 300LA load
    2. in the case of 300LA load, 100kN is applied at any poistion on the rail laterally and at any location'''
    
    return {'pos':x,'load':100e3}

#%% Fatigue design traffic load
'''================this part is unfinished=============================='''
'''================this part is unfinished=============================='''
from Bridge_design_lib.Load_Factors_Combination import DLA

def FLS(Lv,L,discount=0.5,x_shift=0):
    '''FLS: Fatigue Limit State
    Section 9.8 and Table D1 of AS5100.2. Principle: traffic load+ 0.5* dynamic load allowance
    Lv: distance between axle group centers, i.e. the vehicle length, in metres
    L: characteristic length of a component
    x_shift: the shift of the first axle group starting point longitudinally along the bridge
    discount: used to discount the influence of dynamic load effect, 0.5 in default;
    the load factor for Fatige Limit State is 1.0
    '''    
    tmp = DLA(L)
    tmp.DynBending()
    loads = M300LA(Lv,x_shift)
    return {'pos':loads['pos'],'loads':[load*1.0*(1+discount*tmp.alpha_bending) 
                                        for load in loads['loads']]}





