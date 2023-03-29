# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 19:04:40 2023

@author: wenxuli
"""


'''load distribution'''
from design_loads import FatigueDesignTrafficLoad

class LoadDistribution:
    def __init__(self,TrackForm,track_no,axle_spacing,dis_sleeper_beam,depth_slab,
                depth_ballast,width_sleeper,span,dis_tracks=0):
        self.TrackForm = TrackForm
        self.track_no = track_no
        self.axle_spacing = axle_spacing
        self.dis_sleeper_beam = dis_sleeper_beam
        self.depth_slab = depth_slab
        self.depth_ballast = depth_ballast
        self.width_sleeper = width_sleeper
        self.dis_tracks = dis_tracks
        self.span = span
        self.FatigueLoads = FatigueDesignTrafficLoad(span)
    def DistributionLengthWidth(self):
        if self.TrackForm==1:
            # ballasted track on concrete bridge     
            self.width=self.width_sleeper
            self.length = 1.1+self.depth_ballast+2*self.depth_slab
            if self.length>self.axle_spacing:
                self.length = self.axle_spacing                
                self.width = self.width_sleeper+self.dis_sleeper_beam+2*self.depth_slab
            '''in the case of multiple tracks on the bridge'''
            if self.track_no>1:
                if self.width>self.dis_tracks:
                    self.width=self.dis_tracks
    # if TrackForm==2:
        # '''direct fixation track'''
       
        # '''
        # ??????how to determine the load distribution on this type of bridge???????
        # '''
    def FatigueLoadDistribution(self):
        self.FatigueLoadsDistribution['x'] = []
        for i in range(len(self.FatigueLoads['pos'])):
            start_pos = self.FatigueLoads['pos'](1-1/self.width*2)
            length = self.length
            magitude = self.FatigueLoads['loads'][i]
            if start_pos < 0:
                start_pos = 0
            if start_pos>self.span:
                raise ValueError('The setting of 300LA model is not correct!')
            self.FatigueLoadsDistribed=self.FatigueLoadsDistribed+(start_pos,length,magitude)