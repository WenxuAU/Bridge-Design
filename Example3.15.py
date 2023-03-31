# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:50:49 2023

@author: wenxuli
"""
from Bridge_design_lib import ActionEffects, SectionProperties,TorsionStrength,\
    ShearStrength,ReinforcementDesign, FlexuralStrength

fc = 25    
D = 700
bv = 350
d = D-30-10-28-60/2
Rect = SectionProperties.RectBeam(bv, D)
dv = TorsionStrength.dv(d, D)
Acp = Rect.Ag
uc = Rect.uc
Tcr = TorsionStrength.Tcr(fc, Acp, bv, uc, 0)
Vcr = TorsionStrength.Vcr(fc, bv, dv)
Td = TorsionStrength.TCalc(Tcr, 0.5, fc, bv, dv)