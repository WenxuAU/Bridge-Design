# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:23:18 2023

@author: wenxuli
"""

from Bridge_design_lib import Loading_Effects, SectionProperties,TorsionStrength,\
    ShearStrength,ReinforcementDesign

D = 700
d = 700-30-10-60/2-28/2
dv = TorsionStrength.dv(d,D)
bv =350
fc = 25
Asv = 6*80

Section = SectionProperties.RectBeam(bv,D)
Acp = Section.Ag
uc = Section.uc

Tcr = TorsionStrength.Tcr(fc,Acp,bv,uc,0)

T = TorsionStrength.TCalc(Tcr, 0.5,fc,bv,dv)
print(T)

