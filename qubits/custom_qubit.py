# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:18:15 2022

@author: Theo
"""

import numpy as np
from component import Component
from pt_operations import rotate_pt, rotate_pts, translate_pts, arc_pts, orient_pts, mirror_pts, translate_pt, orient_pt
from junction import junction
from component import Component
import ezdxf

from qubits.notch import QubitNotchFromJunc

class CustomQubit(Component):
    """
    
    Import custom qubit and create pocket around it.
    
    Requirements for qubit file:
        -- must be dxf AND MADE OF LWPOLYLINES (no arcs, only straight lines)
        -- must have bottom left corner at (0,0)
        -- must be oriented horizontally
    
    settings:
        pinw: pinw of CPW the notch attaches to
        gapw: gapw of CPW the notch attaches to
        height: height of notch from base to base
        taper_angle: inner angle of tapers on both sides of the notch
        notch_type: currently only takes 'trapezoid'
        leftright: if refjunc.direction is up, draws the notch on the 'left' or
            'right' side of the CPW
        notch_offset: if refjunc.direction is up, positive offset shifts the notch 
            down along the CPW
        refjunc: endpoint of CPW the notch attaches to
        
        qubit_path: path of dxf file to import
        pin_gap: distance from pin to qubit
        import_offset: distance from corner of notch to (0,0) of imported qubit
        
    """
    _defaults = {}  
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['height'] = 100
    _defaults['taper_angle'] = 60 # (0-90]
    _defaults['length'] = 500
    _defaults['leftright'] = 'right'
    _defaults['refjunc'] = None
    _defaults['notch_offset'] = 0
    _defaults['notch_type'] = 'trapezoid'
    
    _defaults['qubit_path'] = None
    _defaults['pin_gap'] = 8.372
    _defaults['import_offset'] = 0
    
    def __init__(self,structure,settings):
        
        s = structure
        
        comp_key = 'CustomQubit'
        global_keys = ['pinw','gapw','pin_gap']
        object_keys = ['pinw','gapw','gapw'], # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        if self.refjunc is None:
            print("please provide refjunc for qubit")
            return
        
        if self.qubit_path is None:
            print("please provide filepath for qubit")
            return
        
        coords = self.refjunc.coords
        direction = self.refjunc.direction + 180
        
        doc = ezdxf.readfile(self.qubit_path)
        msp = doc.modelspace()  # contains all drawing entities
        
        all_pts = []
        polylines = msp.query("LWPOLYLINE")  # get all polylines in modelspace
        for polyline in polylines:
            pts = polyline.vertices()
            pts = list(pts)
            pts.append(pts[0])
            pts = translate_pts(pts,(self.import_offset+self.notch_offset,self.pin_gap+self.pinw/2))
            pts = orient_pts(pts,direction,coords)
            all_pts.append(pts)
            
        if self.leftright == 'left':
            for pts in all_pts:
                pts = mirror_pts(pts,direction,coords)
        elif self.leftright != 'right':
            print('invalid option passed for leftright, default value \'right\' used')
        
        for pts in all_pts:
            s.drawing.add_lwpolyline(pts)
        
        QubitNotchFromJunc(s,settings = {'pinw': self.pinw,
                                         'gapw': self.gapw,
                                         'height': self.height,
                                         'length': self.length,
                                         'taper_angle': self.taper_angle,
                                         'leftright': self.leftright,
                                         'refjunc': self.refjunc,
                                         'offset': self.notch_offset,
                                         'notch_type': self.notch_type})
