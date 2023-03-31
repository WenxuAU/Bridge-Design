# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:55:19 2023

@author: wenxuli
"""


MG = 70  #dead load, kNm
MQ = 110 #live load, kNm
# chosen concrete material
fc = 30  #concrete strength,MPa
fsy = 400 # yeild strength of reinforcement steel, MPa
ku = 0.2  # the ratio between dn and d
phi = 0.8  #capacity reduction factor

gamma = 0.85 -0.007*(fc-28)
# design load
M = 1.25*MG+1.5*MQ
bd2 = M*1e6/(phi*0.85*fc*gamma*ku*(1-0.5*gamma*ku))
r = 0.6 #ratio of b and d
d = (bd2/r)**(1/3)
b = r*d
dn = ku*d    # the depth of netural axis
a = gamma*dn  # the depth of the stress block

#area of the reinforcing steel
C = 0.85*fc*b*a
As = C/fsy

#adjusting to suitably rouned valudes and checking Mu
d = 520
b = 300
D = 570 
As = 1800 
Mu = fsy*As*(d-0.5*gamma*dn)/1e3
print(Mu)
if phi*Mu>M:
    print('The moment capacity d% is bigger than the design moment, d%',Mu,M)
else:
    print('The moment capacity d% is less than the design moment, d%',Mu,M)


print(80/24+8e-3*275**2/128)
sigma = 80/24+8e-3*275**2/128
print(sigma/28570)