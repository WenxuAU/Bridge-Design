# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 21:42:19 2023

@author: wenxuli
"""


class Object:
    pass 

'''load factors for ULS, SLS and Fatigue limit state design loads'''
def LoadactorsVertical():
    '''for 300LA rail traffic load'''
    return {'ULS':1.6,'SLS':1.0,'FLS':1.0}
def LoadFactorsHorizontal():
    '''load factors for longitudinal and traction forces and nosing forces are considered
    here'''
    return {'ULS':1.6,'SLS':1.0}


class LoadFactors:
    def __init__(self):
        self.ULS = Object()
        self.SLS = Object()
        self.FDL = Object()
    def PermanentLoad(self):        
        self.ULS.concrete = 1.2
        self.ULS.ballasttrack = 1.7
        self.ULS.concreteslab=2.0
        self.ULS.shrinkcreep = 1.2
        self.ULS.prestress = 1.0
    def TransientLoad(self):
        self.ULS.M300LA  = 1.6
        self.ULS.braketraction = 1.6
        self.ULS.derailment = 1.0
        self.ULS.prestress2nd = 1.0
        self.ULS.prestresstransfer = 1.0
        

        
        