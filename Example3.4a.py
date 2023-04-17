# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 08:03:43 2023

@author: wenxuli
"""
from Bridge_design_lib import SectionProperties, Serviceability 

wG = 60
wQ = 40
fc = 32
Ec = 30100
Es = 200e3
psis = 0.7
psil = 0.4
epsiloncs = 800e-6

tf = 1000
hf = 120
tw = 300
h = 800
l = 9e3
# design load 
ws = wG+psis*wQ 
wl = wG+psil*wQ
# tensional side 
dst = h - 90
dsc = 60
Asc = 2170
Ast = 3720
Beamt = SectionProperties.TBeamParam(tf, tw, hf, h, Asc =Asc,dsc =dsc,Ast=Ast,dst = dst,Es=Es,Ec=Ec)
Ief1 = Beamt.Icr['Icr']
kcs = Serviceability.kcs(Asc, Ast)
# compressive side
dsc = 60
dst = h - 60
Asc = 1860
Ast = 5600
Beamc = SectionProperties.RectBeam(tw, h, Asc=Asc,dsc=dsc,Ast=Ast,dst=dst,Es=Es,Ec=Ec )
Ief2 = Beamc.Icr['Icr']
Iefav = (Ief1+Ief2)/2
# short term deflection
MLs = 0
MMs = ws*l**2/16e6
MRs = -ws*l**2/8e6
Deltas = l**2/96/Ec/Iefav*(MLs+10*MMs+MRs)*1e6
# long term deflection
MLl = 0
MMl = wl*l**2/16e6
MRl = -wl*l**2/8e6
Deltal = l**2/96/Ec/Iefav*(MLl+10*MMl+MRl)*1e6

# overall deflection
Delta = Deltas+kcs*Deltal
print("The short- and long-term deflections are {:.2f} and {:.2f}".format(Deltas,Deltal),' respectively')
print('The total deflection at the mid span is {:.2f}'.format(Delta))

