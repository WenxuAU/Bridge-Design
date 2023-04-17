# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 16:45:31 2023

@author: wenxuli
"""
from Bridge_design_lib import Serviceability
l = 7e3
D = l/10
b = D*0.6

fc = 32
Ec = 30100
Es = 200e3
psis = 0.7
psil = 0.4
wG = 55
wQ = 40
weight = 25*b*D/1e6
# design load
kcs =  2
Fdef = Serviceability.Fedf(kcs, psis, psil, wG+weight, wQ)
#moment at the compressive region, mid span
ML = 0
MM = Fdef*l**2/16e6
MR = -Fdef*l**2/8e6
Iefav = l/96/Ec/(1/250)*(ML+10*MM+MR)*1e6
Ig = Iefav/0.4
# choose b = 400
D = (12*Ig/b)**(1/3)