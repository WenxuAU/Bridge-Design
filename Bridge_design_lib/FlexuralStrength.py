# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:46:19 2023

@author: wenxuli

References:
    1. Reinforced concrete basis: Warner, 2021
    2. AS5100.5: 2017

"""


'''
Note: the section properties, Ig and Icr can be obtained from SectionProperies.py

'''

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

def StressBloc(fc,b,d,ku):    
    return alpha2(fc)*fc*b*gamma(fc)*ku*d

def SigmaCs(pw,pcw,Es,epsilon_cs):
    '''the cracking stress of the concrete beam, Eq.8.5.3.1 of AS5100.5'''
    return (2.5*pw-0.8*pcw)/(1+50*pw)*Es*epsilon_cs
def Mcr(sigmaCs,fctf,P,Ag,e,Z):
    '''The cracking moment of the concrete beam, Eq.8.5.3.1 of AS5100.5'''
    sigmaCr = fctf -sigmaCs + P/Ag # the cracking stress
    # return the cracking moment
    return Z*sigmaCr+P*e

def Muomin(fctf,P,e,Ag,Ig,Z): 
    '''Minimum strength requirements, Eq.8.1.6.1 of AS5100.5:2017'''
    return 1.2*(Z*(fctf/1e6+P/Ag/1e3)+P*e/1e3)

def Ief(Ig,Icr,Mcr,Ms,Iefmax):
    '''the effective moment of area'''
    return min([Icr/(1-(1-Icr)*(Mcr/Ms)**2),Iefmax])
    
    
    
def RectTest(Ast,fsy,alpha2,fc,tf,hf):
    '''Test whether the section can be treated as rectangular: Ref1, Eq.3.76'''
    if hf>=Ast*fsy/alpha2/fc/tf:
        return 1
    else:
        return 0
    

class StressResultants:
    '''calculate the stress resultants'''
    def __init__(self,Ast,fsy,alpha2,fc,tf,hf,d,gamma):
        '''Ast: the area of tensile reinforcement steel
        fsy: the yield strength of the reinforcemen steel
        alpha2: used to get the stress block
        fc: the characteristic compressive strength of the concrete at 28 days, i.e. fc'
        tf: the width of the flange in a T-beam
        hf: the depth of the flange in a T-beam'''
        self.Ast = Ast
        self.fsy = fsy
        self.alpha2 = alpha2
        self.fc = fc
        self.tf = tf
        self.hf = hf    
        self.d = d
        self.gamma = gamma
        # test whether the T-section can be seen as a rectangular block
        self.Rect = RectTest(Ast,fsy,alpha2,fc,tf,hf)
        # the stress resultant in the tensile reinforcement steel
        self.T = fsy*Ast
        self.dn()
        self.Cf()
        self.Cw()
        self.Mu()
        
    def Cf(self):
        '''Compressive force in the flange'''
        if self.Rect == 0:
            ''''dn is NOT in the flange'''
            self.Cf = self.alpha2*self.fc*self.hf*(self.tb-self.tw)
        else:
            self.Cf = self.alpha2*self.fc*self.dn*(self.tb-self.tw)
    def Cw(self):
        self.Cw = self.T-self.Cf
    def dn(self):
        '''depth of the neutral axis'''
        self.dn = (self.T-self.Cf)/(self.alpha2*self.fc*self.gamma*self.tw)
    def Mu(self):
        '''ultimate moment capacity'''
        self.Mu = self.Cf*(self.d-0.5*self.hf)+self.Cw*(self.d-0.5*self.gamma*self.dn)
    
    

        