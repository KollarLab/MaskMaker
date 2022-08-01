 # -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:09:29 2022

@author: Kollarlab

"""
from component import Component
from cpw.CPWStraight import CPWStraight
from cpw.CPWBend import CPWBend

import numpy as np
# from pt_operations import rotate_pt

class LobedRing(Component):
    """
    parameters:
        
        N: number of arms
        R: distance from center of lobed ring to edge (centerpin of bend)
        r1: radius of inner bends
        r2: radius of outer bends

    """
    
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['inner_bend_radius'] = 100
    _defaults['outer_bend_radius'] = 100
    _defaults['resonator_radius'] = 1700
    _defaults['num_arms'] = 6
    
    def __init__(self,structure, settings = {}, startjunc = None, cxns_names = ['couple']):
        
        s = structure
        
        comp_key = 'LobedRing'
        global_keys = ['pinw','gapw','radius','radius']
        object_keys = ['pinw','gapw','inner_bend_radius','outer_bend_radius'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        if startjunc is None:
            startjunc = s.last.copyjunc()
        else:
            s.last = startjunc.copyjunc()
        
        self.cxns = {cxns_names[0]:startjunc.copyjunc()}
        
        theta = 2*np.pi/self.num_arms
        theta_d = 360/self.num_arms
        R2 = self.resonator_radius - self.outer_bend_radius
        R1 = (self.outer_bend_radius+self.inner_bend_radius)/np.sin(theta/2)
        length_straights = R2 - R1*np.cos(theta/2)
        
        error_condition = self.outer_bend_radius > 0 and self.inner_bend_radius > 0 and self.resonator_radius > 0 and self.num_arms > 1 and self.resonator_radius > self.outer_bend_radius and self.inner_bend_radius + self.outer_bend_radius < R2*np.sin(theta/2)
        
        if error_condition == False:
            print("impossible geometry!")
            return
        
        self.qubit_cxns = []
        for arm_index in range(self.num_arms):
            CPWBend(s, settings = {'turn_angle':-90,
                                   'radius':self.outer_bend_radius
                                   })
            CPWStraight(s, settings = {'length':length_straights})
            CPWBend(s, settings = {'turn_angle':180-theta_d,
                                   'radius':self.inner_bend_radius
                                   })
            CPWStraight(s, settings = {'length':length_straights})
            
            self.qubit_cxns.append(s.last)
            
            CPWBend(s, settings = {'turn_angle':-90, 
                                   'radius':self.outer_bend_radius
                                   })
