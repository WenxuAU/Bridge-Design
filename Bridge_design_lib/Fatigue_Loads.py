# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 21:20:36 2023

@author: wenxuli
"""


'''fatigue load'''
from Load_Distribution import LoadDistrubtion


def CT(Track_Category):
    ''''Section 9.8.2 of AS5100.2
    CT: base number of load cycles for the track catergory, given by Table 9.8.4'''
    if Track_Category==1:
        '''heavy haul freight'''
        return 6.0e7
    elif Track_Category==2:
        '''all passenger and light rail lines'''
        return 1.0e5
    elif Track_Category==3:
        '''main line freight'''
        return 1.0e5
    else:
        '''branch line freight'''
        return 1.0e4
    
def nT(Lv,Lf):
    ''''Section 9.8.3 of AS5100.2
    nT; number of equivalent stress cyles of amplitude f' per train'
    Lv: distance between centers of axle groups or the length of a vehicle
    Lf: span of main girders, trusses or stringers; or 
    cross-girder spacing for cross-girders, given by Table 9.8.3'''
    if Lf<2.5:
        nT=240
    elif Lf<9.0 and Lf>2.5:
        nT= 60*((2*Lv-Lf)/Lf)**3+2
        if nT>60: nT=60
        if nT<2: nT=2
    else:
        nT=2.0
    return nT

def NoOfStressCycles(**kwargs):
    '''Section 9.8.3 of AS5100.2
    the output is the Effective number of stress cycles(n);
    The inputs have to be three keywords: 
        Track_Category: 1,2,3,else;
        Lv: distance between centers of axle groups or the length of a vehicle;
        Lf:  span of main girders, trusses or stringers; or 
        cross-girder spacing for cross-girders, given by Table 9.8.3'''
        
    inputs = list(kwargs.values())
    if len(inputs)!=2:
        raise ValueError("Error: Two inputs are required: 1st is the Track_category and \
              the 2nd is the Lf")
    else:
        return CT(inputs[0])*nT(inputs[1],inputs[2])

def FatigueDesignStressRange(max_stress, min_stress):
    '''Section 9.8.2 of AS5100.2: Fatigue design stress range,f*
    max_stress: the max stress under he fatigue design traffic load
    min_stress: the min stress....
    '''
    return (max_stress-min_stress)
    
    