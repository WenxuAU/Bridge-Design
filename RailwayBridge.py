# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 15:33:24 2023

@author: wenxuli
"""

from Bridge_design_lib import Design_Loads, Design_Limits, SectionProperties, \
    ActionEffects, ReinforcementDesign,FlexuralStrength
    
from matplotlib import pyplot as plt
from matplotlib import patches as pts
import numpy as np
l = 20 #bridge length, m
lv = 12 #vehicle center length, m
fc = 32
fctf = 0.6*fc**0.5
fsy = 500
Es = 200e3
Ec = 30100

# deflection limit
DeldivL = Design_Limits.Defl_Limits(1)
#Initial guess of the depth of T-beam, accordign to Table C.1 of Reinforced Concrete
# basics, Warner, 2021
D = l/12*1e3
# assume depth of the flange
tw = 0.4*D  # no basis for this choice
tf = 2400
hf = 200

d = D-10-32/2-30 # the depth of the longitudinal tensile reinforecement in the web, 
# 10mm, diameter of the stirrups, 32mm, diameter of the reinforcement bars, 30mm cover gap

dpt_blst = 0.6 # m, depth of the ballast
l_slp = 2 #m, sleeper length

a = 0.5*hf #initialize the compressive block depth, less than hf to enable the iteration
ii = 0  # count of the number of iterations

while abs(hf-a)>1e-2:
    ii = ii+1    
    # deflection design load
    DflDL = Design_Loads.DeflDL(0, l,x_shift= (l-6.5)/2)
    # deflection design load distribution on the rail track deck    
    ldist = Design_Loads.LoadDist(l, 1, 1, hf/1000, dpt_blst, l_slp)
    DflDLDist = ldist.M300LADist(DflDL)           
    # determine moment due to deflection design load 
    y = np.linspace(0, l,200)
    Md = np.zeros(len(y))
    Vd = np.zeros(len(y))
    for i in range((len(DflDL['pos']))):
        start_pos = DflDLDist[i][0]
        wdt = DflDLDist[i][1]
        q = DflDLDist[i][-1]
        Mobj = ActionEffects.UniformPartialSpanLoad(start_pos, wdt, q, l, y)
        Md = Md+Mobj.M
        Vd = Vd+Mobj.V
    phi = 0.6
    Mu = max(Md)/phi    
    #calculate the compressive block depth
    ku = ReinforcementDesign.ku(fc, tw, d, Mu)
    Cc = ReinforcementDesign.Cc(fc, tw, d, Mu)
    gamma = ReinforcementDesign.gamma(fc)
    a = gamma*ku*d
    # update hf
    hf = (a+hf)/2
print('the current iteration number is ', ii)    
# compare a with assumed hf        
print('The depth of the compressive block is {:.2f} and hf is {:.2f}'.format(a,hf))
#T=Cc is the combined effect of tensile and prestressing steel
Ast = Cc*1e3/fsy
print('The area of the flexural tensile reinforncement is {:.2f}mm2'.format(Ast))
ku = a/gamma/d
dn = ku*d
print('ku is {:.2f}, dn is {:.2f}mm'.format(ku,dn))

# determine the depth again 


#plot the axle locations
theta = np.linspace(0,2*np.pi,20)
fig1 = plt.figure(1)
# plt.rcParams['figure.figsize']=(6,5)

plt.subplot(211)
plt.gca().add_patch(pts.Rectangle((0,0),l, 0.5,color='grey'))
for i in range(len(DflDL['pos'])):
    xx = DflDL['pos'][i]+0.45*np.cos(theta)
    start_pos = DflDLDist[i][0]
    wdt = DflDLDist[i][1]
    yy = 1+0.5*np.sin(theta)    
    plt.arrow(DflDL['pos'][i],3,0,-1,width=0.05,head_width=0.2,color='r')
    plt.plot(xx,yy,'k')
    plt.gca().add_patch(pts.Rectangle((start_pos,0),wdt, 1))
plt.ylim([0,5])
plt.plot(DflDL['pos'],DflDL['loads'],'ko')

plt.xlim([0,l])
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

plt.yticks([])

plt.subplot(212)
plt.plot(y,-Md/max(Md)*5,y,-Vd/max(Vd)*5)
plt.gca().add_patch(pts.Rectangle((0,-0.5),l, 0.5,color='grey'))
plt.yticks([])
plt.xlabel('x,m')
plt.xlim([0,l])
plt.legend(['Moment','Shear Force'])
plt.subplots_adjust(top=1)
plt.show()


# design load
Beam = SectionProperties.TBeamParam(tf, tw, hf, D)
Ag = Beam.Ag
Ig = Beam.dnIg['Ig']
Z = Ig/(D-dn)
# determine SLS
weight = 25*Beam.Ag/1e6  
Muomin =FlexuralStrength.Muomin(fctf, 0, 0, Ag, Ig, Z)

#design shear and torsion reinforcement




