# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 09:54:32 2023

@author: wenxuli
"""
from Bridge_design_lib import ActionEffects, SectionProperties,\
    ShearStrength,ReinforcementDesign, FlexuralStrength, TorsionStrength
    
hf1 = 150
hf2 = 180
tw = 900
twall = 150
D = 700
tf = 1600

#assume N12 stirrups and N32 longitudinal reinforcement bars
# 30 is the cover to the stirrups
d = D - 30-12-32/2
bv = 2*twall 
dv = ShearStrength.dv(d, D)

x = tw-2*(30+12/2)
y = D-2*(30+12/2)
A0h = x*y
uh = 2*(x+y)

x0 = tw - twall/2*2
y0 = D-twall/2-hf2/2
A0 = x0*y0
u0 = 2*(x0+y0)

#design load
Md = 800
Vd = 500
Td = 150

# material properties
fc = 40
fsy = 500
fsyf = 500
Es =  200e3

# ------------------design for flexure---------------------------
print('------------------------Design for flexure--------------------------')
#assume a = 50
phi = 0.85
a = 50
z = d-a/2
T = Md*1e3/z/phi #tensile force in steel reinforcement
As_f = T*1e3/fsy

#check the neutral axis location
alpha2 = FlexuralStrength.alpha2(fc)
a = T*1e3/alpha2/fc/tf 
print('a=gamm*dn is {:.2f} mm'.format(a))
print('The flexural reinforcement area is {:.2f} mm2 '.format(As_f))

#---------design for shear--------------------------------------------------
print('------------------------Design for shear--------------------------')
print('-------------------Design for shear transverse reinforcement---------')
Ast = 5600
epsilonx = ShearStrength.epsilonx_TorsionShear(Md, dv, Vd, 0, Td, 0, 0, A0, Es, Ast, 0, 0, 0, 0, uh)
thetav = ShearStrength.thetav(epsilonx)
kv = ShearStrength.kv(fc, 8, 1, 0, epsilonx) # assume Asv=1>Asvmin=0, dg = 8mm

# check web crushing capability
phi = 0.75
Vumax = ShearStrength.Vumax(fc, bv, dv, thetav)
ShearStrength.tauw(Vd, Vumax, 0, Td, bv, dv, twall, uh, A0h, phi)
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
Vu = Vd/phi
Vus = Vu-Vuc
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_s_min = ReinforcementDesign.Asvsmin(fc, bv, fsyf)
if Asv_s>Asv_s_min:
    print("The minimum shear reinforcement is not sufficient, confirming \
the assumption that Asv {:.2f} mm>Asvmin {:.2f} mm".format(Asv_s,Asv_s_min))

print('-------------------Design for shear longitudinal reinforcement---------')
dFtds = ReinforcementDesign.dFtd(Vd, 0, Vus, Td, phi, thetav, uh, A0)
dFcds = ReinforcementDesign.dFcd(Vd, 0, Vus, Td, phi, thetav, uh, A0, 0)
phi = 0.85
Ast_v = ReinforcementDesign.AstST(dFtds, phi, fsy) 
Asc_v = ReinforcementDesign.AstST(dFcds, phi, fsy) 

print('The longitudinal tensile reinforcement area needed for shear is {:.2f} mm2'.format(Ast_v),
      ' and the compressive reinforcement area is {:.2f} mm2'.format(Asc_v))


#---------design for torsion--------------------------------------------------
print('------------------------Design for torsion--------------------------')
print('-------------------Design for torsion transverse and longitudinal reinforcement---------')
Tus = Td/phi
Asw_s = ReinforcementDesign.AswsTorsion(Tus, A0h, fsyf, thetav)
dFtdt = ReinforcementDesign.dFtdTorsion(Td, u0, A0, thetav)
Ast_t = ReinforcementDesign.AstST(dFtdt, phi, fsy) 
print('The transverse tensile reinforcement area needed for torsion is {:.2f} mm'.format(Asw_s),
      ' and the longitudinal reinforcement area is {:.2f} mm2'.format(Ast_t))


#----------------------final results-------------------------------------------
Ast = As_f+Ast_t+Ast_v
Asc = -0.85*As_f+Ast_t+Ast_v

print('The total longitudinal tensile reinforcement area needed for shear is {:.2f} mm2'.format(Ast),
      ' and the compressive reinforcement area is {:.2f} mm2'.format(Asc))
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

#-----------strut and tie model------------------------------------------------
print('----------------------------------------------------------------------')
print('-------------------Strut and tie model--------------------------------')
thetav = 36
#check web crushing 
twalle = twall
Vuwallmax = ShearStrength.Vuwallmax(fc, bv, dv, thetav, twalle)
Vt = TorsionStrength.Vt(Td, dv, A0h)
Vwall = TorsionStrength.Vwall(Vt, Vd)
if Vuwallmax*phi>Vwall:
    print('Web crushing is not a problem')
#---------design for shear--------------------------------------------------
print('------------------------Design for shear--------------------------')
print('-------------------Design for shear transverse reinforcement---------')
Vuc = 0
Vu = Vd/phi
Vus = Vu-Vuc
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_s_min = ReinforcementDesign.Asvsmin(fc, bv, fsyf)
if Asv_s>Asv_s_min:
    print("The minimum shear reinforcement is not sufficient, confirming \
the assumption that Asv {:.2f} mm>Asvmin {:.2f} mm".format(Asv_s,Asv_s_min))
print('-------------------Design for shear longitudinal reinforcement---------')
dFtds = ReinforcementDesign.dFtd(Vd, 0, Vus, Td, phi, thetav, uh, A0)
dFcds = ReinforcementDesign.dFcd(Vd, 0, Vus, Td, phi, thetav, uh, A0, 0)
phi = 0.85
Ast_v = ReinforcementDesign.AstST(dFtds, phi, fsy) 
Asc_v = ReinforcementDesign.AstST(dFcds, phi, fsy) 

print('The longitudinal tensile reinforcement area needed for shear is {:.2f} mm2'.format(Ast_v),
      ' and the compressive reinforcement area is {:.2f} mm2'.format(Asc_v))

#---------design for torsion--------------------------------------------------
print('------------------------Design for torsion--------------------------')
print('-------------------Design for torsion transverse reinforcement---------')
Tus = Td/phi
Asw_s = ReinforcementDesign.AswsTorsion(Tus, A0h, fsyf, thetav)
Ast_t = ReinforcementDesign.AsTorsion(Asw_s, fsy, fsyf, u0, thetav)
print('The transverse tensile reinforcement area needed for torsion is {:.2f} mm'.format(Asw_s),
      ' and the longitudinal reinforcement area is {:.2f} mm2'.format(Ast_t))


#----------------------final results-------------------------------------------
Ast = As_f+Ast_t+Ast_v
Asc = -0.85*As_f+Ast_t+Ast_v

print('The total longitudinal tensile reinforcement area needed for shear is {:.2f} mm2'.format(Ast),
      ' and the compressive reinforcement area is {:.2f} mm2'.format(Asc))








