# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:47:03 2023

@author: wenxuli
"""

Q = 1.0
wG = 3
psis = 0.7
psil = 0.4
fc = 25
hf = 170
l = 2400
Ec = 26700
epsiloncs = 750e-6

D = 370
tf = 7100
tw = 2400
h = 370

# design load
Ag = tf*hf+tw*(D-hf)
weight =  25*Ag/1e3
WG = weight+tf*1
wQ = tf*3 
kcs = 2
Fedf = (1+kcs)*wG+(psis+kcs*psil)*wQ

