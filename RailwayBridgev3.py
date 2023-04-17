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
l = 21 #bridge length, m
# lv = 12 #vehicle center length, m
fc = 40
fctf = 0.6*fc**0.5
fsy = 500
Es = 200e3
Ec = 30100
g = 9.83 #gravity, m/s2
# deflection limit
DeldivL = Design_Limits.Defl_Limits(1)
#Estimate of the self-weight
# basics, Warner, 2021
D = l/12*1e3
# assume depth of the flange
dpt_blst = 500 # m, depth of the ballast
l_slp = 2500 #m, sleeper length
tf = 3000
tw = max([D/3,800])
wblst = 1800*g*tf*dpt_blst/1e9
wslab = 18.6 
weight = 25*tw*D/1e6
# determine the maximum moment and shear force
y = np.linspace(0, l,200)
#self-weight and ballast track weight 
wG = 1.2*weight+1.7*wblst
MG = ActionEffects.UniformLoad(wG, l, y)

#horizontal forces
# braking force
Fbr = Design_Loads.BrakeForce(l, 1)[0]
#traction force
Ftr = Design_Loads.TractionForce(l, 1)[0]
Fbt = 5*[Fbr/5]+[-Ftr]
LD300LA = Design_Loads.M300LA(0,x_shift=(l-6.5)/2) 
yFbt = LD300LA['pos']+[LD300LA['pos'][-1]]
Mbt = ActionEffects.MomentLoad(Fbt,yFbt, l, y)
fig10 = plt.figure(10)
plt.subplot(211)
Design_Loads.pltAxles(LD300LA)
plt.xlim([0,l])
plt.ylim([0,6])
plt.yticks([])
plt.xlabel(None)
plt.subplot(212)
plt.plot(y,-Mbt.M)
plt.yticks([0,200,400],[0,-200,-400])
plt.xlim([0,l])
plt.xlabel('Longitudinal distance,m')
plt.ylabel('Moment,kNm')

#%% 300LA model 

step = 0.1
n = int((l-6.5)/step)+1
hf = 200
a = 2*hf

x_shift = 0
Mdmax = np.zeros(n)
Vdmax = np.zeros(n)
locmax = np.zeros(n)
ii = 0
phi = 1.6  # load factor for 300LA, Table D.1 of AS5100.2:2017, for ULS
alpha = Design_Loads.DLA(l).alpha_bending #dynamic load effect
fig1 = plt.figure(1)
plt.subplot(211)

while x_shift<=l-6.5:
    Md = np.zeros(len(y))
    Vd = np.zeros(len(y))
    # 300LA design load
    LD300LA = Design_Loads.M300LA(0,x_shift) 
    LADist = Design_Loads.LoadDist(l, 1, 1, hf/1000, dpt_blst/1000, l_slp/1000).M300LADist(LD300LA)
    for i in range((len(LD300LA['pos']))):
        start_pos = LADist[i][0]
        wdt = LADist[i][1]
        q = LADist[i][-1]
        Mobj = ActionEffects.UniformPartialSpanLoad(start_pos, wdt, q, l, y)
        Md = Md+(1+alpha)*phi*(Mobj.M)
        Vd = Vd+(1+alpha)*phi*(Mobj.V)
    Md = Md + MG.M
    Vd = Vd + MG.V
    Mdmax[ii]= max(Md)
    locmax[ii] = y[[i for i, m in enumerate(Md) if m ==max(Md)][0]]
    Vdmax[ii]= max(Vd)
    x_shift = x_shift+step
    plt.plot(y,-Md/500,y,-Vd/100)
    ii = ii+1 

#%%%

ind = [i for i, m in enumerate(Mdmax) if m ==max(Mdmax)][0]
x_shift0 = np.linspace(0, l-6.5,n)[ind]
print('Maximum moment occurs at {:.2f}m'.format(x_shift0))
print('Maximum shear force is {:.2f} kN'.format(max(Vdmax)))
#longitudinal location where the maximum is reached
xmax = locmax[ind]
print('The location where the maximum moment is reached is {:.2f}m'.format(xmax))


plt.xlabel('x,m')
plt.yticks([])
plt.subplot(212)
plt.subplots_adjust(hspace=0.3,top=0.9)
plt.plot(np.linspace(0, l-6.5,n),-Mdmax/max(Mdmax),np.linspace(0, l-6.5,n),-Vdmax/max(Vdmax),'--')
plt.gca().add_patch(pts.Rectangle((0,0),l-6.5, -0.1,color='grey'))
plt.xlabel('longitudinal shift, m')
plt.ylim([-1.2,0])
plt.yticks([])
plt.legend(['Moment','Shear Force'])


