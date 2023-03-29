# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:59:23 2023

@author: wenxuli
"""
from Bridge_design_lib import Loading_Effects, SectionProperties,TorsionStrength,\
    ShearStrength,ReinforcementDesign, FlexuralStrength
    
tf = 1600
hf1 = 150
hf2 = 180
tw = 900
D = 700
bv = 300
d = 700-30-12-32/2
dv = ShearStrength.dv(d, D)
Md = 800
Vd = 500
Td = 150
Es =  200e3
fsy = 500
fc = 40
phi = 0.85
dg = 8
# Et = 
# dimension properties
x = D-2*(30+12/2)
y = tw - 2*(30+12/2)
uh = 2*(x+y)
A0h = x*y
x0 = tw-150/2-150/2 
y0 = D - hf2/2-150/2 
u0 = 2*(x0+y0)
A0 = x0*y0
# design for flexture
a = 50 # assume gamma*ku*d = 50mm
z = d - a/2
T = Md/phi/z*1000 
Ast = T/fsy
a = T/FlexuralStrength.alpha2(fc)/fc/tf
if a < 150:
    print('the stress block is in the flange')

#design for shear
Ast = 5600
epsilonx = ShearStrength.epsilonx_TorsionShear(Md, dv, Vd, 0, Td, 0, 0, A0, Es, Ast, 0, 0, 0, 0, uh)
kv = ShearStrength.kv(fc, dg, 1, 0, epsilonx)
thetav = ShearStrength.thetav(epsilonx)
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
Vumax = ShearStrength.Vumax(fc, bv, dv, thetav)
#web crushign failure check

