# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 15:58:51 2023

@author: wenxuli
"""


''' vertical forces'''
#%% 300LA model
def M300LA(span):
    '''span: the span betwen multiple groups, <=20m, >=12m
    span is a vector, # of elements = nv'''
    if type(span) is list:
        span = [0]+[float(i) for i in span]
    else:
        span = [span]
    pos = [0,1.7,1.1,1.7,2]
    pos = [sum(pos[:i+1]) for i in range(len(pos))]
    loads = 4*[300]+[360]   
    if len(span)>1:        
        pos1 = []
        for i in range(len(span)):
            pos1 = pos1+list(map(lambda x: x+sum(span[:i+1])+pos[-1]*i, pos))
        loads = loads*len(span) 
        pos=pos1
    return {'pos':pos,'loads':loads}
# print(M300LA([12,20,15]))
#%% dynamic load allowance
def DynBending(L):
    '''L: characteristic length in meters'''
    alpha = 2.16/(L**0.5-0.2)-0.27
    if alpha>0.67:
        alpha = 0.67
    if alpha < 0.2:
        alpha = 0.2
    return alpha
def DynOthers(L):
    '''Dynamic load effct for torsion, shear and reactions'''
    return 0.67*DynBending(L)