MG = ActionEffects.UniformLoad(wG, l,xmax)
LD300LA = Design_Loads.M300LA(0,x_shift0) 
#assume ku = 0.2 to obtain bd^2
phic = 0.6  # capacity reduction factor
ku = 0.2
alpha2 = FlexuralStrength.alpha2(fc)
gamma = FlexuralStrength.gamma(fc)

while abs(hf-a)>5:  
    Md = 0   
    LADist = Design_Loads.LoadDist(l, 1, 1, hf/1000, dpt_blst/1000, l_slp/1000).M300LADist(LD300LA)
    for i in range((len(LD300LA['pos']))):
        start_pos = LADist[i][0]
        wdt = LADist[i][1]
        q = LADist[i][-1]
        Mobj = ActionEffects.UniformPartialSpanLoad(start_pos, wdt, q, l, xmax)        
        Md = Md+(1+alpha)*phi*Mobj.M    
    Md = Md[0]+MG.M[0]
    Mu = Md/phi    
    bd2 = Mu*1e6/alpha2/gamma/fc/(1-gamma*ku/2)/ku
    print('The minimum bd2 is {:.2f} mm.'.format(bd2))
    d = (bd2/tf)**0.5
    print('The depth of the tensile force center is {:.2f} mm'.format(d))
    # d = 1400
    
    #check the compressive block depth, which should be within the flange    
    z = d-gamma*ku*d/2
    Cc = Mu*1e3/z
    a = Cc*1e3/alpha2/fc/tf
    print('The effective depth of the compressive block is {:.2f}mm'.format(a))
    print('The depth of the flange is {:.2f}mm'.format(hf))
    hf = (a+hf)/2

print('The effective depth of the compressive block is {:.2f}mm'.format(a))
print('The depth of the flange is {:.2f}mm'.format(hf))


Vd = np.zeros((2,2))
MG = ActionEffects.UniformLoad(wG, l,[0,l])
jj = 0
for x_shift in [0,l-6.5]:
    LD300LA = Design_Loads.M300LA(0,x_shift) 
    LADist = Design_Loads.LoadDist(l, 1, 1, hf/1000, dpt_blst/1000, l_slp/1000).M300LADist(LD300LA)
    for i in range((len(LD300LA['pos']))):
        start_pos = LADist[i][0]
        wdt = LADist[i][1]
        q = LADist[i][-1]
        Mobj = ActionEffects.UniformPartialSpanLoad(start_pos, wdt, q, l, [0,l])        
        Vd[jj,:] = Vd[jj,:]+(1+alpha)*phi*Mobj.V     
    jj = jj+1
Vd = Vd+MG.V[0]   
# choose the web width
twmin = 7.2*np.max(abs(Vd))*1e3/fc/d

# calculate the shear force at both ends of the span
bwmin = twmin+0.5*100
tw =  800
print('The minimum web width is {:.2f} mm, the final chosen web width is {:.2f}mm'.format(bwmin, tw))

#%% ---------------------------determine the prestress steel---------------------
# cross-section properties
Beam = SectionProperties.TBeamParam(tf, tw, hf, D)
wsw = 25*Beam.Ag/1e6  #self-weight
print('The revised self-weight is {:.2f} kN/m'.format(wsw))
# serviceability check
# determine the total load to be balanced by the prestressing steel
wo = wsw+wblst #UDL component
wobj = ActionEffects.UniformLoad(wo, l, y)
ld300la = Design_Loads.M300LA(0,x_shift0)
ld300dst = Design_Loads.LoadDist(l, 1, 1, hf/1e3, dpt_blst/1e3, l_slp/1e3).M300LADist(ld300la)
Md = np.zeros(len(y))
for i in range((len(ld300la['pos']))):
    start_pos = ld300dst[i][0]
    wdt = ld300dst[i][1]
    q = ld300dst[i][-1]
    Mobj = ActionEffects.UniformPartialSpanLoad(start_pos, wdt, q, l, y)  
    Md = Md+ 0.5*Mobj.M
Md = Md+wobj.M
fig3 = plt.figure(3)
plt.plot(y,-Md)         
plt.yticks(np.arange(0,-7000,-1000),np.arange(0,7000,1000))
Mo = max(Md)
Indo = [i for i, j in enumerate(Md) if j==max(Md)][0]
print('The maximum moment is {:.2f}kNm, which occurs at {:.2f}m from the left end'.\
      format(Mo,y[Indo]))
