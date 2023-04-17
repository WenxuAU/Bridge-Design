# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:13:32 2023

@author: wenxuli
"""
from Bridge_design_lib import Serviceability, SectionProperties
from matplotlib import pyplot as plt

b = 250
h = 750
Ap = 405
Ast = 1350
Ep = 200e3
Es = 200e3
dp = 625
Pe = 445
dst = 700
fc = 40
Ec = 32e3

Beam = SectionProperties.RectBeam(b, h)
epsiloncs = Serviceability.epsiloncs(fc, Beam.th,envro=-1)
e = dp-h/2
Z = Beam.Ig/(h/2)


#determine the moment curvature relationship, iterative approach
dnrng =  [550,500,450,400,375,350,325,300,275,250,200,100,50,10]

kappa = []
M = []



for dn in dnrng:
    
    cnt = 0 # count the number of iterations
    epsilon0 = 1e-3    
    step = 1e-3 # step change of epsilon0
    tmp = 1000  # to record the difference Cc-Tst-Tp, 1000 is chosen to start the iteration
    
    while abs(tmp)>10:
        tmp0 = tmp   
        
        sigma0 = Ec*epsilon0 
        Cc = 0.5*sigma0*b*dn
        epsilonst = epsilon0*(dst-dn)/dn
        epsiloncp= epsilon0*(dp-dn)/dn
        epsilonpe = Pe*1e3/Ap/Ep 
        epsilonce = Pe*1e3*(1/Beam.Ag+e**2/Beam.Ig)/Ec
        epsilonp = epsilonce+epsilonpe+epsiloncp
        Tst =  Es*epsilonst*Ast
        Tp = Ep*epsilonp*Ap
        tmp = Cc-Tst-Tp
        epsilon0f = Ep*Ap*(epsilonpe+epsilonce)/(0.5*Ec*b*dn-Es*Ast*(dst-dn)/dn-Ep*Ap*(dp-dn)/dn)    
        tmp1 = 0.5*Ec*epsilon0f*b*dn- Es*epsilon0f*(dst-dn)/dn*Ast-\
            Ep*(epsilonpe+epsilonce+epsilon0f*(dp-dn)/dn)*Ap
            
        # print(epsilon0f,tmp1)   
        print('the result is {:.2e} and {:.2f}, respectively'.format(epsilon0,tmp))
        if tmp0*tmp<0:
            step = step/100
        elif tmp0*tmp>0:
            if dn >=205:  # this 205 is a magic number
                if tmp>0:
                    epsilon0 = epsilon0-step
                elif tmp<0:
                    epsilon0 = epsilon0+step
            else:
                if tmp>0:
                    epsilon0 = epsilon0+step
                elif tmp<0:
                    epsilon0 = epsilon0-step
       
        cnt = cnt+1
    # print(dn)
    epsilon0 = epsilon0-step
    M = M+[(Tst*dst+Tp*dp-Cc*dn/3)/1e6]
    kappa = kappa + [epsilon0/dn]

res = [(dn,kappa[i],M[i]) for i,dn in enumerate(dnrng)]
for j in res:
    print('dn, kappa and M are {:d}, {:.3e} and {:.2f}'.format(j[0],j[1],j[2]))
plt.plot(dnrng,M)
    
#%% approach two
kappa = []
M = []
for dn in dnrng:
   
    epsilon0 = Ep*Ap*(epsilonpe+epsilonce)/(0.5*Ec*b*dn-Es*Ast*(dst-dn)/dn-Ep*Ap*(dp-dn)/dn)    
    tmp1 = 0.5*Ec*epsilon0f*b*dn- Es*epsilon0f*(dst-dn)/dn*Ast-\
        Ep*(epsilonpe+epsilonce+epsilon0f*(dp-dn)/dn)*Ap
        
    sigma0 = Ec*epsilon0 
    Cc = 0.5*sigma0*b*dn
    epsilonst = epsilon0*(dst-dn)/dn
    epsiloncp= epsilon0*(dp-dn)/dn
    epsilonpe = Pe*1e3/Ap/Ep 
    epsilonce = Pe*1e3*(1/Beam.Ag+e**2/Beam.Ig)/Ec
    epsilonp = epsilonce+epsilonpe+epsiloncp
    Tst =  Es*epsilonst*Ast
    Tp = Ep*epsilonp*Ap

    M = M+[(Tst*dst+Tp*dp-Cc*dn/3)/1e6]
    kappa = kappa + [epsilon0/dn]    
    
res = [(dn,kappa[i],M[i]) for i,dn in enumerate(dnrng)]
print("Analytic approach:------------------------------------------------")
for j in res:
    print('dn, kappa and M are {:d}, {:.3e} and {:.2f}'.format(j[0],j[1],j[2]))
plt.plot(dnrng,M,'k--')
plt.xlabel('dn,mm')
plt.ylabel('Moment,kNm')

plt.legend(['Numerical Approach','Analytic approach'])