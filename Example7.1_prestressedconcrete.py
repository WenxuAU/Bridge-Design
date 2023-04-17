# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 11:24:49 2023

@author: wenxuli
"""

fc = 40
Ig = 83.8e9
yt = 552
yb = 668
l = 25

dd = 112
tf = 760
tw = 200
hf1 = 230
hf2 = 75
tb = 510
hb1 = 230
hb2 = 150
h = 1220
Ag = tf*hf1+(tf-tw)/2*hf2+(h-hf1-hb1)*tw+(tb-tw)/2*hb2+tb*hb1
dn = (tf*hf1**2/2+(tf-tw)/2*hf2*(hf2/3+hf1)+\
      tw*(h-hf1-hb1)*((h-hf1-hb1)/2+hf1)+(tb-tw)/2*hb2*(h-hb2/3-hb1)+\
         tb*hb1*(h-hb1/2))/Ag
#self-weight
wG = 25*Ag/1e6
wQ = 24
# minimum serivce load
phis = phil = 1
ws = phis*wG+phil*wQ
#moment at x = 1
x = 1
M = ws*l/2*x-ws*x**2/2
V = ws*l/2-ws*x
#stresses at x=1
eM = 524
Pe = 2435-(2435-2300)/(l/2)*x
ex = eM-4*eM/l**2*(l/2-x)**2
# first moment of area, above or below the centroidal axis
Q = tf*hf1*(dn-hf1/2)+(tf-tw)/2*hf2*(dn-hf1-hf2/3)+\
    (dn-hf1)*tw*(dn-(hf1+(dn-hf1)/2))
# stresses at the neural axis
bv = tw - dd/2
sigmacx = -Pe/Ag*1e3 #tensile 
# M*yb/Ig - Pe/Ag - Pe*ex*yb/Ig
#calculate Vt corresponding to fct
fct = 0.36*fc**0.5 
sigmac1 = fct
Vt = ((sigmac1-0.5*sigmacx)**2-(0.5*sigmacx)**2)**0.5/(Q/Ig/bv)
# stresses at the intersection of the web and bootom flange at the
# section C-C
# first moment of area, above or below the centroidal axis
QCC = tb*hb1*(h-dn-hb1/2)+(tb-tw)/2*hb2*(h-dn-hb1-hb2/3)+\
    hb2*tw*(h-dn-hb2/2-hb1)
tauCC = Vt*QCC/Ig/bv
MCC = Vt/V*M
sigmacxCC = MCC*1e3*(h-dn-(hb1+hb2))/Ig - Pe*1e3/Ag - Pe*1e3*ex*(h-dn-(hb1+hb2))/Ig
sigmac1CC = ((0.5*sigmacxCC)**2+tauCC**2)**0.5+0.5*sigmacxCC #tensile
# the angle of the tendon at x=1.0m
alpha = 8*eM/l**2*(l/2-x)/1e3
Pv= Pe*alpha
Vcr = Pv+Vt/1e3
print('The total shear force at cracking is {:.2f}kN'.format(Vcr))


