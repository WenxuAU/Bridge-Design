# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:33:04 2023

@author: wenxuli
"""
from Bridge_design_lib import SectionProperties, Serviceability

l = 7e3
D = l/10 
b = 0.60*D

fc = 32
Ec = 30100
psis = 0.7
psil = 0.4

Beam = SectionProperties.RectBeam(b, D)


wG = 55
wQ = 40
weight = 25*b*D/1e6

kcs = 2
Fedf = Serviceability.Fedf(kcs, psis, psil, wG+weight, wQ)

ML = 0
MM = Fedf*l**2/16e6
MR = -Fedf*l**2/8e6 

Iefav = l/96/Ec/(1/250)*(ML+10*MM+MR)*1e6
Ig = Iefav/0.4 
# choose b = 400
D = (12*Ig/b)**(1/3)
