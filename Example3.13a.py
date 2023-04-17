# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:57:38 2023

@author: wenxuli
"""

from Bridge_design_lib import ActionEffects, SectionProperties,\
    ShearStrength,ReinforcementDesign, FlexuralStrength
l = 7e3
hf = 250
D = 1100
twall = 250
tw = 1200
bv = 2*twall
d = 1030
dv = ShearStrength.dv(d, D)

fc = 25
fsy = 500
fsyf = 500
Es = 200e3
phi1 = 0.75 # for Vuc and Vus
phi2 = 0.7 # for web crushing

w = 380 # uniform design load, kN/m

# design loads: Md and Vd
Resultants = ActionEffects.UniformLoad(w*1e3, l/1e3, dv/1e3)
Md = Resultants.M/1000
Vd = Resultants.V/1000

#--------------case 1----------------------------------------------------------
# shear reinforcement
dg  = 8
Ast = 5304
epsilonx = ShearStrength.epsilonx(Md, dv, Vd, 0, 0, 0, Es, Ast, 0, 0, 0, 0)
thetav = ShearStrength.thetav(epsilonx)
kv = ShearStrength.kv(fc, dg, 1, 0, epsilonx) #assume Asv>Asvmin
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
#check whether shear reinforcement is needed
ReinforcementDesign.TransverseReinforcementCheck(Vd, Vuc, phi1, 0)
#check web crushing
Vucmax = ShearStrength.Vumax(fc, bv, dv, thetav)
if Vuc<Vucmax:
    print('Web crushing is not an issue')
Vu = Vd/phi1
Vus = Vu-Vuc
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_s_min =ReinforcementDesign.Asvsmin(fc, bv, fsyf)
if Asv_s>Asv_s_min:
    print('the minimum shear reinforcement is not sufficient, the assumption that Asv>Asvmin is correct')
# select the right transverse reinforcement bars

# check the longitudinal reinforcement
dFtd = ReinforcementDesign.dFtdShear(Vd, 0, Vus, phi1, thetav)
dFcd = ReinforcementDesign.dFcdShear(Vd, 0, Vus, phi1, thetav, 0)
z = dv
Ftd = ReinforcementDesign.Ftd(Md, 0, dFtd,z)
Fcd = ReinforcementDesign.Fcd(Md, 0, dFcd,z)

Fu = 2652
print('Fu {:.2f} kN, phi*Fu {:.2f} kN, Ftd {:.2f} kN, Fcd {:.2f} kN'.format(Fu,phi1*Fu,Ftd,Fcd))

#--------------case 2----------------------------------------------------------
print('--------Case 2---------------')
Ast = 4080
epsilonx = ShearStrength.epsilonx(Md, dv, Vd, 0, 0, 0, Es, Ast, 0, 0, 0, 0)
#angle of strut
thetav = ShearStrength.thetav(epsilonx)
kv = ShearStrength.kv(fc, dg, 1, 0, epsilonx) #assume Asv>Asvmin
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
#check whether shear reinforcement is needed
ReinforcementDesign.TransverseReinforcementCheck(Vd, Vuc, phi1, 0)

#check web crushing
Vucmax = ShearStrength.Vumax(fc, bv, dv, thetav)
if Vuc<Vucmax:
    print('Web crushing is not an issue')
Vu = Vd/phi1
Vus = Vu-Vuc
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_s_min =ReinforcementDesign.Asvsmin(fc, bv, fsyf)
if Asv_s>Asv_s_min:
    print('the minimum shear reinforcement is not sufficient, the assumption that Asv>Asvmin is correct')
# select the right transverse reinforcement bars

# check the longitudinal reinforcement
dFtd = ReinforcementDesign.dFtdShear(Vd, 0, Vus, phi1, thetav)
dFcd = ReinforcementDesign.dFcdShear(Vd, 0, Vus, phi1, thetav, 0)
z = dv
Ftd = ReinforcementDesign.Ftd(Md, 0, dFtd,z)
Fcd = ReinforcementDesign.Fcd(Md, 0, dFcd,z)    
Fu = 2040
print('Fu {:.2f} kN, phi*Fu {:.2f} kN, Ftd {:.2f} kN, Fcd {:.2f} kN'.format(Fu,phi1*Fu,Ftd,Fcd))
