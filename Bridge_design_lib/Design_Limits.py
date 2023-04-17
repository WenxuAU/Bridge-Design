# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 21:38:36 2023

@author: wenxuli
"""


'''thresholds'''
#%% Serviceablity design limits
def Defl_Limits(l_bridge,bridge_type=2):
    '''Section 9.10 of AS5100.2: deflection limit
    For SLS test, under the traffic load dynamic load allowance.
    bridge_type: 1/320: cantilever type; 1/640: others;
    len_bridge: the length of the bridge'''
    if bridge_type ==1:
        '''cantilever'''
        '''the bridge is subject o '''
        return l_bridge/320.
    else:
        return l_bridge/640. 
''' requirements about hogging and sagging are ignored here'''
# def Cracking_Limits():
    


#%% Fatigue design limits
# def CompressionStrength_Beam(fc,sigma_min):
#     '''Section  2.2.2. of AS5100.5: concrete compressive stress limit
#     fc: chacteristic compressive (cyliner) strength of concrete at 28 days
#     sigma_min: minimum compressive stress at the extreme fibers under consideration, 0 if in tension'''
#     return 0.45*fc*(fc-sigma_min)/fc
# def ShearStrength_Beam(IsPressed):
#     '''Section  2.2.3. of AS5100.5: shear stress limit
#     '''
#     if not IsPressed:
#         if Asv<Asv_min:
#             kv=200/(100+1.3*dv)
#             if kv>0.10: kv =0.1
#         else:
#             kv=0.15
# def TensileStrength_Reinforcement(di,db,n):
#     '''Tensile strength of reinforcement based on Table 2.2.5 of AS5100.5, in MPa
#     db: nomial diameter of a reinforcing bar;
#     di: nominal internal diameter of reinforcement bend or hook;
#     n: design number of stress cycles, determined by NoOfStressCycles() of Fatigue_Loads.py'''
#     s = 150*(0.35+0.26*di/db)
#     alphaf = (2e6/n)**(1/3)
#     if alphaf<0.74: alphaf=0.74
#     return alphaf*f
    
    