# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 15:00:08 2023

@author: wenxuli
"""

from Bridge_design_lib import SectionProperties, FlexuralStrength

fc  = 32
fsy = 500
epsilonsy =  0.0025
b = 300
D = 450
d = 390
Ast = 1800
gamma = FlexuralStrength.gamma(fc)
alpha2 = FlexuralStrength.alpha2(fc)
Beam = SectionProperties.RectBeam(b, D, fc=fc, Ast=Ast,dst = d, Asc=0, dsc = 0, Es=0,Ec=1)
