# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 09:16:02 2023

@author: wenxuli
"""

'''the input data for the model'''
class Object():
    pass
g = 9.83
class InputData:    
    def __init__(self,bf=0,tf=0,hw=0,tw=0):        
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
                  
        ======================Inputs:==========================================
        bf: flange width, in meters
        hf: flange height, in m
        hw: web height, in m
        tw: web width,in m        
        =====================Outputs:==========================================
        ballast.h: ballast depth, in metres
        ballast.rho: ballast density, N/m3
        ballast.bt: tope width of the ballast, in m
        ballast.b: mean ballast width, in m
        ballast.w: ballast weight per meter, N/m
        
        
        concrete.slab.b: concrete slab width, in m
        concrete.slab.h: concrete slab height, in m
        concrete.slab.w: concrete slab weight per metre, N/m
        concrete.rho: concrete density, in N/m3
        concrete.v: Poisson's ratio, section 3.1.5 of AS5100.5
        concrete.fc: chracteristic compressive strength, in MPa, at 28 days
        concrete.fctf: flexural tensile strength, in MPa
        concrete.fct: uniaxial tensile strength, in MPa    
                
        gauge: track gauge, standard gauge, in metres
        h_rail : rail height, Chosen to be a UIC60 [m]
        L: bridge length
        Lv: distance between axle group centers
        l_slp: sleeper length
        
        h_traction: the height of the traction application point from the rail head
        h_brake: the height of brake application point from the rail head
        ======================================================================
        '''
        self.bf = bf
        self.tw = tw
        self.tf = tf
        self.hw = hw
        #% vehicle parameters        
        self.Lv = 12 
        #% bridge parameters
        self.L = 40 
        #% track parameters, generic 
        self.h_rail = 0.172 
        self.gauge = 1.435  
        self.trk_no = 1
        self.l_slp = 2  
        #% parameters of ballassted and ballastless track              
        self.h_traction = 0.9+self.h_rail
        self.h_brake = 2.0 + self.h_rail
    def Blst(self):
        '''return ballast depth
        1: ballasted track; otherwise: ballastless track'''
        self.blst = Object()
        self.blst.h = 0.6   
        self.blst.rho = 19e3
        self.blst.bt = 2.4 
        self.blst.b = (self.bf+self.blst.bt)/2  
        self.blst.area = self.blst.b*self.blst.h 
        self.blst.wt = self.blst.area*self.blst.rho*g  
        
        
    def Conc(self,grade):
        '''the concrete properties according to the kind selected:
            grade: concrete grade, has to be one of 25,32,40,50,65,80,100'''
        self.conc=Object()
        self.conc.slab = Object()
        self.conc.v = 0.2 
        grade_table = [25,32,40,50,65,80,100]
        E_table = [24000,26700,30100,32800,34800,37400,39600,42200] #Modulus for standard grades
        if grade not in grade_table:
            raise ValueError("The grade has to be one of 25,32,40,50,65,80,100")    
        self.conc.fc=grade*1.0e6        
        self.conc.fctf=0.6*self.conc.fc**(1/2)*1.4 #1.4 is the factor to get the mean characterisitic value
        self.conc.fct=0.36*self.conc.fc**(1/2)*1.4       
        self.conc.rho = 25e2
        self.conc.E= [E_table[i] for i,j in enumerate(grade_table) if grade==j]
        self.conc.t = 28
        self.conc.slab.b = 2.4
        self.conc.slab.h = 0.3
        self.conc.slab.area = self.conc.slab.b*self.conc.slab.h
        self.conc.slab.wt= self.conc.slab.area*self.conc.rho*g
        

   

