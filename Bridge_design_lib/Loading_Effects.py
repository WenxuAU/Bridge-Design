# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:10:23 2023

@author: wenxuli
"""


'''Loading effects Calculation'''

#%% models to calculate loading effects, i.e. moments, stresses, strains and deflections
'''point load effect'''
class PointLoad:
    '''
    Point load
    x: location of the point load
    p: the magitude of the load, downwards direction
    l: the length of the beam (bridge)
    y: location where the effect is wanted
    z: the vertical location where the stress is calculated
    I: moment of area
    E: Young's modulus
    '''
    def __init__(self,x,p,l,y,z,I,E):
        self.x = x
        self.p = p
        self.l = l
        self.y = y
        self.z = z
        self.I = I 
        self.E = E
        if y<=x:  
            self.M = (1-x/l)*p*y #moment, Nm   
            self.V = (1-x/l)*p   #shear force, N                 
        else: 
            self.M= x*p*(1-y/l)
            self.V = -x/l*p   #shear force, N 
        self.Defl = self.M/E/I*(y**2-self.l)
        self.Sigma=self.M*z/I
        self.Strain = self.Sigma/E
#%% 

class UniformLoad:
    '''   
    uniformly distributed load across the whole beam
    p: the magitude of the load density per meter, downwards direction
    l: the length of the beam (bridge)
    y: longitudinal location where the effect is wanted
    z: the vertical location where the stress is calculated
    I: moment of area
    E: Young's modulus
    '''
    def __init__(self,q,l,y,**kwargs):
        self.q = q
        self.l = l
        self.y = y
        self.M = q/2*y*(l-y) #moment, Nm   
        self.V = q/2*(l-2*y)   #shear force, N   
        if len(kwargs):
           z = kwargs.get('z', -10)
           I = kwargs.get('I', -10)
           E = kwargs.get('E', -10)  
           if z!=-10 and I!=-10 and E!=-10:
               self.Defl = self.M/E/I*(y**2-self.l)
               self.Sigma=self.M*z/I
               self.Strain = self.Sigma/E
#%%
class UniformPartialSpanLoad:
    '''Distributed load of a finite length'''
  
    def __init__(self,x,d,q,l,y,z,I,E):
        '''   
        x: starting position of the uniform distributed load
        d: the span of the uniformly distribued load
        p: the magitude of the load density per meter, downwards direction
        l: the length of the beam (bridge)
        y: location where the effect is wanted
        z: the vertical location where the stress is calculated
        I: moment of area
        E: Young's modulus
        #outputs================
        M: moment
        ShearForce
        Sigma: stress
        strain
        '''
        self.x = x
        self.d = d
        self.q = q
        self.l = l
        self.y = y
        self.z = z
        self.I = I 
        self.E = E
        if y<=x: 
            self.M = q*d/l*(l-x-d/2)*y
            self.V = q*d/l*(l-x-d/2)   #shear force, N
        elif y>x and y<=x+d:
            self.M = q*y*d*(l-x-d/2)/l-q*(y-x)**2/2
            self.V = q*d/l*(l-x-d/2)-q*(y-x)
        else:
            self.M = q*d*(d/2+x)*(l-y)/l
            self.V = -q*d*(d/2+x)/l
        self.Defl = self.M/E/I*(y**2-self.l)
        self.Sigma=self.M*z/I
        self.Strain = self.Sigma/E
#%% 
'''Moment load, for traction and braking forces'''
class MomentLoad:
    '''Moment load'''
    def __init__(self,P,h,y,l,z,I,E):        
        '''h: the distance from the top surface of the bridge
        P: the force, traction or braking
        y: location where the effect is wanted
        z: the vertical location where the stress is calculated
        l: the length of the beam (bridge)
        I: moment of area
        E: Young's modulus'''
        self.P = P
        self.h = h
        self.z = z
        self.I = I 
        self.E = E
        M_tot = 0
        if type(P) is list:
            for i in P:
                M_tot = M_tot + i*h
        self.M = M_tot/l*y
        self.V = M_tot/l
        self.Sigma=self.M*z/I
        self.Strain = self.Sigma/E 
        self.Defl = self.M/E/I*(y**2-l)               
                
class TorsionLoad:
    '''torsion is applied to the surface of a bridge'''
    def __init__(self,P,e):
        '''P: the torsional force
        e: the eccentric distance from the centroid'''
        self.T = P*e
#%% test the algorithms
if __name__=='__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    N = 100  # number of positions to be looked at along the bridge
    Lv = 20 # brindge length
    # loading effects to be examined
    Mom = np.zeros(N)
    SF = np.zeros(N)
    sigma = np.zeros(N)
    epsilon = np.zeros(N)
    yp = np.linspace(0,Lv,N) #locations to calculate moments, stresses, strains and deflections
    
    Mom1 = np.zeros(N)
    SF1 = np.zeros(N)
    Mom2 = np.zeros(N)
    SF2 = np.zeros(N)
    for k,y in enumerate(yp):
        tmp = UniformLoad(10, 20, y, z=2, I=20, E=1e3)
        tmp1 = PointLoad(10, 100, 20, y, 2, 20, 1e3)
        tmp2 = UniformPartialSpanLoad(0, 10, 20, 20, y, 2, 20, 1e3)
        Mom[k] = tmp.M
        SF[k] = tmp.V
        Mom1[k] = tmp1.M
        SF1[k] = tmp1.V
        Mom2[k] = tmp2.M
        SF2[k] = tmp2.V
    plt.plot(yp,Mom,'k',yp,SF,'k--',yp,Mom1,'b',yp,SF1,'b--',yp,Mom2,'r',yp,SF2,'r--')
    plt.legend(['Uniformly distributed force-Moment','Uniformly distributed force-Shear Force',
               'Point load-Moment','Point load-Shear Force','Uniform distribution with a limited span-Moment',
               'Uniform distribution with a limited span-Shear Force'])
    plt.xlabel('Span of the beam')
    plt.ylabel('Magnitude')