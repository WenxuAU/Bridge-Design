# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 20:23:15 2023

@author: wenxuli
"""
import numpy as np
t = 350
h = 1200
Ast = 1240
Asc = 1860
dp = h-1070
dst = 1150
dsc = 50
l = 25
Es = 200e3
fc = 32
epsilonsy = 0.0025
fsy = 500
alpha2 = 0.80
gamma = 0.89
wG = 25*t*h/1e6
MG = wG*l**2/8
epsiloncu = 0.003
Csc = fsy*Asc
p = [alpha2*gamma**2*fc*t/2,-alpha2*gamma*fc*t*dp,\
     Es*Ast*epsiloncu*(dst-dp)+Csc*(dsc-dp)-0.9*MG,\
     Es*Ast*epsiloncu*dst*(dp-dst)]
     
r = np.roots(p)
dn = [i for i in r if i>20][0]
print(dn)
