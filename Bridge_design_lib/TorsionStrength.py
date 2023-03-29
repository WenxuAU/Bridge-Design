# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 13:54:10 2023

@author: wenxuli
"""

'''
Acp: the area enclosed by the outside perimeter,i.e. the area of the section
uc is the length of the outside perimeter of the concrete section, see SectionProperies.py'''  
        
def dv(d,D):
    # dv is the internal level arm
    # d is the distance from the extreme compressive fibre to the centroid of the 
    # area of the reinforcement steel in the tensile half of the session.
    return max([0.9*d,0.72*D])

def Tcr(fc,Acp,bv,uc,sigmacp,option=0,**kwargs):
    # cracking torsional moment
    '''Option: 0, solid section, default; 1: box section.
    bv: the effective width of the critical web
    '''
    Jt = Acp**2/uc
    if option ==1:
        A0 = kwargs.get('A0')
        bv = kwargs.get('bv')
        Jt = min([Jt,2*A0*bv])        
    return 0.33*fc**0.5*Jt*(1+sigmacp/0.33/fc**0.5)**0.5/1000


def CrackCkeck(T,Tcr,V,Vcr=0,**kwargs):
    if Vcr<=0:
        fc = kwargs.get('fc')
        bv = kwargs.get('bv')
        dv = kwargs.get('dv')
        Vcr = min([0.18*fc**0.5*bv*dv,1.2*bv*dv])/1000
    if T/Tcr+V/Vcr >1:
        print("The section is cracked")
def TCalc(Tcr,ratio,fc,bv,dv):
    Vcr = min([0.18*fc**0.5*bv*dv,1.2*bv*dv])/1000
    return 1/(1/Tcr+1/ratio/Vcr)