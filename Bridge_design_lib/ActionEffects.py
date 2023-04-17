# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 14:10:23 2023

@author: wenxuli
"""


'''Loading effects Calculation'''
import numpy as np

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
#%% UDL

class UniformLoad:
    '''   
    uniformly distributed load across the whole beam
    p: the magitude of the load density per meter, downwards direction, in N/m
    l: the length of the beam (bridge), in m
    y: longitudinal location where the effect is wanted, in m
    z: the vertical location where the stress is calculated
    I: moment of area
    E: Young's modulus
    
    '''
    def __init__(self,q,l,y,**kwargs):
        self.q = q
        self.l = l
        try:
            y = np.asarray(list(y)) 
        except TypeError:
            y = np.asarray([y])         
        self.M = q/2*y*(l-y)   #moment, kNm   
        self.V = q/2*(l-2*y)   #shear force, kN   
        if len(kwargs):
           z = kwargs.get('z', -10)
           I = kwargs.get('I', -10)
           E = kwargs.get('E', -10)  
           if z!=-10 and I!=-10 and E!=-10:
               self.Defl = self.M/E/I*(y**2-self.l)
               self.Sigma=self.M*z/I
               self.Strain = self.Sigma/E
#%% partial UDL
class UniformPartialSpanLoad:
    '''Distributed load of a finite length'''
  
    def __init__(self,x,d,q,l,y,**kwargs):  
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
        try:
            y = np.asarray(list(y)) 
        except TypeError:
            y = np.asarray([y]) 
        ix = np.arange(0,len(y))
        ind1 = ix[y<=x]
        ind3 = ix[y>x+d]
        ind2 = ix[(y<=x+d) & (y>x)]
  
        self.M = np.zeros(len(y))
        self.V = np.zeros(len(y))
        self.M[ind1] = q*d/l*(l-x-d/2)*y[ind1]
        self.M[ind2] = q*y[ind2]*d*(l-x-d/2)/l-q*(y[ind2]-x)**2/2
        self.M[ind3] = q*d*(d/2+x)*(l-y[ind3])/l
        self.V[ind1] = q*d/l*(l-x-d/2)   #shear force, N
        self.V[ind2] = q*d/l*(l-x-d/2)-q*(y[ind2]-x)
        self.V[ind3] = -q*d*(d/2+x)/l

        if len(kwargs)>1:
            z = kwargs.get('z')
            I = kwargs.get('I')
            E = kwargs.get('E')
            self.Defl = self.M/E/I*(y**2-self.l)
            self.Sigma=self.M*z/I
            self.Strain = self.Sigma/E

    
#%% 
'''Moment load, for traction and braking forces'''
class MomentLoad:
    '''Moment load'''
    def __init__(self,M,yM,l,y,**kwargs):      
        '''h: the distance from the top surface of the bridge
        M: the moment, e.g. traction or braking
        yM: the locations where Ms are applied
        y: location where the effect is wanted
        z: the vertical location where the stress is calculated
        l: the length of the beam (bridge)
        I: moment of area
        E: Young's modulus'''
        
        try:
            y = np.asarray(list(y)) 
        except TypeError:
            y = np.asarray([y]) 

          
        
        if type(M) is list:   
            M_tot = sum(M) 
            V = M_tot/l
            # sort the Ps according to the application locations
            tmp = [(i,j) for i,j in sorted(zip(M,yM), key=lambda tuples: tuples[1])] 
            M = [i for i, j in tmp]
            yM = [j for i,j in tmp]
            # find the indices where the Ps are applied
            ind = np.zeros(len(yM))
            if yM[-1]>l:
                raise ValueError('The moment applied must be within the span of the beam')

            ix = np.arange(0,len(y))
            for i in range(len(yM)):
                ind[i] = ix[y<=yM[i]][-1]
                    
            self.M = V*y 
            
            ind = ind.astype(int)
            for i in range(len(ind)):      
                ir = np.arange(0,len(y))[ind[i]:]
                self.M[ir] = self.M[ir]-M[i]
                # print(ir) #test point
            self.V = V*np.ones(len(y))
        else:
           V = M/l
           self.M = V*y       
           n = len(y)
           ind = np.arange(0,n)[y>=yM]
           self.M[ind] = self.M[ind]-M
           self.V = V*np.ones(n)               
           
        if len(kwargs)>1:
            self._z = kwargs.get('z')
            self._I = kwargs.get('I')
            self._E = kwargs.get('E')
            self.Sigma=self.M*self._z/self._I
            self.Strain = self.Sigma/self._E 
            self.Defl = self.M/self._E/self._I*(y**2-l)               
                
class TorsionLoad:
    '''torsion is applied to the surface of a bridge'''
    def __init__(self,P,e):
        '''P: the torsional force
        e: the eccentric distance from the centroid'''
        self.T = P*e
#%% test the algorithms
if __name__=='__main__':
    from matplotlib import pyplot as plt
    from matplotlib import patches as pts
    N = 100  # number of positions to be looked at along the beam
    # loading effects to be examined
    Mom = np.zeros(N)
    SF = np.zeros(N)
    sigma = np.zeros(N)
    epsilon = np.zeros(N)    
    
    Mom1 = np.zeros(N)
    SF1 = np.zeros(N)
    Mom2 = np.zeros(N)
    SF2 = np.zeros(N)
    Mom3 = np.zeros(N)
    SF3 = np.zeros(N)
    
    l = 20  # beam length
    yp = np.linspace(0,l,N) #locations to calculate moments, stresses, strains and deflections
    fig1 = plt.figure(1)
    for k,y in enumerate(yp):
        tmp = UniformLoad(10, l, y, z=2, I=20, E=1e3)
        tmp1 = PointLoad(10, 100, l, y, 2, 20, 1e3)
        tmp2 = UniformPartialSpanLoad(5, 10, l, 20, y)
        tmp3 = MomentLoad(10, 5, l, y)
        Mom[k] = tmp.M
        SF[k] = tmp.V
        Mom1[k] = tmp1.M
        SF1[k] = tmp1.V
        Mom2[k] = tmp2.M
        SF2[k] = tmp2.V
        Mom3[k] = tmp3.M 
        SF3[k] = tmp3.V
    plt.plot(yp,Mom/max(abs(Mom)),'k',yp,SF/max(abs(SF))-3,'k',yp,Mom1/max(abs(Mom1)),\
              'b--',yp,SF1/max(abs(SF1))-3,'b--',yp,Mom2/max(abs(Mom2)),'r-.',yp,SF2/max(abs(SF2))-3,'r-.',\
                  yp,Mom3/max(abs(Mom3)),'g:',yp,SF3/max(abs(SF3))-3,'g:')
    plt.gca().add_patch(pts.Rectangle((0,0),l,0.1,color='grey'))
    plt.ylim([-5,7])
    plt.yticks(np.arange(-6,7,3),['','Shear\nforce','Moment','',''],rotation=90)
    plt.legend(['Uniformly distributed force-Moment','Uniformly distributed force-Shear Force',
                'Point load-Moment','Point load-Shear Force','Uniform distribution with a limited span-Moment',
                'Uniform distribution with a limited span-Shear Force',\
                    'Moment load-Moment','Moment load-Shear force'])
    plt.xlabel('Span of the beam')
    # check the momentload algorithm
    figure2 = plt.figure(2)
    tmp3 = MomentLoad([1,-1,1], [0.1,0.5,0.2], 1, np.linspace(0, 1,100))
    plt.plot(yp,-tmp3.M,yp,tmp3.V)
    plt.legend(['Moment load-Moment','Moment load-Shear force'])
    plt.xlabel('Span of the beam')
    