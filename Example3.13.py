# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:09:35 2023

@author: wenxuli
"""
from Bridge_design_lib import Loading_Effects, SectionProperties,ShearStrength,ReinforcementDesign
w = 380
l = 7000
D = 1100
d = 1030
bv = 500
Es = 200e3
fc = 25
fsy=500
fsyf=500
dg = 8
Ec = 30100
Act = 0
phi = 0.7
dv = ShearStrength.dv(d,D)
y = [0,dv]
#moment and shear force at a position dv from the support
MV = Loading_Effects.UniformLoad(w, l, y[1])
M = MV.M/1e6
V = MV.V/1e3
#%%--------------------case 1-----------------------------------------
Ast = 5304
# shear design strength
epsilonx = ShearStrength.epsilonx(M,dv,V,0,0,0,Es,Ast,0,0,Ec,Act)
kv = ShearStrength.kv(fc,dg,2,1,epsilonx)
# the contribution from the concrete 
Vuc = ShearStrength.Vuc(fc,bv,dv,kv)
thetav = ShearStrength.thetav(epsilonx)
Vumax = ShearStrength.Vumax(fc,bv,dv,thetav)
if V<phi*Vumax:
    #web crushing is not critical
    print('Web crushing failure is not an issue')
else:
    print("Web crushing is an issue, the dimension of the section needs to be increased")
#the contribution from the stirrups
Vus = (V - phi*Vuc)/phi
#transverse reinforcement demand
Asv_s = ReinforcementDesign.AsvsShear(Vus,fsyf,dv,thetav) # assume Asvmin not sufficient
Asv_s_min = ReinforcementDesign.Asvsmin(fc,bv,fsyf)
#check the validity of the assumption
if Asv_s>Asv_s_min:
    print("The minimum reinforncement is confirmed to be insufficient")
# choose the stirrups
Asv = 320
s = Asv/Asv_s 

# check longitudinal reinforcement
dFtds = ReinforcementDesign.dFtdShear(V,0,Vus,phi,thetav,0)
z = dv
Ftd = ReinforcementDesign.Ftd(M,0,dFtds)
Fcd = ReinforcementDesign.Fcd(M,0,dFtds)
Fu = 2652
if phi*Fu > Ftd:
    print('The tensile reinforcement is sufficient')
else:
    print('More tensile reinforcement is needed')
if phi*Fu>Fcd:
    print('The compressive reinforcement is sufficient')
else:
    print('More compressive reinforcement is needed')

#%%--------------------case 2-----------------------------------
Ast = 4080
# shear design strength
epsilonx = ShearStrength.epsilonx(M,dv,V,0,0,0,Es,Ast,0,0,Ec,Act)
kv = ShearStrength.kv(fc,dg,2,1,epsilonx)

# the contribution from the concrete 
Vuc = ShearStrength.Vuc(fc,bv,dv,kv)
thetav = ShearStrength.thetav(epsilonx)
# epsilonx = (thetav-29)/7000
# kv = ShearStrength.kv(fc,dg,2,1,epsilonx)
# Vuc = ShearStrength.Vuc(fc,bv,dv,kv)
# 
Vumax = ShearStrength.Vumax(fc,bv,dv,thetav)
if V<phi*Vumax:
    #web crushing is not critical
    print('Web crushing failure is not an issue')
else:
    print("Web crushing is an issue, the dimension of the section needs to be increased")

#the contribution from the stirrups
Vus = (V - phi*Vuc)/phi
#transverse reinforcement demand
Asv_s = ReinforcementDesign.AsvsShear(Vus,fsyf,dv,thetav) # assume Asvmin not sufficient
Asv_s_min = ReinforcementDesign.Asvsmin(fc,bv,fsyf)
#check the validity of the assumption
if Asv_s>Asv_s_min:
    print("The minimum reinforncement is confirmed to be insufficient")
# choose the stirrups
Asv = 320
s = Asv/Asv_s 
#check the spacing requirement
ReinforcementDesign.SpacingCheck(s, D)


# check longitudinal reinforcement
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

    