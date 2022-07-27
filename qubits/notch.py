# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:53:20 2022

@author: Theo Gifford
"""

import numpy as np
from component import Component
import sdxf
from pt_operations import rotate_pt, rotate_pts, translate_pts, orient_pts, mirror_pts
from junction import junction
from component import Component

class QubitNotchFromJunc(Component):
    """
    Draws a qubit notch based on a cxn junction
    
    you pass it a 'in' or 'out' junction of a straight and it draws
    the notch on that straight
    
    thinking:
        - should it take a startjunc or a CPWStraight as an argument
        - should startjunc be moved to settings for all Components, along with
          cxns_names_defaults? idk it just seems wrong suddenly
        - 
    
    """
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['height'] = 100
    _defaults['taper_angle'] = 60 # (0-90]
    _defaults['notch_type'] = 'trapezoid' # / bevel / etc idk
    _defaults['length'] = 500
    _defaults['leftright'] = 'right'
    _defaults['refjunc'] = None
    _defaults['offset'] = 0
    
    def __init__(self, structure, settings = {}):
        
        s = structure
        
        comp_key = 'QubitNotchFromJunc'
        global_keys = ['pinw','gapw']
        object_keys = ['pinw','gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)        
        
        if self.refjunc is None:
            print("please provide junction for notch")
            return
        
        coords = self.refjunc.coords
        direction = self.refjunc.direction + 180
        d_to_gnd = self.gapw + 0.5*self.pinw
        
        if self.notch_type == 'trapezoid':
            tf = np.tan(np.pi*self.taper_angle/180)
            pts = [(self.offset+0,d_to_gnd),
                   (self.offset+self.height/tf,d_to_gnd+self.height),
                   (self.offset+self.length - self.height/tf,d_to_gnd+self.height),
                   (self.offset+self.length,d_to_gnd),
                   (0,d_to_gnd)]
            
            pts = orient_pts(pts,direction,coords)
            
            if self.leftright == 'left':
                pts = mirror_pts(pts,direction,coords)
            
            s.drawing.append(sdxf.PolyLine(pts))

        
        