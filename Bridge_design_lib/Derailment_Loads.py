# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 11:25:43 2023

@author: wenxuli
"""


'''Derailment loads'''
from Design_Loads import M300LA
def CaseA(Lv,gauge,x_shift=0,y_shift=0):
    
    ''' 
          /_____________bf________________/
      /    
      |   |------------------------------|
      tf  |                              |
      |   |------------------------------|
      /              |        |
      |              |        |
      hw             |        |
      |              |        |
      /              |        |
                     |________|
                     /---tw--/
                     
                          /\ x                  
                          /
                         /
                        /
                       /  
                       ----------------->y
    '''
    '''Load case A according to Section 11.5.3 of AS 5100.2.
    Principle: shifting the 300LA loads laterally;
    span: the distance between successive axle group centers, i.e. vehicle length, in meters;
    gauge: track gauge width
    x_shift: the shift of the axle group starting point longitudinally along the bridge
    y_shift: the shift of the axle group horizontally across the bridge
    two siutations are included in CASE A:
    1) based on 300LA model where the load is allowed to be shifted laterally within 
    a range of 1.5*track gauge from the track centreline
    2) a point load of 200kN at any position on the bridge surface
    '''
    if y_shift >1.5*gauge:
        y_shift = 1.5*gauge    
    loads = M300LA(Lv,x_shift)
    return ({'pos':loads['pos'],'loads':loads['loads'],'yshift':y_shift},
            {'load':200e3,'xshift':x_shift,'yshift':y_shift})

def CaseB(bf,L,gauge,x_shift=0):
    '''Load case B according to Section 11.5.3 of AS 5100.2.
    bf: width of the bridge surface, see def in the Input_Data file'''
    '''The units of load is kN, the length is in meters
    L: the length of the bridge, in metres
    gauge: track gauge width, in metres
    x_shift: the longitudinal shift of the UDL when L>20'''
    if L<20:
        span = L
        start_pos = 0
    else:
        span = 20
        start_pos = 0
    if x_shift+span>L:
        span = 20
        start_pos = L-20
    if x_shift+span<20 and L>20:
        span = 20
        start_pos = 0
    loads=[(start_pos,span,100e3),{'load':100e3,'length':span,'yshift':bf/2-gauge/2.}]
    return loads



