# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 15:58:51 2023

@author: wenxuli
"""


''' rail traffic loads-vertical forces'''
#%% vertical rail traffic load: 300LA model
def M300LA(span):
    '''
    Rail traffic load model: 300LA, Section 9.2 of AS5100.2
    span: the span betwen multiple groups, <=20m, >=12m
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
    

#%% Horizontal Forces-vertical direction
'''the empirical models are used here'''
# LLF: total length of the bridge, in metres
# BF: longitudinal braking force, in kN
# TF: longitudinal traction force, in kN
# a: multiple co
from Bridge_design_lib.Vertical_loads import M300LA

def CoexistFactor(n):
    if n == 1:
        CF = 1
    elif n == 2:
        CF = [1,1]
    elif n == 3:
        CF = [1,1,0.5]
    else:
        CF = [1,1,0.5]+[0.25]*n
    return CF

def BrakeForce(LLF,n):
    '''applied to the driving axes, in the longitudinal direction'''
    
    BF = 200+15*LLF
    CF = CoexistFactor(n)
    return BF*CF

def TractionForce(LLF,n):
    ''' apploed to the all axles uniformly, in the longitudinal direction'''
    if LLF>250:
        TF = 2700+5*(LLF-250)
    elif LLF<=250 and LLF>50:
        TF = 1200+7.5*(LLF-50)
    elif LLF<=25:
        TF = 200+25*LLF
    else:
        TF = 200+25(LLF) 
    CF = CoexistFactor(n)
    return TF*CF

def NosingLoad(rail_type,*args):
    ''' Nosing load is applied in the lateral direction
    1. In the case of lateral rail, rail_type=1, the load is 0.5 of the 300LA load
    2. in the case of 300LA load, 100kN is applied at any poistion on the rail laterally and at any location'''
    if rail_type == 1:       
        return {'pos':M300LA(args)['pos'],'loads':M300LA(args)['loads']}
    else: 
        return 100
    
#%% dynamic load allowance
def DynBending(L):
    '''Dynamic load allowance for bending effects, Section 9.5.3 of AS5100.2
    L: characteristic length of a component in meters;
    alpha: the dynamic load factor. alpha*deadload=dynamic load'''
    alpha = 2.16/(L**0.5-0.2)-0.27
    if alpha>0.67:
        alpha = 0.67
    if alpha < 0.2:
        alpha = 0.2
    return alpha
def DynOthers(L):
    '''Dynamic load allowance for other load effects, Section 9.5.5 of AS5100.2
    L: characteristic length of a component in meters;
    Dynamic load effct for torsion, shear and reactions'''
    alpha = 0.67*DynBending(L)
    return alpha
    
#%% Design action
def DesignAction(alpha,load_factor,loads,option):
    '''
    Design action is the design loads in various directions.
    alpha: the dynamic load factor, determined by DynaBending(L) or DhnOthers(L), depending on the type of the loading;
    load_factor: load factors, determined by LoadactorsVertical() and LoadFactors_Horizontal(), for ULS and SLS it has 
    different values;
    loads: M300LA(span), BrakeForce(LLF,n), TractionForce(LLF,n) and NosingLoad(rail_type,*args)'''
    return (alpha+1)*load_factor*loads


#%% ULS and SLS design loads
def ULSLoadComb():
    return {'ReduceSafety':1.45,'IncreaseSafety':0.9}

#%% Fatigue design traffic load
    '''================this part is unfinished=============================='''
    '''================this part is unfinished=============================='''
    '''================this part is unfinished=============================='''
def FatigueDesignTrafficLoad(L):
    '''principle: traffic load+ 0.5* dynamic load allowance'''
    return M300LA+0.5*DynBending(L)




