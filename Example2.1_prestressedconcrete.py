# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:08:37 2023

@author: wenxuli
"""
from Bridge_design_lib import Serviceability
import numpy as np
sigmasus = 10
t = 400
h = 400
th = t*h/(t+h)
fc = 32
Ec=32e3
t = [14,180]
for ti in t[:1]:
    # shrinkage strain
    fc1 = np.exp(0.38*(1-(28/ti)**0.5))*35
    Ec1 = 2400**1.5*0.043*35**0.5
    epsiloncs = Serviceability.epsiloncs(fc, th,aggreg_type=0)
    # creep strain
    epsiloncc = Serviceability.epsiloncc(fc, th, sigmasus, Ec1,tau = ti)
    epsilonc = epsiloncc+epsiloncs
    print('The shrinkage strain, creep strain and the overall strains \
          are {:.4f}, {:.4f} and {:.4f}, respectively.'.format(epsiloncs,epsiloncc,epsilonc))

