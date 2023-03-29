# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:13:51 2023

@author: wenxuli
"""


'''the main code for designing the bridge'''
'''
1. the bridge is simply supported
2. the bridge length is l
3. the bridge is T-sectined

'''
#%% change to the working directory
import os
dir_name = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_name)
#%%
import numpy as np
from matplotlib import pyplot as plt
from Bridge_design_lib.Design_Loads import M300LA,FLS
from Bridge_design_lib.Loading_Effects import PointLoad, UniformLoad, UniformPartialSpanLoad
from Bridge_design_lib.Load_Distribution import LoadDist
#%% input data 
from Bridge_design_lib.Input_Data import InputData 
trk_form = 1
Inputs = InputData(bf=4)
Inputs.Blst()
# initial parameters
N = 500  # number of positions to be looked at along the bridge
x_shift = 0 #the shift of the first axle group starting point longitudinally along the bridge
trk_no =1

#%% Fatigue traffic design laod
LoadDistCase = LoadDist(trk_form, trk_no, 0.3, Inputs.blst.h, Inputs.l_sleeper)
LoadDistCase.FatigueLoadsOnBr(Inputs.Lv,Inputs.L,x_shift)
FatigueLoadsFinal = LoadDistCase.FatigueLoads
Mom = np.zeros(N)
sigma = np.zeros(N)
epsilon = np.zeros(N)
Defl = np.zeros(N)
SF = np.zeros(N)
yp = np.linspace(0,Inputs.L,N) #locations to calculate moments, stresses, strains and deflections
for k,y in enumerate(yp):
    for i in range(len(FatigueLoadsFinal)):
        tmp=UniformPartialSpanLoad(FatigueLoadsFinal[i][0], FatigueLoadsFinal[i][1], 
                                   FatigueLoadsFinal[i][2], Inputs.L, y, 0.2, 20, 1e3)
        # print(tmp.M)
        Mom[k] = Mom[k]+tmp.M
        sigma[k] = sigma[k]+tmp.Sigma    
        epsilon[k] = epsilon[k]+tmp.Strain
        SF[k] = SF[k]+tmp.SF
        Defl[k] = Defl[k]+tmp.Defl
plt.plot(yp,Mom,yp,SF,yp,Defl,'b--')      
plt.xlabel('x,m')
plt.legend(['Moment','Shear Force','Deflection'])     
#plot the load distribution density0.85*25*1100
# figure2= plt.figure(3)
for i in range(len(FatigueLoadsFinal)):
    start_pos = FatigueLoadsFinal[i][0]
    end_pos = start_pos+FatigueLoadsFinal[i][1]
    load = FatigueLoadsFinal[i][2]
    plt.plot([start_pos,end_pos],[load,load])
#%% braking and traction force
#assuming the inflenece distance is known
from Bridge_design_lib.Loading_Effects import MomLoad, TorsionLoad    
from Bridge_design_lib.Design_Loads import TractionForce, BrakeForce, NosingLoad
vehicle_no = len(FatigueLoadsFinal)/5
Brake = BrakeForce(Inputs.L,vehicle_no)
Traction = TractionForce(Inputs.L,vehicle_no)
BTMom = np.zeros(N)
BT_sigma = np.zeros(N)
BT_epsilon = np.zeros(N)
BT_defl = np.zeros(N)
BTSF = np.zeros(N)
for k,y in enumerate(yp):
    tmp = MomLoad(Brake,Inputs.h_brake,y,Inputs.L,0.2,20,1e3)
    tmp1 = MomLoad(Traction,Inputs.h_traction,y,Inputs.L,0.2,20,1e3)    
    BTMom[k] = tmp.M +tmp1.M
    BTSF[k] = tmp.SF+tmp1.SF
    BT_sigma[k] = tmp.Sigma+tmp1.Sigma
    BT_epsilon[k] = tmp.Strain+tmp1.Strain
    BT_defl[k] = tmp.Defl+tmp1.Defl
plt.plot(yp,BTMom,yp,BTSF,yp,BT_defl,'b--')      
plt.xlabel('x,m')
plt.legend(['Moment','Shear Force','Deflection'])         
#%% nosing load
Nosing = TorsionLoad(100e3,Inputs.h_rail)
#%% derailment load
x_shift = 0
y_shift = 2
LoadDistCase.DerailmentLoadonBr(Inputs.Lv,Inputs.L, Inputs.bf,
                                            Inputs.gauge, x_shift, y_shift)
#Case A: based on 300LA, a distributed load with lateral shift 
loadsCaseA1 = LoadDistCase.DerailmentLoadsCaseA1
loadsCaseA2 = LoadDistCase.DerailmentLoadsCaseA2
loadsCaseB = LoadDistCase.DerailmentLoadsCaseB
DA_Mom = np.zeros(N)
DA_sigma = np.zeros(N)
DA_epsilon = np.zeros(N)
DA_defl = np.zeros(N)
DA_SF = np.zeros(N)
for k,y in enumerate(yp):   
    for i in range(len(loadsCaseA1)):
        tmp=UniformPartialSpanLoad(loadsCaseA1[i][0], loadsCaseA1[i][1], 
                                   loadsCaseA1[i][2], Inputs.L, y, 0.2, 20, 1e3)
        # print(tmp.M)
        DA_Mom[k] = DA_Mom[k]+tmp.M
        DA_sigma[k] = DA_sigma[k]+tmp.Sigma    
        DA_epsilon[k] = DA_epsilon[k]+tmp.Strain
        DA_SF[k] = DA_SF[k]+tmp.SF
        DA_defl[k] = DA_defl[k]+tmp.Defl
#CaseA: the y_shift caused eccentricity, here assume yshift >=gauge/2
TorsionLoad(loadsCaseA2['load'],loadsCaseA2['yshift']*2+Inputs.gauge)

#CaseB
DB_Mom = np.zeros(N)
DB_sigma = np.zeros(N)
DB_epsilon = np.zeros(N)
DB_defl = np.zeros(N)
DB_SF = np.zeros(N)
for k,y in enumerate(yp):
    tmp=UniformPartialSpanLoad(loadsCaseB[0][0], loadsCaseB[0][1], 
                               loadsCaseB[0][2], Inputs.L, y, 0.2, 20, 1e3)
    # print(tmp.M)
    DB_Mom[k] = DB_Mom[k]+tmp.M
    DB_sigma[k] = DB_sigma[k]+tmp.Sigma    
    DB_epsilon[k] = DB_epsilon[k]+tmp.Strain
    DB_SF[k] = DB_SF[k]+tmp.SF
    DB_defl[k] = DB_defl[k]+tmp.defl
#CaseB: the y_shift caused eccentricity, here assume yshift >=gauge/2
TorsionLoad(loadsCaseB[1]['load']*loadsCaseB[1]['length'],loadsCaseB[1]['yshift'])


#%% load combination: ballasted track
from Bridge_design_lib.Load_Factors_Combination import ULSLoadComb, SLSLoadComb
# ULS load combination
bf = 3
depth_slab = 0.3
dst_trks = 0
ULSloads = ULSLoadComb(bf,trk_no,depth_slab,dst_trks,x_shift,y_shift=1.2)
#SLS load combination
SLSloads = SLSLoadComb(bf,trk_no,depth_slab,dst_trks,x_shift,y_shift=1.2)
ULS_Mom = np.zeros(N)
ULS_sigma = np.zeros(N)
ULS_epsilon = np.zeros(N)
ULS_defl = np.zeros(N)
ULS_SF = np.zeros(N)
z = 0.2
I = 20
E = 1e3
for k,y in enumerate(yp):
    # effect of the dead load, self weight is not considered yet.========
    tmp1 = UniformLoad(ULSloads['DeadLoad'],Inputs.L,y,z, I, E) # effects due to dead load
    for i in range(len(ULSloads['FatigueLoad'])):
        # effect of the fatigue load
        tmp2=UniformPartialSpanLoad(ULSloads['FatigueLoad'][i][0], 
                                    ULSloads['FatigueLoad'][i][1], 
                                    ULSloads['FatigueLoad'][i][2], 
                                    Inputs.L, y, z, I, E)
        # effect of the derailment load
        tmp3 = UniformPartialSpanLoad(ULSloads['DerailmentLoadCaseA1'][i][0], 
                                      ULSloads['DerailmentLoadCaseA1'][i][1], 
                                      ULSloads['DerailmentLoadCaseA1'][i][2], 
                                      Inputs.L, y, z, I, E)
        
        
        ULS_Mom[k] = ULS_Mom[k]+tmp1.M+tmp2.M +tmp3.M
        ULS_sigma[k] = ULS_sigma[k]+tmp1.Sigma+tmp2.Sigma + tmp3.Sigma
        ULS_epsilon[k] = ULS_epsilon[k] + tmp1.Strain+tmp2.Strain + tmp3.Strain
        ULS_SF[k] = ULS_SF[k] +tmp1.SF+tmp2.SF + tmp3.SF
        ULS_defl[k] = ULS_defl[k] + tmp1.Defl+tmp2.Defl + tmp3.Defl
plt.plot(yp,ULS_Mom,yp,ULS_SF,yp,ULS_defl,'b--')      
plt.xlabel('x,m')
plt.legend(['Moment','Shear Force','Deflection'])    

for i in range(len(ULSloads['FatigueLoad'])):
    start_pos = ULSloads['FatigueLoad'][i][0]
    end_pos = start_pos+ULSloads['FatigueLoad'][i][1]
    load = ULSloads['FatigueLoad'][i][2]
    plt.plot([start_pos,end_pos],[load,load])


#%% strength design
'''In accordance with Section 2.3 of AS5100.5'''
# need to look at the prestress and reinforcement




 
    

