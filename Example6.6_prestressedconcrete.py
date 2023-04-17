# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 17:53:33 2023

@author: wenxuli

I cannot replicate the results of the Example in the textbook with the same results
"""
from Bridge_design_lib import SectionProperties
import numpy as np
As1 = 3720
As2 = 400
As3 = 400
As4 = 1800
ds1 = 1150
ds2 = 900
ds3 = 300
ds4 = 50
Ap1 = 1200
dp1 = 1060
Ap2 = 500
dp2 = 800

fc = 35
alpha2 = 0.80
gamma = 0.88
sigmape = 1100
Ec = 32e3
Ep = Es = 200e3
fpy = 1750
fsy = 500
yt = yb = 600

tf = 800
h1 = h2 = 100
h = 800
tw = 150
# equivalent presstress force
Pe1 = sigmape*Ap1
Pe2 = sigmape*Ap2
Pe = Pe1+Pe2
dp = (Pe1*dp1+Pe2*dp2)/Pe


Beam = SectionProperties.IBeamParam(tf, tw, h1, h2, h)

e = dp-Beam.dnIg['dn']
e1 = dp1 -Beam.dnIg['dn']
e2 = dp2 -Beam.dnIg['dn']

dn = 210  #assume dn in the web below the flange
epsiloncu = 0.003
i = 1
flag = 1

Cf1 = alpha2*fc*tf*h1
Cf2 = alpha2*fc*(tf-tw)*h2/2
epsilonpe = sigmape/Ep
sigmace1 = Pe/Beam.Ag + Pe*e*e1/Beam.dnIg['Ig']
epsilonce1 = sigmace1/Ec
sigmace2 = Pe/Beam.Ag + Pe*e*e2/Beam.dnIg['Ig']
epsilonce2 = sigmace2/Ec
while flag==1:
    
    Cw = alpha2*fc*tw*(gamma*dn-h1)
    epsilons1 = epsiloncu*(ds1-dn)/dn
    epsilons2 = epsiloncu*(ds2-dn)/dn
    epsilons3 = epsiloncu*(dn-ds3)/dn
    epsilons4 = epsiloncu*(dn-ds4)/dn
    epsiloncp1 = epsiloncu*(dp1-dn)/dn
    epsiloncp2 = epsiloncu*(dp2-dn)/dn    
    
    
    epsilonp1 = epsilonpe+epsilonce1+epsiloncp1
    epsilonp2 = epsilonpe+epsilonce2+epsiloncp2        
    
    Tp1 = Ep*epsilonp1*Ap1
    Tp2 = Ep*epsilonp2*Ap2
    
    if epsilonp1> fpy/Ep:
        Tp1 = fpy*Ap1
    
    
    Tst1 = Es*As1*epsilons1
    if epsilons1 > fsy/Ec:
        Tst1 = fsy*As1 #assume the bottom reinforcement steel at yield
    Tst2 = Es*As2*epsilons2
    Csc3 = Es*As3*epsilons3
    Csc4 = Es*As4*epsilons4
    
    if (Cf1+Cf2+Csc3+Csc4+Cw)-(Tst1+Tst2+Tp1+Tp2)>100:
        dn = dn - 0.1
        flag = 1
    elif (Cf1+Cf2+Csc3+Csc4+Cw)-(Tst1+Tst2+Tp1+Tp2)<-100:
        dn = dn + 0.1
        flag = 1
    else:
        flag = 0
    # flag = 1
    i = i+1
print('dn is {:.2f}mm'.format(dn))
# alpha2*fc*tw
p = [alpha2*fc*tw*gamma,Es*epsiloncu*(As1+As2+As3+As4)\
     -Ep*Ap1*(epsilonce1+epsilonpe-epsiloncu)\
        -Ep*Ap2*(epsilonce2+epsilonpe-epsiloncu)+Cf1+Cf2 \
        -alpha2*fc*tw*h1,-Es*epsiloncu*\
            (As1*ds1+As2*ds2+As3*ds3+As4*ds4)\
             -Ep*epsiloncu*(Ap1*dp1+Ap2*dp2)]

r = np.roots(p)
dn1 = [i for i in r if i>10][0]
print('dn is {:.2f}mm'.format(dn1))


# to compare with the equations given in the textbook
print('Cf1={:.2f}N'.format(Cf1))
print('Cf2={:.2f}N'.format(Cf2))
print('Cw = {:.2f}({:.2f}*dn-{:.2f})'.format(alpha2*fc*tw,gamma,h1))
print('Cs3 = {:.2f}(dn-{:.2f})/dn'.format(Es*As3*epsiloncu,ds3))
print('Cs4 = {:.2f}(dn-{:.2f})/dn'.format(Es*As4*epsiloncu,ds4))
print('Ts1 = {:.2f}({:.2f}-dn)/dn'.format(Es*As1*epsiloncu,ds1))
print('Ts2 = {:.2f}({:.2f}-dn)/dn'.format(Es*As2*epsiloncu,ds2))
print('Tp1 = {:.2f}+{:.2f}({:.2f}-dn)/dn'.format(Ep*Ap1*(epsilonpe+epsilonce1),Ep*Ap1*epsiloncu,dp1))
print('Tp2 = {:.2f}+{:.2f}({:.2f}-dn)/dn'.format(Ep*Ap2*(epsilonpe+epsilonce2),Ep*Ap2*epsiloncu,dp2))

p = [alpha2*fc*tw*gamma,\
     Cf1+Cf2-alpha2*fc*tw*h1+Es*(As1+As2+As3+As4)*epsiloncu-Ep*Ap1*(epsilonpe+epsilonce1-epsiloncu)-\
         Ep*Ap2*(epsilonpe+epsilonce2-epsiloncu),\
         -Es*epsiloncu*(As1*ds1+As2*ds2+As3*ds3+As4*ds4)-Ep*epsiloncu*(Ap1*dp1+Ap2*dp2)]
r = np.roots(p)
print(r)

# calculate the forces

Cw = alpha2*fc*tw*(gamma*dn-h1)
epsilons1 = epsiloncu*(ds1-dn)/dn
epsilons2 = epsiloncu*(ds2-dn)/dn
epsilons3 = epsiloncu*(dn-ds3)/dn
epsilons4 = epsiloncu*(dn-ds4)/dn
epsiloncp1 = epsiloncu*(dp1-dn)/dn
epsiloncp2 = epsiloncu*(dp2-dn)/dn    


epsilonp1 = epsilonpe+epsilonce1+epsiloncp1
epsilonp2 = epsilonpe+epsilonce2+epsiloncp2        

Tp1 = Ep*epsilonp1*Ap1
Tp2 = Ep*epsilonp2*Ap2

Tst1 = Es*As1*epsilons1
Tst2 = Es*As2*epsilons2
Csc3 = Es*As3*epsilons3
Csc4 = Es*As4*epsilons4


#moment capacity
a = gamma*dn
Mu = -(Cf1*h1/2+Cf2*(h1+h2/3)+Cw*(a/2-h1)+Csc3*ds3+Csc4*ds4)+\
    Tst1*ds1+Tst2*ds2+Tp1*dp1+Tp2*dp2
Mu = Mu/1e6
print('Mu is {:.2f}kNm'.format(Mu))


#check ductility
d = (Tst1*ds1+Tst2*ds2+Tp1*dp1+Tp2*dp2)/(Tst1+Tst2+Tp1+Tp2)
kuo = dn/d
print('kuo is {:.2f}'.format(kuo))
print('The ductility is NOT enough')