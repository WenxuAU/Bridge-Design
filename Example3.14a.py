# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:13:18 2023

@author: wenxuli
"""
from Bridge_design_lib import ActionEffects, SectionProperties,\
    ShearStrength,ReinforcementDesign, FlexuralStrength
l = 7e3
fsyf = 250
s = 180
Asv = 4*80
d = 1030
D = 1100
dv= ShearStrength.dv(d, D)
dg = 8
Es = 200e3
fc = 25
bv = 500
Ast = 7140
# concrere capacity reduction factor
phi = 0.75
epsilonx = 1e-3 
e0 = epsilonx
e1 = 0
diff = 100
while diff>1e-6:
    e0 = (e0+e1)/2
    thetav = ShearStrength.thetav(e0)
    kv = ShearStrength.kv(fc, dg, 1, 0, e0)
    Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
    Vus = ShearStrength.Vus(Asv, s, dv, thetav, fsyf)
    Vu = ShearStrength.Vu(Vuc, Vus, 0)
    Vd = Vu*phi
    Md = 1.094*Vd
    e1 = ShearStrength.epsilonx(Md, dv, Vd, 0, 0, 0, Es, Ast, 0, 0, 0, 0)
    diff = abs(e1-e0)
epsilonx = e0
thetav = ShearStrength.thetav(epsilonx)
kv = ShearStrength.kv(fc, dg, 1, 0, epsilonx)
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
Vus = ShearStrength.Vus(Asv, s, dv, thetav, fsyf)
Vu = ShearStrength.Vu(Vuc, Vus, 0)
Vd = Vu*phi
print("The shear capacity is {:.2f}".format(Vd))

w = Vd*1e3/(l/2-dv)
#check the minimum longitudinal reinforcement
dFtd = ReinforcementDesign.dFtdShear(Vd, 0, Vus, phi, thetav)
Ftd = ReinforcementDesign.Ftd(Md, 0, dFtd)
Fu = Ast*fsyf/1e3
if phi*Fu<Ftd:
    print('The tensile longitudinal reinforcement is not sufficient')
    # add more longitudinal reinforcement
    Ast1 = (Ftd-phi*Fu)*1e3/fsyf
    print('The additional longitudinal reinforcement area is {:.2f} mm2'.format(Ast1))

#check shear reinforcement sufficiency
Asv_v = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_v_min = ReinforcementDesign.Asvsmin(fc, bv, fsyf)
if Asv_v > Asv_v_min:
    print("The minimum shear reinforcement is sufficient")
    
#check web crushing 
Vumax = ShearStrength.Vumax(fc, bv, dv, thetav)
if phi*Vumax>Vd:
    print("THe web crushing is not an issue")


