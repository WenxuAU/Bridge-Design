# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 11:59:37 2023

@author: wenxuli
"""
from Bridge_design_lib import Loading_Effects, SectionProperties,ShearStrength,ReinforcementDesign

l = 7*1e3
fsyf = 250
s = 180
Asv = 4*80
# first assumption of epsilonx

dv = 927
bv = 500
fc= 25
Es = 200e3
Ast = 7140
dg = 8
phi = 0.7
epsilonx = 0.001
diffe = 100
e0 = epsilonx
e1 = 0
while diffe>1e-6:    
    e0 = (e0+e1)/2
    kv = ShearStrength.kv(fc, dg, 1, 0, e0)
    thetav = ShearStrength.thetav(e0)
    Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
    Vus = ShearStrength.Vus(Asv, s, dv, thetav, fsyf)
    Vu = ShearStrength.Vu(Vuc, Vus, 0)
    V = 0.75*Vu 
    M = 1.094*V
    e1 = ShearStrength.epsilonx(M, dv, V, 0, 0, 0, Es, Ast, 0, 0, 0, 0)
    diffe = abs(e1-e0)

epsilonx = e0
    
kv = ShearStrength.kv(fc, dg, 1, 0, e0)
thetav = ShearStrength.thetav(e0)
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
Vus = ShearStrength.Vus(Asv, s, dv, thetav, fsyf)
Vu = ShearStrength.Vu(Vuc, Vus, 0)
V = 0.75*Vu 
M = 1.094*V 
#the maximum load that can be applied
w = V/(l/2-dv)*1000
#check the minimum shear reinforcement requirements
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_s_min = ReinforcementDesign.Asvsmin(fc, bv, fsyf)
if Asv_s>Asv_s_min:
    print('The shear reinforcement is sufficient')
# check longitudinal reinforcement requirements
dFtds = ReinforcementDesign.dFtdShear(V,0,Vus,phi,thetav,0)
z = dv
Ftd = ReinforcementDesign.Ftd(M,0,dFtds)
Fcd = ReinforcementDesign.Fcd(M,0,dFtds)
Fu = 4080*0.5
if phi*Fu > Ftd:
    print('The tensile reinforcement is sufficient')
else:
    print('More tensile reinforcement is needed')
if phi*Fu>Fcd:
    print('The compressive reinforcement is sufficient')
else:
    print('More compressive reinforcement is needed')
    
#check the web crushing
Vumax=ShearStrength.Vumax(fc, bv, dv, thetav)
if V<phi*Vumax:
    #web crushing is not critical
    print('Web crushing failure is not an issue')
else:
    print("Web crushing is an issue, the dimension of the section needs to be increased")
    
    
