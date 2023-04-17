# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 15:46:53 2023

@author: wenxuli
"""
from Bridge_design_lib import SectionProperties
import numpy as np
t = 250
h = 750
dp = 625
ds = 700
Ap = 405
Ast = 1350


sigmape = 1100
fc = 40
alpha2 = 0.79
gamma = 0.87
Ep = Es = 200e3
fpb = 1870
fpy = 0.82*fpb
k1 = 0.40
fsy = 500
bef = t
k2 = (Ap*fpb+Ast*fsy)/(bef*dp*fc)
# stress in the tendons
sigmapu = fpb*(1-k1*k2/gamma)

# tensile force in the tendons
Tp = sigmapu*Ap
# tensile force in the reinforcing steel
Ts = fsy*Ast 
#concrete comressive force
Cc = Tp+Ts 
#dn
a = Cc/alpha2/fc/t
dn = a/gamma
#moment capacity
Mu = (Tp*dp+Ts*ds-Cc*a/2)/1e6
print("Mu is {:.2f}kNm".format(Mu))
#check ductility
d = (Tp*dp+Ts*ds)/(Tp+Ts)
kuo = dn/d
print('kuo is {:.2f}'.format(kuo))