dp = 1500
e = dp-Beam.dnIg['dn']
Zb = Beam.dnIg['Ig']/(D-Beam.dnIg['dn'])
Pe = Mo*1e3/(e+Zb/Beam.Ag)

# prestress losses and cable selection 
eta = 0.8
Pi = Pe/eta
theta = 4*e/l/1e3 
mu = 0.2 
beta = 0.016 
Pij = Pi/(np.exp(-mu*(theta+beta*l/2)))



#------------------------------------------------------------------------------


# d = D-10-32/2-30 # the depth of the longitudinal tensile reinforecement in the web, 
# # 10mm, diameter of the stirrups, 32mm, diameter of the reinforcement bars, 30mm cover gap


# a = 0.5*hf #initialize the compressive block depth, less than hf to enable the iteration
# ii = 0  # count of the number of iterations

# while abs(hf-a)>1e-2:
#     ii = ii+1    
#     # deflection design load
#     DflDL = Design_Loads.DeflDL(0, l,x_shift= (l-6.5)/2)
#     # deflection design load distribution on the rail track deck    
#     ldist = Design_Loads.LoadDist(l, 1, 1, hf/1000, dpt_blst, l_slp)
#     DflDLDist = ldist.M300LADist(DflDL)           
#     # determine moment due to deflection design load 
#     y = np.linspace(0, l,200)
#     Md = np.zeros(len(y))
#     Vd = np.zeros(len(y))
#     for i in range((len(DflDL['pos']))):
#         start_pos = DflDLDist[i][0]
#         wdt = DflDLDist[i][1]
#         q = DflDLDist[i][-1]
#         Mobj = ActionEffects.UniformPartialSpanLoad(start_pos, wdt, q, l, y)
#         Md = Md+Mobj.M
#         
#     phi = 0.6
#     Mu = max(Md)/phi    
#     #calculate the compressive block depth
#     ku = ReinforcementDesign.ku(fc, tw, d, Mu)
#     Cc = ReinforcementDesign.Cc(fc, tw, d, Mu)
#     gamma = ReinforcementDesign.gamma(fc)
#     a = gamma*ku*d
#     # update hf
#     hf = (a+hf)/2
# print('the current iteration number is ', ii)    
# # compare a with assumed hf        
# print('The depth of the compressive block is {:.2f} and hf is {:.2f}'.format(a,hf))
# #T=Cc is the combined effect of tensile and prestressing steel
# Ast = Cc*1e3/fsy
# print('The area of the flexural tensile reinforncement is {:.2f}mm2'.format(Ast))
# ku = a/gamma/d
# dn = ku*d
# print('ku is {:.2f}, dn is {:.2f}mm'.format(ku,dn))

# # determine the depth again 


# #plot the axle locations
# theta = np.linspace(0,2*np.pi,20)
# fig1 = plt.figure(1)
# # plt.rcParams['figure.figsize']=(6,5)

# plt.subplot(211)
# plt.gca().add_patch(pts.Rectangle((0,0),l, 0.5,color='grey'))
# for i in range(len(DflDL['pos'])):
#     xx = DflDL['pos'][i]+0.45*np.cos(theta)
#     start_pos = DflDLDist[i][0]
#     wdt = DflDLDist[i][1]
#     yy = 1+0.5*np.sin(theta)    
#     plt.arrow(DflDL['pos'][i],3,0,-1,width=0.05,head_width=0.2,color='r')
#     plt.plot(xx,yy,'k')
#     plt.gca().add_patch(pts.Rectangle((start_pos,0),wdt, 1))
# plt.ylim([0,5])
# plt.plot(DflDL['pos'],DflDL['loads'],'ko')

# plt.xlim([0,l])
# ax = plt.gca()
# ax.set_aspect('equal', adjustable='box')

# plt.yticks([])

# plt.subplot(212)
# plt.plot(y,-Md/max(Md)*5,y,-Vd/max(Vd)*5)
# plt.gca().add_patch(pts.Rectangle((0,-0.5),l, 0.5,color='grey'))
# plt.yticks([])
# plt.xlabel('x,m')
# plt.xlim([0,l])
# plt.legend(['Moment','Shear Force'])
# plt.subplots_adjust(top=1)
# plt.show()


# # design load
# Beam = SectionProperties.TBeamParam(tf, tw, hf, D)
# Ag = Beam.Ag
# Ig = Beam.dnIg['Ig']
# Z = Ig/(D-dn)
# # determine SLS
# weight = 25*Beam.Ag/1e6  
# Muomin =FlexuralStrength.Muomin(fctf, 0, 0, Ag, Ig, Z)

# #design shear and torsion reinforcement




