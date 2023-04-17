# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:13:26 2023

@author: wenxuli
"""

from Bridge_design_lib import Serviceability, SectionProperties

b = 400
h = 800
Ap = 1000
Pe = 1200
e = 250
l = 10

fc = 35
fctf = 0.6*fc**0.5
Es = 200e3

Beam = SectionProperties.RectBeam(b, h)
Z = Beam.Ig/(h/2)

wQ = 30

#shrinkage induced stress
d = 650 # depth to the resultant tensile force
pcw = 0
pw = Serviceability.pw(0, b, d, Apt=Ap)
epsiloncs = Serviceability.epsiloncs(fc, Beam.th,aggreg_type=2,envro=3)
sigmacr = Serviceability.sigmacr(fctf, pw, pcw, Es, epsiloncs,Pe,Beam.Ag)
Mcr = Serviceability.Mcr(Z, sigmacr,Pe,e)
print('The cracking moment is {:.2f} kNm'.format(Mcr))
#cracking load
wcr = 8*Mcr/l**2 
print('The cracking force is {:.2f}kN'.format(wcr))

## example 5.2
d = 700
Ast = 1800
Beam = SectionProperties.RectBeam(b, h)
epsiloncs = Serviceability.epsiloncs(fc, Beam.th,aggreg_type=2,envro=3)
pw = Serviceability.pw(Ast, b, d, Apt=Ap)
sigmacr = Serviceability.sigmacr(fctf, pw, pcw, Es, epsiloncs,Pe,Beam.Ag)
Mcr = Serviceability.Mcr(Z, sigmacr,Pe,e)
print('The cracking moment is {:.2f} kNm'.format(Mcr))
#cracking load
wcr = 8*Mcr/l**2 
print('The cracking force is {:.2f}kN'.format(wcr))