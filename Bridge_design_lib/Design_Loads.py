# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 15:58:51 2023

@author: wenxuli
"""


''' rail traffic loads-vertical forces'''
# import os
# print(os.path.realpath(__file__))


#%% vertical rail traffic load: 300LA model
def M300LA(Lv,x_shift=0):
    '''
    Rail traffic load model: 300LA, Section 9.2 of AS5100.2
    Lv: the span betwen centres of axle groups,i.e. vehicle lengths, <=20m and >=12m
    Lv can be a vector, # of elements = nv; when there is one axle group on the bridge
    Lv=0
    x_shift: the shift of the first axle group starting point longitudinally along the bridge
    '''
    
    if type(Lv) is list:
        if Lv[0]>0 and len(Lv)>=1:
            Lv = [0]+[float(i) for i in Lv]
    elif Lv>0:
        Lv = [0,Lv]
        # print(Lv)
    else:
        Lv=[0]
    if len(Lv)>1:
        for i in Lv[1:]:        
            # print(i)
            if i >20 or i <12:
                raise ValueError("Error: each axle group distance has to be between 12 and 20m")
            
    pos = [0,1.7,1.1,1.7,2]
    pos = [sum(pos[:i+1]) for i in range(len(pos))]
    loads = 4*[300]+[360]   #in kN
    if len(Lv)>1:        
        pos1 = []
        for i in range(len(Lv)):
            pos1 = pos1+list(map(lambda x: x+sum(Lv[:i+1])+pos[-1]*i, pos))
        loads = loads*len(Lv) 
        pos=pos1      
    return {'pos':[k+x_shift for k in pos],'loads':loads}



#%% Horizontal Forces
'''the empirical models are used here'''
def CoexistFactor(n):
    '''
    n: number of rail vehicles
    
    '''
    if n == 1:
        CF = [1]
    elif n == 2:
        CF = [1,1]
    elif n == 3:
        CF = [1,1,0.5]
    else:
        CF = [1,1,0.5]+[0.25]*n
    return CF

class BrakeForce:
    def __init__(self,LLF,n,hBr):
        
        '''applied to the driving axles, in the longitudinal direction
        # LLF: total length of the bridge, in metres
        # BF: longitudinal braking force, in kN
        # hBr: the force lever arm, i.e. the height of the braking force from the neutral axis of the member.
        see Clause 9.7.2 of AS5100.2:2017, in meters
        '''
        self._LLF = LLF
        self._n = n
        self._h = hBr
    @property
    def Force(self):
        BF = 200+15*self._LLF
        CF = CoexistFactor(self._n)
        return [ BF*i for i in CF]
    @property
    def Moment(self):
        return [i*self._h for i in self.Force]

class TractionForce:
    def __init__(self,LLF,n,hTf):
        '''
        Parameters
        ----------
        LLF : TYPE
            total length of the bridge, in metres.
        n : TYPE
            DESCRIPTION.
        hTf : TYPE
            the force lever arm, i.e. the height of the traction force from the neutral axis of the member.
            see Clause 9.7.2 of AS5100.2:2017, in meters

        Returns
        -------
        None.

        '''
        self._LLF = LLF
        self._n = n
        self._h = hTf        
        
    @property
    def Force(self):
        ''' Section 9.7.2.2 Empirical model
        LLF: total length of the bridge, in metres
        n: the number of vehicles on the birdge at the same 
        applied to all axles uniformly, in the longitudinal direction'''
        # TF: longitudinal traction force, in kN
        if self._LLF>250:
            TF = 2700+5*(self._LLF-250)
        elif self._LLF<=250 and self._LLF>50:
            TF = 1200+7.5*(self._LLF-50)
        elif self._LLF<=25:
            TF = 200+25*self._LLF
        else:
            TF = 825+15*(self._LLF-25) 
            
        # print('trial')
        CF = CoexistFactor(self._n)
        return [TF*i for i in CF]   #change the unit to Newton from kN
    @property
    def Moment(self):
        '''calculate the traction force moment
        '''       
        return [i*self._h for i in self.Force]


def NosingLoad(x):
    ''' Section 9.7.3 of AS5100.2
    Nosing load is applied in the lateral direction at a single point at any location along the track
    x: the location of the load applied along the track
    1. In the case of lateral rail, rail_type=1, the load is 0.5 of the 300LA load
    2. in the case of 300LA load, 100kN is applied at any poistion on the rail laterally and at any location'''
    
    return {'pos':x,'load':100e3}

# %% dynamic load allowance
class DLA:
    def __init__(self,L):
        """dynamic load allowance, applies to both ULS and SLS, section 9.5.1 of AS5100.2
        L: characteristic length of a component in meters """
        self.L = L
        self.alpha_bending = self.DynBending()
        self.alpha_others = 0.67*self.alpha_bending #'''Dynamic load allowance 
        # for other load effects, Section 9.5.5 of AS5100.2
        # Dynamic load effct for torsion, shear and reactions'''
    def DynBending(self):
        '''Dynamic load allowance for bending effects, Section 9.5.3 of AS5100.2        
        alpha: the dynamic load factor. alpha*deadload=dynamic load'''
        alpha = 2.16/(self.L**0.5-0.2)-0.27
        if alpha>0.67:
            alpha = 0.67
        if alpha < 0.2:
            alpha = 0.2 
        return alpha
def DeflDL(Lv,L,x_shift=0):
    '''deflection design load, clause 9.10 of AS5100.2:2017'''
    traffic_loads = M300LA(Lv,x_shift)
    factor = 1.0+DLA(L).alpha_bending
    return {'pos':traffic_loads['pos'],'loads':[factor*i for i in traffic_loads['loads']]}
def FDL(Lv,L,x_shift=0):
    '''Clause 9.8.1 of AS5100.2:2017, faituge design traffic load
    Principle: traffic load+ 0.5* dynamic load allowance
    Lv: distance between axle group centers, i.e. the vehicle length, in metres
    L: characteristic length of a component
    x_shift: the shift of the first axle group starting point longitudinally along the bridge    
    '''
    traffic_loads = M300LA(Lv,x_shift=0)
    factor = 1.0+DLA(L).alpha_bending/2
    return {'pos':traffic_loads['pos'],'loads':[factor*i for i in traffic_loads['loads']]}

    
#%% load distribution on the surface of railway bridge deck
class Object:
    pass

class LoadDist:
    '''Section 9.6 of AS5100.2
    '''
    def __init__(self,L,trk_fm,trk_no,dpt_slab,dpt_blst,
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
        self.L = L        

    def _DistSize(self,axle_spacing):
        '''Section 9.6.4 of AS 5100.2
        axle_spacing: distance btween neighbouring axles
        '''
        if self.trk_fm==1:
            '''Section 9.6.4 of AS5100.2:ballasted track on concrete bridge '''
            self.w=self.l_slp + self.dpt_blst + 2*self.dpt_slab  # width of distribution
            self.l = 1.1+self.dpt_blst+2*self.dpt_slab   # length of load distribution
            if self.l>axle_spacing:
                self.l = axle_spacing                
            '''in the case of multiple tracks on the bridge'''
            if self.trk_no>1:
                if self.w>self.dis_trks:
                    self.w=self.dis_trks
        if self.trk_fm==2:
           '''direct fixation track: assume uniform distribution along the track'''
           pass       
        
          
    def M300LADist(self,traffic_loads):
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
        discount: to discount the effect of loading from dynamic load allowance
        ### applicable to M300LA type load, including the fatigue design load
        
        '''         
        axle_pos = traffic_loads['pos']
        axle_no = len(axle_pos)    
        axle_spacings1 = [axle_pos[0]]+ [axle_pos[i+1]-axle_pos[i] for i in range(axle_no-1)]  
        axle_spacings2 = [axle_pos[i+1]-axle_pos[i] for i in range(axle_no-1)] + [self.L - axle_pos[-1]]
        axle_spacings = [min([axle_spacings1[i],axle_spacings2[i]]) for i in range(axle_no)]
        # print(axle_spacings1,axle_spacings2,axle_spacings)
        if axle_spacings[0]<axle_spacings2[0]: axle_spacings[0] = axle_spacings2[0]
        if axle_spacings[-1]<axle_spacings1[-1]: axle_spacings[-1] = axle_spacings1[-1]
        # print(axle_spacings2,axle_spacings)
        tmp = []
        for i in range(axle_no): 
            self._DistSize(axle_spacings[i]) # generate l and w of the distributed loads
            start_pos = max([axle_pos[i]-self.l/2,0])
            # print(start_pos,self.l)
            magitude = traffic_loads['loads'][i]/self.l
            if start_pos < 0:
                start_pos = 0
            if start_pos > self.L:
                raise ValueError('The setting of 300LA model is not correct!')
            if self.l+start_pos >self.L:
                self.l = self.L-start_pos
            tmp=tmp+[(start_pos,self.l,magitude)]
        return tmp
#%% derailment load and the distribution        
class DerailLoad:
    def __init__(self):
        pass
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

      
    # def DerailmentLoadonBr(self,Lv,L,bf,gauge,x_shift,y_shift):
        
    #     '''Derailment load acting on the bridge surface, as opposed to that on the railway track.
    #     Case A: 2 situations: 1: 300LA with lateral shift; 2: a point load of 200kN;
    #     Case B: a distributed load of 100kN of 20 m long;
    #     option: 1: Case A sitaution 1; 2, CaseA situation 2; 3, CaseB'''
    #     self.DerailmentLoads = Object()
    #     self.DerailmentLoads.blst = Object()
    #     self.DerailmentLoads.slab = Object()
    #     loadCaseA = CaseA(Lv,gauge,x_shift,y_shift)  
    #     self.DerailmentLoads.blst.CaseA2 = loadCaseA[1]                                     
    #     self.DerailmentLoads.blst.CaseA1 = self.M300LAOnBr(Lv,L,0,x_shift)#No DLA considered
    #     self.DerailmentLoads.blst.CaseB = CaseB(bf,L,gauge,y_shift)
        
    #     #-------------------load distribution-----------------------------
    #     #-----------------------not finished for slab track---------------
    #     self.DerailmentLoads.slab.CaseA1 = sum(
    #         [j[1]*j[2] for j in self.M300LAOnBr(Lv,L,0,x_shift)])/L
    #     self.DerailmentLoads.slab.CaseA2 =  loadCaseA[1]
    #     self.DerailmentLoads.slab.CaseB =  CaseB(bf,L,gauge,y_shift)
        
#%% test code 
def pltAxles(traffic_loads,**kwargs):
    from matplotlib import pyplot as plt
    from matplotlib import patches as pts
    import numpy as np
    if len(kwargs)==0:
        theta = np.linspace(0,2*np.pi,20)
        for i in range(len(traffic_loads['pos'])):
            x = traffic_loads['pos'][i]+0.45*np.cos(theta)
            y = 0.45+0.45*np.sin(theta)    
            plt.arrow(traffic_loads['pos'][i],3,0,-1.5,width=0.05,head_width=0.2,color='r')
            plt.plot(x,y,'k')
        plt.ylim([0,8])
        plt.plot(traffic_loads['pos'],traffic_loads['loads'],'ko')
        plt.xlabel('x,m')
        # ax = plt.gca()
        # ax.set_aspect('equal', adjustable='box')
    if len(kwargs)>0:
        '''plot load distributions'''
        plt.gca().add_patch(pts.Rectangle((0,0),l, 0.5,color='grey'))   
        theta = np.linspace(0,2*np.pi,20)
        LDist = kwargs.get('LoadDist')
        for i in range(len(traffic_loads['pos'])):
            xx = traffic_loads['pos'][i]+0.45*np.cos(theta)
            start_pos = LDist[i][0]
            wdt = LDist[i][1]
            yy = 1+0.5*np.sin(theta)    
            plt.arrow(traffic_loads['pos'][i],3,0,-1,width=0.05,head_width=0.2,color='r')
            plt.plot(xx,yy,'k')
            plt.gca().add_patch(pts.Rectangle((start_pos,0),wdt, 1))
        plt.ylim([0,5])
        plt.xlim([0,l])
        plt.xlabel('Longitudinal Distance, m')
        plt.yticks([])
        plt.plot(DLd['pos'],DLd['loads'],'ko')
        plt.gca().set_aspect('equal', adjustable='box')    
        plt.draw()
    
if __name__=='__main__':
    from matplotlib import pyplot as plt
    from matplotlib import patches as pts
    import numpy as np
    Lv = [12,12]
    x_shift = 20
    traffic_loads = M300LA(Lv,x_shift)
    fig = plt.figure(1)
    plt.subplot(211)
    pltAxles(traffic_loads) #plot axle load locations  
    
    plt.subplot(212)
    l = 20
    x_shift = 5
    DLd = DeflDL(0, l,x_shift= 5)    
    ldobj = LoadDist(l, 1, 1, 0.2, dpt_blst=0.6, l_slp=2)
    LDist = ldobj.M300LADist(DLd)              
    #plot load distributions
    pltAxles(DLd,LoadDist=LDist) 
 




