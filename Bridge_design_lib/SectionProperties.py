# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:40:43 2023

@author: wenxuli
"""

import sys
import numpy as np
class RectBeam:
    '''Rectangular shaped beam (solid section), x: width, y: depth
    '''
    def __init__(self,x,y,**kwargs):
        self.x = x
        self.y = y
        self.Ag = x*y
        self.uc = 2*(x+y)
        self.Ig = x*y**3/12
        self.tw = 0.75*self.Ag/self.uc # effective wall thickness
        self.Ast = 0 
        self.dst = 0 
        self.Asc = 0 
        self.dsc = 0
        self.n = 0
        self.ue = self.uc
        self.th = self.Ag/self.ue
        if len(kwargs)>1:
            self.n = kwargs.get('Es')/kwargs.get('Ec')
            self.Ast = kwargs.get('Ast')
            self.dst = kwargs.get('dst')      
            if 'Asc' in kwargs:
                self.Asc = kwargs.get('Asc')
                self.dsc = kwargs.get('dsc')  
     
            self.kud = self.kud()
            self.Icr = self.Icr()
    def kud(self):
        p =[self.x/2,self.n*self.Ast+(self.n-1)*self.Asc,\
            -self.n*self.Ast*self.dst-(self.n-1)*self.Asc*self.dsc]
        r = np.roots(p)
        return [i for i in r if i > 0][0]
    def Icr(self):
        dn = self.kud
        Icr = (self.n-1)*self.Asc*(dn-self.dsc)**2+self.x*dn**3/3+\
           self.n*self.Ast*(self.dst-dn)**2
        return {'dn':self.kud,'Icr':Icr}
class TBeamParam1:
    '''calculate the geometric properties associated with the T-beam section
    
                       /_____________tf________________/
                    /    
                 /  |   |------------------------------|    /    /
                 |  hf1 |                              |    \    |
                 |  |---|                             -     hf2  |
                 |  /     -                         -       |    |
                 |           -                   -          |    |
                 |              -            -------------- /    |
                 |                 |        |                    |
                 h                 |        |                    d
                 |                 |        |                    |
                 |                 |        |                    |
                 |                 | o o o--\---------------     /
                 |                 |________|
                 /                 /---tw--/
    '''
    def __init__(self,tf,tw,hf1,hf2,h,d,**kwargs):
        self.tf = tf
        self.tw = tw
        self.hf1 = hf1
        self.hf2 = hf2
        self.h = h
        self.Ast = 0
        self.d = 0
        self.Asc = 0
        self.dsc = 0
        self.n = 0
        if len(kwargs)>1:
            self.n = kwargs.get('Es')/kwargs.get('Ec')
            self.Ast = kwargs.get('Ast')
            self.dst = kwargs.get('dst')
            self.fc = kwargs.get('fc')
            if 'Asc' in kwargs:
                self.Asc = kwargs.get('Asc')
                self.dsc = kwargs.get('dsc')           
            self.dnIcr = self.dnIcr()
        self.gamma = self.gamma()
        self.dnIg = self.dnIg()
        self.Ag = self.Ag()
        self.uc = self.uc()
        self.ue = self.ue()
        self.th = 2*self.Ag/self.ue
    def gamma(self):
        '''Section 8.1.3 of As5100.5
        fc: characteristic concrete compressive strength,MPa
        b: the width of the cross -section of the stress block
        d: the depth of the refinforcement steel from the extreme compressive concrete fibre, mm
        ku: dn/d'''    
        gamma = 1.05 - 0.007*self.fc    
        if gamma>0.85: gamma = 0.85
        if gamma<0.67: gamma = 0.67
        return gamma
    
    def Ag(self):
        return self.tf*self.hf1+(self.d-self.hf2)*self.tw+(self.hf2-self.hf1)*(self.tf-self.tw)
    def uc(self):
        return 2*self.d-2*(self.hf2-self.hf1)+ self.tf+self.tw+\
            2*(((self.tf-self.tw)/2)**2+(self.hf2-self.hf1)**2)**0.5
    def ue(self):
        # the perimeter of a member plus half the perimeter of any internal voids,
        # exposed to a drying environment
        return self.uc
    def dnIg(self,Ast,Asc=0):
        '''Ig of an uncracked section, the steel is ignored'''
        dn =(self.tf*self.h1**2/2+(self.tf-self.tw)*(self.h2-self.h1)*(self.h2+2*self.h1)/3+\
            self.tw*(self.d-self.h1)*(self.d+self.h1)/2)/self.Ag
        
        Ig = self.tf*self.hf**3/12+self.tf*self.hf*(dn-self.hf/2)**2+ \
            self.tw*(self.h-self.hf)**3/12+self.tw*(self.h-self.hf)*((self.hf+self.h)/2-dn)**2
        return {'dn':dn,'Ig':Ig}
    def dnIcr(self,Ast,Asc=0):
        '''2nd moment of area of a fully cracked section'''
        p = [self.tw/2,(self.tf-self.tw)*self.hf+self.n*self.As,
             -(self.tf-self.tw)*self.hf**2/2-self.n*self.As*self.d]
        
        r = np.roots(p)
        a = [i for i in r if i > 0][0]
        Icr = (self.h-self.tw)*self.hf**3/12+(self.tf-self.tw)*self.hf*(a-self.hf/2)**2+\
            self.tw*a**3/3+self.n*self.As*(self.d-a)**2
        return {'dn':a/self.gamma,'Icr':Icr}
    
class TBeamParam:
    '''calculate the geometric properties associated with the T-beam section
    
                       /_____________tf________________/
                    /    
                 /  |   |------------------------------| |  /
                 \  hf  |o o o o o o o o o o o o o o o |dsc \
                 \  |   |------------------------------|    \
                 \  /              |        |               \
                 h                 |        |               dst
                 \                 |        |               \
                 \                 |        |               \
                 \                 | o o o--\---------------/
                 \                 |________|
                 /                 /---tw--/
    '''
    def __init__(self,tf,tw,hf,h,**kwargs):
        self.tf = tf
        self.tw = tw
        self.hf = hf
        self.h = h
        self.Ast = 0
        self.dst = 0
        self.Asc = 0
        self.dsc = 0
        self.n = 0
        
        self.Ag = self.Ag()
        # self.uc = self.uc()
        # self.ue = self.ue()
        # self.th = 2*self.Ag/self.ue
        self.dnIg = self.dnIg()
        
        if len(kwargs)>1:
            self.n = kwargs.get('Es')/kwargs.get('Ec')
            self.Ast = kwargs.get('Ast')
            self.dst = kwargs.get('dst')
      
            if 'Asc' in kwargs:
                self.Asc = kwargs.get('Asc')
                self.dsc = kwargs.get('dsc')  
     
            self.kud = self.kud()
            self.Icr = self.Icr()        

    def Ag(self):
        return self.tf*self.hf+ (self.h-self.hf)*self.tw
    def uc(self):
        return 2*self.dst+2*self.tf
    def dnIg(self):
        dn = (self.tf*self.hf**2/2+self.tw*(self.h-self.hf)*(self.h+self.hf)/2)/self.Ag
 
        Ig = self.tf*self.hf**3/12+self.tf*self.hf*(dn-self.hf/2)**2+\
            self.tw*(self.h-self.hf)**3/12+self.tw*(self.h-self.hf)*((self.hf+self.h)/2-dn)**2
        return {'dn':dn,'Ig':Ig}
    def kud(self):    
        p = [self.tw/2,(self.tf-self.tw)*self.hf+self.n*self.Ast+(self.n-1)*self.Asc,
             -(self.tf-self.tw)*self.hf**2/2-self.n*self.Ast*self.dst-(self.n-1)*self.Asc*self.dsc]        
        r = np.roots(p)
        return [i for i in r if i > 0][0]
    def Icr(self):        
        Icr = (self.tf-self.tw)*self.hf**3/12+(self.tf-self.tw)*self.hf*\
            (self.kud-self.hf/2)**2+\
            self.tw*self.kud**3/3+self.n*self.Ast*(self.dst-self.kud)**2
        return {'dn':self.kud,'Icr':Icr}

class IBeamParam:
    '''calculate the geometric properties associated with the I-beam section
                       /_____________tf________________/
                    /    
                    |   |------------------------------|
                    h1  |                              |
                    /    -                            -
                    \     -                          -
                    h2     -                        -
                    \       -                      -
                    /         ------        -------
                    \              |        |
                    \              |        |
                    \              |        |
                    h              |        |
                    \              |        |
                    \              |___tw___|
                    \              \        \
                    \              \        \
                    /         ------        -------
                             -                      -
                            -                        -
                           -                          -
                          -                            -
                         |                              |
                         |------------------------------|
    
    '''
    
    def __init__(self,tf,tw,h1,h2,h):
        self.tf = tf
        self.tw = tw
        self.h1 = h1
        self.h2 = h2
        self.h = h
        self.Ag = 2*(tf*h1+(tf-tw)/2*h2+tw*(h2+h/2))
        self.dnIg()
    def dnIg(self):
        dn = self.h1+self.h2+self.h/2
        Ig = self.tf*self.h1**3/12+self.tf*self.h1*(dn-self.h1/2)**2+\
            (self.tf-self.tw)/2*self.h2**3/36+(self.tf-self.tw)/2*self.h2*(dn-self.h1-self.h2/3)**2+\
                self.tw*(self.h2+self.h/2)**3/3
        self.dnIg = {'dn':dn,'Ig':Ig*2}
        
    def dnIcr(self):
        pass

#%% verfications using examples in Concrete strcutures by RF Warner       

if __name__=='__main__':
    #example 5.6
    ex1 = TBeamParam(1000,275,100,760,650,4800,2e5,27700,1)
    ex1.dnIg()
    ex1.dnIcr()
    print('Example 5.6 T beam has \n',ex1.dnIg, ex1.dnIcr,'\n----------------')
    #example  15.1
    ex2 = TBeamParam(6000,350,180,650,590,3200,2e5,28500,0.822)
    ex2.dnIg()
    ex2.dnIcr()
    print('Example 15.1 T beam has \n',ex2.dnIg, ex2.dnIcr,'\n----------------')
    # example 7.17 in the book
    ex3 = IBeamParam(800,150,100,100,800)
    ex3.dnIg()
    print('Example 7.17 I beam section has\n ',ex3.dnIg)
    
    n = 2e5/285e2 
    As = 3200
    d = 590
    p = [350/2*0.822**2, 5650*180+n*As,-(5650*180*90+n*As*590)]
    r = np.roots(p)
    dn = [i for i in r if i>0][0]
    print(dn)
    Icr = 350/3*(0.822*dn)**3 + n*3200*(590-dn)**2+(6000-350)*180*(dn-90)**2
    print(Icr)
    
    dn0 = (6000*180*90+470*350*415)/(6000*180+470*350)
    Ig = 6000*180**3/12+6000*180*(dn0-90)**2+350*470**3/12+470*350*((180+470/2)-dn0)**2
    print(Ig/1e9)
    p = [275/2,7.22*4800+72500,-72500*50-7.22*650*4800]
    r = np.roots(p)
    dn =[i for i in r if i >0][0]
    print('--------------------')
    print(r)
    Icr = 725*1e6/12+72500*(dn-50)**2+275*dn**3/3+7.22*4800*(650-dn)**2
    print(Icr)
    
    # dn0 = (50e5+660*275*430)/(1e5+660*275)
    
    # Ig = 1000*100**3/12+1e5*(dn0-50)**2+275*660**3/12+660*275*(430-dn0)**2
    # print(dn0,Ig/1e9)