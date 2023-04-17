# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 17:25:19 2023

@author: wenxuli
"""
import os
os.chdir(os.path.dirname(__file__))

from Bridge_design_lib import SectionProperties, FlexuralStrength, Serviceability

tf = 1000
tw = 300
hf = 120
h = 800
Asc = 2170
Ast = 3720
dst = 800 -90
dsc = 60
Es = 200e3
Ec = 30100
fc = 32
psis = 0.7
psil = 0.4
n = Es/Ec
l = 9e3
    
wG = 60
wQ = 40

ws = wG+psis*wQ
wl = wG+psil*wQ
    
#check the beam is cracked under the loading condition
#at mid span, tensional section
mTBeam = SectionProperties.TBeamParam(tf, tw, hf, h, \
                                     Ast=Ast,dst=dst,Asc=Asc,dsc=dsc, Es=Es, Ec=Ec)
# creep factor 
kcs = Serviceability.kcs(Asc, Ast)
#compressive section    
Asc = 1860
Ast = 5600
dsc = 60
dst = h-60
    
rTBeam = SectionProperties.RectBeam(tw,h,Ast=Ast,dst=dst,Asc=Asc,dsc=dsc, Es=Es, Ec=Ec)

Iefav = (mTBeam.Icr['Icr']+rTBeam.Icr['Icr'])/2
ML = 0
# short term deflection 
MM = ws*l**2/16e6
MR = -ws*l**2/8e6
Deltas = l**2/96/Ec/Iefav*(ML+10*MM+MR)*1e6

# long term deflection 
MMl = wl*l**2/16e6
MRl = -wl*l**2/8e6

Deltal = l**2/96/Ec/Iefav*(ML+10*MMl+MRl)*1e6

print("The short- and long-term deflections are {:.2f} and {:.2f}".format(Deltas,Deltal),' respectively')

# mid span deflection 
Delta = Deltas+kcs*Deltal
print('The total deflection at the mid span is {:.2f}'.format(Delta))

