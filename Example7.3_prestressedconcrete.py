# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:09:32 2023

@author: wenxuli
"""
from Bridge_design_lib import ReinforcementDesign, ShearStrength
fsy = 500
fsyf = 250
fpb = 1870
Ep = 195e3
Es = 200e3
Ec = 32e3


l = 25
Ap = 2170
dd = 112
tf = 760
tw = 200
hf1 = 230
hf2 = 75
tb = 510
hb1 = 230
hb2 = 150
h = 1220
Ag = 488.4e3
Ig = 83.8e9
yt=552
yb = 668
fc = 40
D = 1220
Ast = 3100
Ap = 2170
dst = 1160
dn = (tf*hf1**2/2+(tf-tw)/2*hf2*(hf2/3+hf1)+\
      tw*(h-hf1-hb1)*((h-hf1-hb1)/2+hf1)+(tb-tw)/2*hb2*(h-hb2/3-hb1)+\
         tb*hb1*(h-hb1/2))/Ag
e = 524

d = 800 # depth of the longitudinal tension reinforcement 
diff = 1e-2
while abs(diff)>1e-5:    
    dv = ShearStrength.dv(d, D)
    ex = e - 4*e/l**2*(l/2-dv/1e3)**2
    dp = ex+dn
    d1 = (Ast*dst+Ap*dp)/(Ast+Ap)
    diff = d1-d
    d = d+diff/5
    
print('The effective shear depth, dv is {:.2f}mm'.format(dv))   
do = max([dv,0.8*D])
alpha = 8*e/l**2*(l/2-do/1e3)/1e3
P = 2435-(2535-2300)/(l/2)*do/1e3
Pv = P*alpha

wG = 25*Ag/1e6
wQ = 24
w = 1.2*wG+1.5*wQ
#design load, do from the support
Md = w*l/2*do/1e3-w*do**2/2e6
Vd = w*l/2 - w*do/1e3
# calculate Vuc
fpo = 0.7*fpb
Act = tb*hb1+(tb-tw)/2*hb2+(h/2-dn)*tw
epsilonx = ShearStrength.epsilonx(Md, dv, Vd, Pv, 0, fpo, Es, Ast, Ep, Ap, Ec, Act)
dg = 8
kv = ShearStrength.kv(fc, dg, 1, 0, epsilonx)
#check webcrushing failure shear force
thetav = ShearStrength.thetav(epsilonx)
bv = tw - 0.5*dd
Vumax = ShearStrength.Vumax(fc, bv, dv, thetav)
print('V* and Vumax are {:.2f} and {:.2f}kN, respectively'.format(Vd,Vumax))
phi = 0.8
if Vd<Vumax*phi:
    print('Web crushing is not an issue')
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)

Vu = Vd/phi
Vus = Vu - Vuc
# transverse shear reinforcement
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
#minimum shear reinforcement
Asv_smin = ReinforcementDesign.Asvsmin(fc, bv, fsyf)

print('Asv/s and Asv/s_min are {:.2f} and {:.2f}, respectively'.format(Asv_s,Asv_smin))
if Asv_s>Asv_smin:
    print('Minimum shear reinforcement is not enough')
else:
    print('Minimum shear reinforcement is enough')

# select the right shear reinforcement steel
Asv = 160
s = Asv/Asv_s
s = 200
print("Asv and s are {:.2f} mm2 and {:.2f}mm, respectively.".format(Asv,s))

# check the shear design at x = 3.5m
x = 3.5e3
ex = e - 4*e/l**2*(l/2-x/1e3)**2
dp = dn+ex
d = (Ast*dst+Ap*dp)/(Ast+Ap)
dv = ShearStrength.dv(d, D)
Pe = 2435-(2535-2300)/(l/2)*x/1e3
alpha = 8*e/l**2*(l/2-x/1e3)/1e3
Pv = Pe*alpha
Md = w*l/2*x/1e3-w*x**2/2e6
Vd = w*l/2 - w*x/1e3
epsilonx = ShearStrength.epsilonx(Md, dv, Vd, Pv, 0, fpo, Es, Ast, Ep, Ap, Ec, Act)
thetav = ShearStrength.thetav(epsilonx)
kv = ShearStrength.kv(fc, dg, 1, 0, epsilonx)
Vumax = ShearStrength.Vumax(fc, bv, dv, thetav)
if Vd<Vumax*phi:
    print('Web crushing is not an issue')
Vuc = ShearStrength.Vuc(fc, bv, dv, kv)
Vu = Vd/phi 
Asv_s = ReinforcementDesign.AsvsShear(Vus, fsyf, dv, thetav)
Asv_smin = ReinforcementDesign.Asvsmin(fc, bv, fsyf)
print('Asv/s and Asv/s_min are {:.2f} and {:.2f}, respectively'.format(Asv_s,Asv_smin))
if Asv_s>Asv_smin:
    print('Minimum shear reinforcement is not enough')
#select the right type of stirrups
Asv = 160
s = Asv/Asv_s
s = 200
print("Asv and s are {:.2f} mm2 and {:.2f}mm, respectively.".format(Asv,s))

