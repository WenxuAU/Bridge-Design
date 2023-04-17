# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:52:36 2023

@author: wenxuli
"""
from Bridge_design_lib import SectionProperties, Serviceability
from matplotlib import pyplot as plt
Ec = 32e3
fc = 40
Ep = 200e3
Es = 200e3
Ap = 405
dp = 625
dst = 700
Ast = 1350
b = 250
h = 750
Pe = 445

Beam = SectionProperties.RectBeam(b, h)
e = dp - h/2
#determine the moment curvature relationship, iterative approach
dnrng =  [550,500,450,400,375,350,325,300,275,250,200,100,50,10]

M = []
kappa = []

for dn in dnrng:
    epsilon0 = 1e-3
    Cc = 200
    Tp = 0
    Tst = 0
    tmp = Cc-Tp-Tst
    i = 0
    step = 1e-3
    while abs(tmp)>10:
        simga0 = Ec*epsilon0
        Cc = 0.5*simga0*b*dn
        epsilonce = Pe*1e3*(1/Beam.Ag+e**2/Beam.Ig)/Ec
        epsilonpe = Pe*1e3/Ap/Ep
        epsiloncp = epsilon0*(dp-dn)/dn
        epsilonp = epsilonce+epsilonpe+epsiloncp
        Tp = Ep*Ap*epsilonp
        epsilonst = epsilon0*(dst-dn)/dn
        Tst = Es*Ast*epsilonst
        
        if tmp*(Cc-Tp-Tst)<0:      
            step = step/100
        else:
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
        
        tmp = Cc-Tp-Tst
        # print(epsilon0,tmp)
        i= i+1
        # if i>=1:
        #     break
        
    print(dn)
    epsilon0 = epsilon0-step
    M = M+[(Tp*dp+Tst*dst-Cc*dn/3)/1e6]
    kappa = kappa + [epsilon0/dn]
res = [(dn,kappa[i],M[i]) for i,dn in enumerate(dnrng)]
for j in res:
    print('dn, kappa and M are {:d}, {:.3e} and {:.2f}'.format(j[0],j[1],j[2]))
plt.plot(dnrng,M)