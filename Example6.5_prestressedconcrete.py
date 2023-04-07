# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 11:24:20 2023

@author: wenxuli
"""

from Bridge_design_lib import SectionProperties
import numpy as np
As = 6400
Ap = 2800
fc = 40
alpha2 = 0.79
gamma = 0.87
Ep  =200e3
Es = 200e3
Ec = 32e3
fpy = 1700
fsy = 500
sigmape = 1000

t = 300
h = 600
Ap1 = 200
Ap2 = 716
dp1 = 60
dp2 = 540

Beam = SectionProperties.RectBeam(t, h)
# prestressing forces
Pe1 = sigmape*Ap1
Pe2 = sigmape*Ap2 
Pe = Pe1+Pe2
dp = (Pe1*dp1+Pe2*dp2)/Pe
e = dp-h/2
e1 = dp1-h/2
e2 = dp2 - h/2
epsilonpe = sigmape/Ep
epsilonce1 = (Pe/Beam.Ag+Pe*e*e1/Beam.Ig)/Ec
epsilonce2 = (Pe/Beam.Ag+Pe*e*e2/Beam.Ig)/Ec

# calculate dn, assuming the bottom steel is at yield,
# important to note the sign of epsiloncp when it is included in
# the calculation. The equations give position resutls while depending on the
# tensile or compressive state of the concrete block, its sign may be 
# changed
Tp2 = fpy*Ap2
epsiloncu = 0.003
p = [alpha2*fc*t*gamma,-Ep*Ap1*(-epsiloncu+epsilonpe+epsilonce1)
     -Tp2, -Ep*epsiloncu*Ap1*dp1]
r = np.roots(p)
dn = [i for i in r if i>20][0]
print('dn is {:.2f}mm'.format(dn))

#effective depth of the compressive block
a = gamma*dn
Cc = alpha2*fc*t*a
# check the yielding status of the bottom prestressing steel
epsiloncp2 = epsiloncu*(dp2-dn)/dn
epsilonp2 = epsilonpe+epsilonce2+epsiloncp2
epsilonpy = fpy/Ep
print('epsilonpy and epsilonp2 are {:.4f} and {:.4f}'.format(epsilonpy,epsilonp2))
#check ductility
kuo = dn/dp2
ku = 0.36
print('kuo and ku are {:.2f} and {:.2f}'.format(kuo,ku))
#moment capacity
epsiloncp1 = epsiloncu*(dn-dp1)/dn
epsilonp1 = epsilonpe+epsilonce1-epsiloncp1
print('Tp1 is {:.2f}kN by using strain-stress theory'.format(Ep*Ap1*epsilonp1/1e3))
Tp1 = Cc-Tp2
print('Tp1 is {:.2f}kN by using equilibrium'.format(Ep*Ap1*epsilonp1/1e3))
Mu = (Tp1*dp1+Tp2*dp2-Cc*a/2)/1e6
print('Mu is {:.2f}kNm '.format(Mu))




