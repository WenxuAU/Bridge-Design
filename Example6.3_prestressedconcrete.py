# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:32:17 2023

@author: wenxuli
"""
from Bridge_design_lib import SectionProperties
As = 6400
Ap = 2800
fc = 40
alpha2 = 0.79
gamma = 0.87
Ep  =200e3
Es = 200e3
Ec = 32e3
fpy = 1750
fsy = 500
sigmape = 1100

tf = 1500
hf = 250
tw = 350
dst = 805
D = 900
dp = 675 

Beam = SectionProperties.TBeamParam(tf, tw, hf, D)

# dn
Tp = fpy*Ap
Ts = fsy*As
Cf = alpha2*fc*(tf-tw)*hf
a = (Tp+Ts-Cf)/(alpha2*fc*tw)
dn = a/gamma
print('Effective comprssive block depth is {:.2f}mm and dn is {:.2f}mm'\
      .format(a,dn))
    
# assume dn in the flange
a = (Tp+Ts)/(alpha2*fc*tf)
dn = a/gamma
print('Effective comprssive block depth is {:.2f}mm and dn is {:.2f}mm'\
      .format(a,dn))
epsiloncu = 0.003
epsiloncp = epsiloncu*(dp-dn)/dn
epsilonpe = sigmape/Ep
Pe = sigmape*Ap
e = dp-Beam.dnIg['dn']
epsilonce = (Pe/Beam.Ag+Pe*e**2/Beam.dnIg['Ig'])/Ec 
epsilonp = epsilonpe+epsiloncp+epsilonce
epsilonpy = fpy/Ep
print('epsilonp and epsilonpy are {:.2f} and {:.2f}'.format(epsilonp,epsilonpy))

#check ductility
d = (Tp*dp+Ts*dst)/(Tp+Ts)
kuo = dn/d
ku = 0.36
print('kuo and ku are {:.2f} and {:.2f}'.format(kuo,ku))
#moment capacity
Cc = alpha2*fc*tf*a
Mu = (Tp*dp+Ts*dst-Cc*a/2)/1e6
print("Mu is {:.2f} kNm".format(Mu))



