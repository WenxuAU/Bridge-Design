# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 15:30:07 2023

@author: wenxuli
"""

from Bridge_design_lib import FlexuralStrength, SectionProperties, ReinforcementDesign

wG = 62
wQ = 40
l = 7e3
b = 400
D = 660
fc = 32
fsy = 500
weight= 25*b*D/1e6
# factored load for strength design
w = 1.2*wG+1.5*wQ
Beam = SectionProperties.RectBeam(b, D)
fctf = 0.6*fc**0.5

MM = w*l**2/16e6
MR= -w*l**2/8e6

#mininum strength requirement
Z = Beam.Ig/D*2
Muomin = FlexuralStrength.Muomin(fctf, 0, 0, Beam.Ag, Beam.Ig, Z)
#compare Mu with the Muomin
phi = 0.85
MuM = MM/phi
MuR = MR/phi 
print("Mu at mid-span and the right end are {:.2f} and {:.2f}".format(MuM,MuR), 'kNm,respectively')
print("\n Muo min is {:.2f} kNm".format(Muomin))

# negative moment reinforcement at the center support
d = D-30 - 10-32/2
kuR = ReinforcementDesign.ku(fc, b,d, MuR)
Cc = ReinforcementDesign.Cc(fc, b, d, MuR)
AstR = Cc*1e3/fsy

#positve moment reinforcement
kuM = ReinforcementDesign.ku(fc, b,d, MuM)
CcM = ReinforcementDesign.Cc(fc, b, d, MuM)
AstM = CcM*1e3/fsy
#select the reuired tensile steel area
