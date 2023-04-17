# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 17:01:55 2023

@author: wenxuli
"""
import numpy as np
l = 20
t = 400
h = 950
Ap = 900
dp = 815
dst = 900
e = 340
wG = 25*t*h/1e6
wQ = 15
P = 972
fc = 40
alpha2 = 0.79
gamma = 0.87
fsy = 500
fpy = 1750
sigmape = 1100
Ep = Es = 200e3
w = 1.2*wG+1.5*wQ
M = w*l**2/8
phi = 0.85
Mu = M/phi
Ast = (Mu*1e6-fpy*Ap*(dp-0.15*dst))/(0.85*dst*fsy)
# choose the reinforcement bars
Ast = 3100 # 5N28
#check strength requirement
#calculate dn, assuming reinforce steel at yield
epsiloncu = 0.003
p = [alpha2*gamma*fc*t,Ep*Ap*epsiloncu-fsy*Ast,\
     -Ep*Ap*epsiloncu*dp]
r = np.roots(p)
dn = [i for i in r if i>10][0]
a = gamma*dn
#check whether the reinforcement steel is indeed at yield
epsilonst = epsiloncu*(dst-dn)/dn
epsilonsy = fsy/Es
print('epsilonst and epsilonsy are {:.4f},{:.4f}, respectively'\
      .format(epsilonst,epsilonsy))
epsilonp = epsiloncu*(dp-dn)/dn
epsilonpy = fpy/Ep
print('epsilonp and epsilonpy are {:.4f},{:.4f}, respectively'\
      .format(epsilonp,epsilonpy))
    

# calculate forces
Tst = fsy*Ast
Tp = Ep*Ap*epsilonp
Cc = Tp+Tst
dn1 = (Tst+fpy*Ap)/alpha2/gamma/fc/t
epsilonp1 = epsiloncu*(dp-dn1)/dn1 
#effective depth
d = (Tp*dp+Tst*dst)/(Tp+Tst)
kuo = dn/d
k = 0.36
print('kuo and k are {:.2f} and {:.2f}, respectively'.format(kuo,k))
#check strength
Mu = (Tst*dst+Tp*dp-Cc*a/2)/1e6
print('Mu is {:.2f}kNm'.format(Mu))
print('phi*Mu and M* are {:.2f} and {:.2f}kNm, respectively'\
      .format(phi*Mu,M))


