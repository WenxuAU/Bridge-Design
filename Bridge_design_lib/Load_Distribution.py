# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 19:04:40 2023

@author: wenxuli
"""


'''load distribution'''
from Bridge_design_lib.Design_Loads import FLS
from Bridge_design_lib.Derailment_Loads import CaseA, CaseB
class Object:
    pass

class LoadDist:
    '''Section 9.6 of AS5100.2
    '''
    def __init__(self,trk_fm,trk_no,dpt_slab,dpt_blst,
                 l_slp,dis_trks=0):
        '''TrackForm: 1, ballasted deck concrete rail bridges; 2. Direct fixation 
        track_no: number of tracks on the bridge
        depth_slab: the depth of the concrete slab
        depth_ballast: the depth of ballast from the bottom of sleepers
        length_sleeper: the length of the sleeper
        dis_tracks: distance between track centrelines in the case of multiple tracks
        '''
        self.trk_fm = trk_fm
        self.trk_no = trk_no      
        self.dpt_slab = dpt_slab
        self.dpt_blst = dpt_blst
        self.l_slp = l_slp
        self.dis_trks = dis_trks

    def DistSize(self,axle_spacing):
        '''Section 9.6.4 of AS 5100.2
        axle_spacing: distance btween neighbouring axles
        '''
        if self.trk_fm==1:
            '''Section 9.6.4 of AS5100.2:ballasted track on concrete bridge '''
            self.w=self.l_slp + self.dpt_blst + 2*self.dpt_slab
            self.l = 1.1+self.dpt_blst+2*self.dpt_slab
            if self.l>axle_spacing:
                self.l = axle_spacing                
            '''in the case of multiple tracks on the bridge'''
            if self.trk_no>1:
                if self.w>self.dis_trks:
                    self.w=self.dis_trks
        if self.track_fm==2:
           '''direct fixation track: assume uniform distribution along the track'''
           
       
        # '''
        # ??????how to determine the load distribution on this type of bridge???????
        # '''
           pass
    def M300LADist(self,Lv,L,discount,x_shift):
        '''
        The effect of 300LA on the bridge deck, as opposed to that on the railway track, i.e. further 
        transmission downwards to the bridge deck.
        Lv: the span between axle group centres, i.e. vehicle length,in metres, between 12 and 20m
        L: the characteristic lengtho of a bridge component, e.g. bridge length
        x_shift: the shift of the first axle group starting point longitudinally along the bridge;
        Output:
            [(Start_position of the partially UDL; length of the UDL, magnitude of the load density),
             (2nd partially UDL)，
             （3rd partially UDL）,...] 
        discount: to discount the effect of loading from dynamic load allowance'''
        
        if type(Lv) is not list:
            Lv = [Lv]
        
        tmp = [] # initialization
        
        FatigueLoads = FLS(Lv,L,discount,x_shift)
        
        axle_pos = FatigueLoads['pos']
        axle_no = len(axle_pos)
        axle_spacings1 = [FatigueLoads['pos'][i+1]-FatigueLoads['pos'][i] for 
                         i in range(axle_no-1)]
        if len(Lv)>1:
            axle_spacings1=axle_spacings1+[min([Lv[-1],L-FatigueLoads['pos'][-1]])]    
        else:
            axle_spacings1=axle_spacings1+[L-FatigueLoads['pos'][-1]] 
        axle_spacings2 = [FatigueLoads['pos'][0]]+[FatigueLoads['pos'][i]-FatigueLoads['pos'][i-1] for 
                         i in range(1,axle_no)]
        axle_spacings = [axle_spacings1[0]]+[min([axle_spacings1[i],axle_spacings2[i]]) for i in range(1,axle_no)]
        # print('axle spacings are:',axle_spacings1, axle_spacings2,axle_spacings)
        for i in range(axle_no):
            self.DistSize(axle_spacings[i])
            start_pos = FatigueLoads['pos'][i]-self.l/2
            l = self.l
            # print('i,l,start_pos',i,l,start_pos)
            magitude = FatigueLoads['loads'][i]/l
            if start_pos < 0:
                start_pos = 0
            if start_pos > L:
                raise ValueError('The setting of 300LA model is not correct!')
            tmp=tmp+[(start_pos,l,magitude)]
        return tmp
        
    def FatigueLoadsOnBr(self,Lv,L,x_shift):        
        '''Lv: the span between axle group centres, i.e. vehicle length,in metres, between 12 and 20m
        L: the characteristic lengtho of a bridge component, e.g. bridge length
        x_shift: the shift of the first axle group starting point longitudinally along the bridge;
        Output:
            [(Start_position of the partially UDL; length of the UDL, magnitude of the load density),
             (2nd partially UDL)，
             （3rd partially UDL）,...] 
        '''      
    
        self.FatigueLoads = self.M300LAOnBr(Lv,L,0.5,x_shift) #discount: default to 0.5
      
    def DerailmentLoadonBr(self,Lv,L,bf,gauge,x_shift,y_shift):
        
        '''Derailment load acting on the bridge surface, as opposed to that on the railway track.
        Case A: 2 situations: 1: 300LA with lateral shift; 2: a point load of 200kN;
        Case B: a distributed load of 100kN of 20 m long;
        option: 1: Case A sitaution 1; 2, CaseA situation 2; 3, CaseB'''
        self.DerailmentLoads = Object()
        self.DerailmentLoads.blst = Object()
        self.DerailmentLoads.slab = Object()
        loadCaseA = CaseA(Lv,gauge,x_shift,y_shift)  
        self.DerailmentLoads.blst.CaseA2 = loadCaseA[1]                                     
        self.DerailmentLoads.blst.CaseA1 = self.M300LAOnBr(Lv,L,0,x_shift)#No DLA considered
        self.DerailmentLoads.blst.CaseB = CaseB(bf,L,gauge,y_shift)
        
        #-------------------load distribution-----------------------------
        #-----------------------not finished for slab track---------------
        self.DerailmentLoads.slab.CaseA1 = sum(
            [j[1]*j[2] for j in self.M300LAOnBr(Lv,L,0,x_shift)])/L
        self.DerailmentLoads.slab.CaseA2 =  loadCaseA[1]
        self.DerailmentLoads.slab.CaseB =  CaseB(bf,L,gauge,y_shift)
        
        
            
            
    
            
    
