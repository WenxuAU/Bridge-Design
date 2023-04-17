# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 15:23:01 2023

@author: wenxuli

Serviceability has two parts: 1, deflection; 2, crack
"""
import numpy as np
from Bridge_design_lib import SectionProperties
'''----------------------Clause 8.5.3.1 approach to calculate deflection----'''
def pw(Ast,bw,d,Apt=0):
    '''(Ast+Ap)/bw/d where d is the effective depth to the resultant tensile force
    #bw: the width of the web
    '''
    return (Ast+Apt)/bw/d 
def pcw(Asc,bw,d):
    return Asc/bw/d

def k1(th,t):
    a1 = 0.8+1.2*np.exp(-0.005*th)
    return a1*t**0.8/(t**0.8+0.15*th)
def k4(envro=2):
    '''
    # envro: 0: arid environment; 1: interior environment; 2: temperate inland environment; 3: tropical or nearcostal environment
    '''
    return [0.7,0.65,0.6,0.5][envro]
def epsiloncs(fc,th,aggreg_type=2,envro=2,t=30*365):
    '''
    design shrinkage strain,clause 3.1.7 of AS5100.5:2017
    th: hypothetical thickness of a member used to determine creep and shrinkage
    available from 
    envro: 0: arid environment; 1: interior environment; 2: temperate inland environment; 3: tropical or nearcostal environment
    aggreg_type: the quality of local aggregates: 0 for Sydney and Brisbane; 1: for Melbourne; 2: elsewhere
    '''
    epsiloncse_f = (0.06*fc-1)*50e-6 # final autogenous shrinkage
    epsiloncse = epsiloncse_f*(1-np.exp(-0.1*t))    
    epsiloncsdb_f = [800e-6,900e-6,1000e-6][aggreg_type]
    epsiloncsdb = (1-0.008*fc)*epsiloncsdb_f    
    epsiloncsd = k1(th,t)*k4(envro)*epsiloncsdb # drying skrinkage strain
    print('k1, k4, epsiloncsdb and epsiloncsd are {:.2f}, {:.2f}, {:3e}, {:3e}'.format(k1(th,t),k4(envro),epsiloncsdb,epsiloncsd))
    return epsiloncse+epsiloncsd

def sigmacr(fctf,pw,pcw,Es,epsiloncs,P=0,Ag=1e-3):
    '''cracking stress, clause8.5.3.1 of AS5100.5:2017
    # epsiloncs: design shrinkage strain
    '''
    sigmacs = (2.5*pw-0/8*pcw)/(1+50*pw)*Es*epsiloncs #shrinkgage strain
    print('sigmacs is {:.2f}MPa'.format(sigmacs),P*1e3/Ag)
    return fctf-sigmacs+P*1e3/Ag
def Mcr(Z,sigmacr,P=0,e=0):
    '''
    # cracking moment
    # Z: section modulus
    '''
    return (Z*sigmacr/1e3+P*e)/1e3
    
def Ief(Ig,Icr,Mcr,Ms,Ast,b,d):
    #p= Ast/bd, b is the width of he rectangular cross-section at the comrpession face
    p = Ast/b/d
    if p<0.005:
        Iefmax = 0.6*Ig
    else:
        Iefmax = Ig
    return min([Icr/(1-(1-Icr/Ig)*(Mcr/Ms)**2),Iefmax])

def ADelP(x,p,l,y,z,I,E):
    Pld = SectionProperties.PointLoad(x,p,l,y,z,I,E)
    return Pld.Defl
def ADelUDL(q,l,y,**kwargs):
    UDL = SectionProperties.UniformLoad(q,l,y,**kwargs)
    return UDL.Defl
def ADelPartialUDL(x,d,q,l,y,z,I,E):
    PUDL = SectionProperties.UniformLoad(x,d,q,l,y,z,I,E)
    return PUDL.Defl

def psiccb(fc):
    '''
    #basci creep coefficient
    '''
    fcl=[20,25,32,40,50,65,80,100]
    psiccbl=[5.2,4.2,3.4,2.8,2.4,2.0,1.7,1.5]
    return np.interp(fc, fcl, psiccbl)
def a2(th):           
    return 1.0+1.12*np.exp(-0.008*th)
def k2(th,t):   
    return a2(th)*t**0.8/(t**0.8+0.15*th)
def psicc(fc,th,envro=2,tau=28,t=30*365):
    '''
    # tau: the fist time of loading for the concrete
    # t: time
    '''
    if tau>1:
        k3 = 2.7/(1+np.log10(tau))
    else:
        raise ValueError('the age of concrete t needs to be bigger than 1 day')
    if fc<=50:
        k5 = 1.0 
    elif fc<=100 and fc>50:
        a3 = 0.7/k4(envro)/a2(th)
        k5 = 2.0-a3-0.02*(1.0-a3)*fc 
    print('k2,k3,k4,k5 are {:.2f},{:.2f},{:.2f} and {:.2f}'.format(k2(th,t),k3,k4(envro),k5))
    return k2(th,t)*k3*k4(envro)*k5*psiccb(fc)
def epsiloncc(fc,th,sigma0,Ec,envro=2,tau=28,t=30*365):
    '''
    Creep strain, clause 3.1.8.1 of AS5100.5:2017
     # the crete strain at any time t caused by a constant sustained stress sigma0
    Parameters
    ----------
    fc : TYPE
        characteristic compressive strength, MPa.
    th : TYPE
        hypothetical thickness,mm.
    sigma0 : TYPE
        sustained stress, MPa.
    Ec : TYPE
        concrete modulus, MPa.
    envro : TYPE, optional
        0: arid environment; 1: interior environment; 2: temperate inland environment; 3: tropical or nearcostal environment. The default is 2.
    tau : TYPE, optional
        age of the concrete at the time of loading, in days. The default is 28.
    t : TYPE, optional
        any time. The default is 30*365, i.e. 30 years.

    Returns
    -------
    TYPE
        epsiloncc, the creep strain.

    '''
  
    print('psicc is {:4e}'.format(psicc(fc,th,envro,tau,t)))
    return psicc(fc,th,envro,tau,t)*sigma0/Ec

def ADeltot(epsiloncc,epsiloncs):
    '''
    The overall deflction 

    Parameters
    ----------
    epsiloncc : TYPE
        DESCRIPTION.
    epsiloncs : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return epsiloncc+epsiloncs

if __name__=='__main__':
    '''plot Fig3.1.7.2 of AS5100.5:2017'''
    # print(epsiloncs(32,50,envro=0)*1e6)  #test the calculated results against Table 3.17.2 of AS5100.5:2017
    import matplotlib.pyplot as plt
    
    t = np.logspace(0, 4,1000)
    ticks = [1,3,10,30,100,365,365*3,365*10,365*30]        
    
    th = [50,100,200,400]
    fig2 = plt.figure(1)
    for i in th:
        k = k1(i,t)
        plt.plot(t,k)            
    plt.xscale('log')
    plt.ylim([0,1.8])
    plt.xlim([ticks[0],ticks[-1]])
    plt.xticks(ticks=ticks,labels=[1,3,10,30,100,1,3,10,30])
    plt.text(0.2, -0.12, 'Days',transform=plt.gca().transAxes)
    plt.text(0.8, -0.12, 'Years',transform=plt.gca().transAxes)
    plt.text(0.2, -0.18, 'Time since commencement of drying, t',transform=plt.gca().transAxes)
    
    plt.text(0.8, 0.95, r't$_h$ = 50mm',transform=plt.gca().transAxes)
    plt.text(0.75, 0.85, r't$_h$ = 100mm',transform=plt.gca().transAxes)
    plt.text(0.65, 0.65, r't$_h$ = 200mm',transform=plt.gca().transAxes)
    plt.text(0.55, 0.35, r't$_h$ = 400mm',transform=plt.gca().transAxes)
    plt.text(0.1,0.8,r'$k_1=\frac{a_1t^{0.8}}{t^{0.8}+0.15t_h}$',transform=plt.gca().transAxes)
    plt.text(0.1,0.7,r'$a_1=0.8+1.2e^{-0.005t_h}$',transform=plt.gca().transAxes)
    plt.text(0.1,0.6,r't is in days',transform=plt.gca().transAxes)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('k1')
    plt.grid(which='major')
   
    '''plot Fig3.1.7.3 of AS5100.5:2017'''
    # print(psicc(25,100,envro=0))  #test the calculated results against Table 3.1.8.3 of AS5100.5:2017
    fig2 = plt.figure(2)
    for i in th:
        k = k2(i,t)
        plt.plot(t,k)            
    plt.xscale('log')
    plt.ylim([0,1.8])
    plt.xlim([ticks[0],ticks[-1]])
    plt.xticks(ticks=ticks,labels=[1,3,10,30,100,1,3,10,30])
    plt.text(0.2, -0.12, 'Days',transform=plt.gca().transAxes)
    plt.text(0.8, -0.12, 'Years',transform=plt.gca().transAxes)
    plt.text(0.2, -0.18, 'Time since commencement of drying, t',transform=plt.gca().transAxes)
    
    plt.text(0.8, 0.95, r't$_h$ = 50mm',transform=plt.gca().transAxes)
    plt.text(0.75, 0.8, r't$_h$ = 100mm',transform=plt.gca().transAxes)
    plt.text(0.65, 0.65, r't$_h$ = 200mm',transform=plt.gca().transAxes)
    plt.text(0.55, 0.35, r't$_h$ = 400mm',transform=plt.gca().transAxes)
    plt.text(0.1,0.8,r'$k_2=\frac{a_2t^{0.8}}{t^{0.8}+0.15t_h}$',transform=plt.gca().transAxes)
    plt.text(0.1,0.7,r'$a_2=1.0+1.2e^{-0.008t_h}$',transform=plt.gca().transAxes)
    plt.text(0.1,0.6,r't is in days',transform=plt.gca().transAxes)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('k2')
    plt.grid(which='major')

'''----------------------pseudo-elastic approach to calculate deflection----'''
def kcs(Asc,Ast):
    '''Creep and shinkage factor'''
    return max([2-1.2*Asc/Ast,0.8])

def Fedf(kcs,psis,psil,G,Q):
    '''
    # the effective load for total deflection
    # Eq.3.47 of Reinforced Concrete basics of Warner, 2021
    # G: permenant dead load
    # Q: transient live load
    # psis: short term load factor
    # psil: long term load factor
    '''
    return (1+kcs)*G+(psis+psil*kcs)*Q


def Iefav(option=0,**kwargs):
    '''
    # average effective second moment of area, Iefav, clause 8.5.3.1 of AS5100.5:2017
    #option: 0, simply supported beam; 1, continuous beam, interior span; 2, end span
    '''
    if option==0: 
        Ief = kwargs.get('Ief')
        return Ief 
    elif option ==1:
        Ief_m = kwargs.get('Ief_m')
        Ief_e1 = kwargs.get('Ief_e1')
        Ief_e2 = kwargs.get('Ief_e2')
        return Ief_m/2+(Ief_e1+Ief_e2)/4
    elif option==2:
        Ief_m = kwargs.get('Ief_m')
        Ief_e = kwargs.get('Ief_e')
        return (Ief_m+Ief_e)/2
    else:
        Ief_e = kwargs.get('Ief_e')
        return Ief_e    

def pDelP(l,Ec,Iefav,ML,MM,MR):
    '''Eq.3.46 of Reinforced concrete basics of Warner et al. 2021
    #pseudo-elastic approach for a concentrated distributed load, mid-span deflection
    # To get ML, MM and MR, needs to use SectionProperties.py functions
    '''
    return l**2/48/Ec/Iefav*(ML+4*MM+MR)

def pDelUDL(l,Ec,Iefav,ML,MM,MR):
    '''Eq.3.45 of Reinforced concrete basics of Warner et al. 2021
    # To get ML, MM and MR, needs to use SectionProperties.py functions
    #uniformly distributed load, mid-span deflection
    '''
    return l**2/96/Ec/Iefav*(ML+10*MM+MR)




