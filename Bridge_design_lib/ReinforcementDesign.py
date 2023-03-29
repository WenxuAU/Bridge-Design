# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:58:58 2023

@author: wenxuli
"""
import numpy as np

''' ==========================transverse reinforcement========================'''

def AsvsShear(Vus,fsyf,dv,thetav):
    return 1e3*Vus/fsyf/dv*np.tan(thetav/180*np.pi)
def Asvsmin(fc,bv,fsyf):
    # the minimum transverse shear reinforcement
    return max([0.08*fc**0.5*bv,0.35*bv])/fsyf

def SpacingCheck(s,D,option=0):
    # option: 0, shear reinforcement; 1: transverse reinforcement
    if option==0:        
        if s> min([0.5*D, 300]): 
            print('Shear reinforcement longitudinal spacing should be less than 0.5D or 300mm, whichever is less')
    else:
        if s> min([D,600]):
            print('Transverse reinforcement lateral spacing shoudl be less than D or 600mm, whichever is smaller')
        
def AsvTorsion():
    pass

'''===========================longitudinal reinforcement======================='''
def dFtdTorsion(T,u0,A0,thetav):
    '''additional design force in the longitudinal tensile reinforcement '''
    '''torsion only'''
    return 0.5*T*u0/2/A0/np.tan(thetav/180*np.pi)

def dFtd(V,Pv,Vus,T,phi,thetav,uh,A0,PvStatus=0):
    '''additional design force in the longitudinal tensile reinforcement '''
    '''Shear with torsion'''
    if PvStatus==0:
        gammap = 0.9
    else:
        gammap = 1.15        
    return ((V-gammap*Pv-0.5*phi*Vus)**2+(0.45*T*uh/2/A0)**2)**0.5/np.tan(thetav/180*np.pi)

def dFtdShear(V,Pv,Vus,phi,thetav,PvStatus=0):
    '''shear without torsion'''
    if PvStatus==0:
        gammap = 0.9
    else:
        gammap = 1.15  
    return (V-gammap*Pv-0.5*phi*Vus)/np.tan(thetav/180*np.pi)


def dFcd(V,Pv,Vus,T,phi,thetav,uh,A0,Fc,PvStatus=0):
    '''addition design force in the longitudinal tensile reinforcement '''
    '''Shear with torsion'''
    return max([dFtd(V,Pv,Vus,T,phi,thetav,uh,A0,PvStatus)-Fc],0)

def dFcdShear(V,Pv,Vus,T,phi,thetav,Fc,PvStatus=0):
    '''shear without torsion'''
    return max([dFtdShear(V,Pv,Vus,T,phi,thetav,PvStatus)-Fc],0)


def Ftd(M,N,dF):
    '''The total force developed in the tensile steel, note gammatd is not introduced
    in AS5100:2017 or AS3600:2018 but in Reinforced Concrete Basics:2021 by Warner'''
    if (M+N)>0:
        gammatd = 1
    else: 
        gammatd = 0.85
    return gammatd*(M+N)/2+dF 

def Fcd(M,N,dF):
    '''The total force developed in the compressive steel, note gammatd is not introduced
    in AS5100:2017 or AS3600:2018 but in Reinforced Concrete Basics:2021 by Warner'''
    if (M+N)>0:
        gammatd = 1
    else: 
        gammatd = 0.85
    return gammatd*(-M+N)/2+dF 


def AstST(dF,phi,Es):
    '''additional shear and/or torsion longitudinal reinforcement area'''
    '''for fully developed bars, fs=fsy
    dF = dFtds or dFtdt or dFtds+dFtdt
    Es: the elaticity modulus of the steel '''
    return dF/phi/Es



    