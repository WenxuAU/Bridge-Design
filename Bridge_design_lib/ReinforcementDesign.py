# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:58:58 2023

@author: wenxuli
"""
import numpy as np

'''---------------------longitudinal reinforcement due to flexure-----------'''

def Astfmin(D,d,bw,fctf,fsy,option=1, **kwargs):

    '''the minimum flexural tensile reinforcement area, Eq.8.1.6.1 of AS5100.5:2017
    option: 0, rectangular sections; 1: T- and L-sections with the web in tension;
    2: T- and L-sections iwth flange in tension'''
    
    if option ==0:
        alphab = 0.2
    else:
        bef = kwargs.get('bef')
        bw = kwargs.get('bw')
        Ds = kwargs.get('Ds')
        if option==1:
        
            alphab = max([0.2+(bef/bw-1)*(0.4*Ds/D-0.18),0.2*(bef/bw)**0.25])
        else:
            alphab = max([0.2+(bef/bw-1)*(0.25*Ds/D-0.18),0.2*(bef/bw)**(2/3)])
    
    return alphab*(D/d)**2*fctf/fsy*bw*d
def alpha2(fc):
    alpha2 = 1.0 - 0.003*fc
    if alpha2>0.85: alpha2 = 0.85
    if alpha2<0.67: alpha2 = 0.67
    return alpha2

def gamma(fc):
    '''Section 8.1.3 of As5100.5
    fc: characteristic concrete compressive strength,MPa
    b: the width of the cross -section of the stress block
    d: the depth of the refinforcement steel from the extreme compressive concrete fibre, mm
    ku: dn/d'''    
    gamma = 1.05 - 0.007*fc    
    if gamma>0.85: gamma = 0.85
    if gamma<0.67: gamma = 0.67
    return gamma
def ku(fc,b,d,Mu):
    Mu = abs(Mu)
    p = [alpha2(fc)*gamma(fc)**2*fc*b*d**2/2e6,-alpha2(fc)*gamma(fc)*b*fc*d**2/1e6,Mu]
    r = np.roots(p)
    return [i for i in r if i >0 and i<1][0]
def Cc(fc,b,d,Mu):
    # the comrpessive force in the concrete
    return alpha2(fc)*fc*gamma(fc)*b*ku(fc,b,d,Mu)*d/1e3


''' ==========================transverse reinforcement========================'''
#--------------shear reinforcement------------------------------------------ 
def TransverseReinforcementCheck(V,Vuc,phi,Pv,option=0,**kwargs):
    if option ==0:
        if V>0.5*phi*Vuc:
            print('Transverse sheear reinforcement is required')
    elif option==1:
        T = kwargs.get('T')
        Tcr = kwargs.get('Tcr')
        if T>0.25*phi*Tcr:            
            print('Transverse sheear reinforcement is required')
    else:
        D = kwargs.get('D')
        if D>750:
            print('Transverse sheear reinforcement is required')

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
#--------------torsion reinforcement------------------------------------------        
def AswsTorsion(Tus,A0h,fsyf,thetav):
    # transverse reinforcement due to torsion only
    A0 = 0.85*A0h
    return Tus*1e6/2/A0/fsyf*np.tan(thetav/180*np.pi)

def Aswsmin(y1,fsyf):
    # y1 is the larger dimension of the colosed tie
    return 0.3*y1/fsyf

'''===========================longitudinal reinforcement======================='''
def dFtdTorsion(T,u0,A0,thetav):
    '''additional design force in the longitudinal tensile reinforcement '''
    '''torsion only'''
    return 0.5*T*1e3*u0/2/A0/np.tan(thetav/180*np.pi)

def dFtd(V,Pv,Vus,T,phi,thetav,uh,A0,PvStatus=0):
    '''additional design force in the longitudinal tensile reinforcement '''
    '''Shear with torsion
    PvStatus: 0: Pv reduces shear; 1, Pv increases shear.
    '''
    if PvStatus==0:
        gammap = 0.9
    else:
        gammap = 1.15        
    return ((V-gammap*Pv-0.5*phi*Vus)**2+(0.45*T*uh/2/A0)**2)**0.5/np.tan(thetav/180*np.pi)

def dFtdShear(V,Pv,Vus,phi,thetav,PvStatus=0):
    '''shear without torsion
    PvStatus: 0: Pv reduces shear; 1, Pv increases shear.'''
    if PvStatus==0:
        gammap = 0.9
    else:
        gammap = 1.15  
    return (V-gammap*Pv-0.5*phi*Vus)/np.tan(thetav/180*np.pi)


def dFcd(V,Pv,Vus,T,phi,thetav,uh,A0,Fc,PvStatus=0):
    '''additional design force in the longitudinal compressive reinforcement '''
    '''Shear with torsion'''
    return max([dFtd(V,Pv,Vus,T,phi,thetav,uh,A0,PvStatus)-Fc,0])

def dFcdShear(V,Pv,Vus,phi,thetav,Fc,PvStatus=0):
    '''shear without torsion'''
    print(dFtdShear(V,Pv,Vus,phi,thetav,PvStatus)-Fc)
    return max([dFtdShear(V,Pv,Vus,phi,thetav,PvStatus)-Fc,0])


def Ftd(M,N,dF,z):
    '''The total force developed in the tensile steel, note gammatd is not introduced
    in AS5100:2017 or AS3600:2018 but in Reinforced Concrete Basics:2021 by Warner
    z: the internal lever arm between internal flexural tension an dflexural compression forces'''
    if (M+N)>0:
        gammatd = 1
    else: 
        gammatd = 0.85
    return gammatd*(M/z+N/2)+dF 

def Fcd(M,N,dF,z):
    '''The total force developed in the compressive steel, note gammatd is not introduced
    in AS5100:2017 or AS3600:2018 but in Reinforced Concrete Basics:2021 by Warner
    Z is the internal lever arm between the internal felxural tension and flexural compression forces from bending'''
    if (M+N)>0:
        gammatd = 1
    else: 
        gammatd = 0.85
    return gammatd*(-M/z+N/2)+dF 


def AstST(F,phi,fsy):
    '''additional shear and/or torsion longitudinal reinforcement area'''
    '''for fully developed bars, fs=fsy
    F: additional force
    fsy: the elaticity modulus of the steel '''
    return F/phi/fsy*1e3

#-----------------------------Strut and tie model------------------------------
def AsTorsion(Asw_s,fsy,fsyf,u0,thetav):
    '''In the Strut-tie model, the longitudinal reinforcement due to torsion, Eq.3.127 of 
    Reinforced Concrete Basics:2021 by Warner'''
    #note only one half of the longitudinal reinforcement is to be provided in the flexural
    #compressive region with the other half in the flexural tensile region
    return 0.5*fsyf/fsy*Asw_s*u0/(np.tan(thetav/180*np.pi))**2


    