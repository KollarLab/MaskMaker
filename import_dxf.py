# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:18:15 2022

@author: Theo
"""

import numpy as np
from component import Component
from pt_operations import rotate_pt, rotate_pts, translate_pts, arc_pts, orient_pts, mirror_pts, translate_pt, orient_pt
from junction import junction
import ezdxf

class ImportedDXF(Component):
    """
    
    Import any dxf, and translate, rotate, and scale.
    
    Requirements for imported file:
        -- must be dxf
        -- I think block.explode() breaks for more complicated dxf objects, but
           it should be fine for most of our stuff
    
    settings:
        xscale, yscale: Scales all x coordinates and y coordinates in the
            drawing. Negative values result in reflections
        offset: tuple coordinates where the imported DXF's origin is drawn on
            the chip
        rotation: simply rotates the DXF about the origin
        dxf_path: filepath for DXF to import
        
    """
    _defaults = {}
    _defaults['xscale'] = 1
    _defaults['yscale'] = 1
    _defaults['offset'] = (0,0)
    _defaults['rotation'] = 0
    _defaults['dxf_path'] = None
    
    def __init__(self,structure,settings):
        
        s = structure
        
        comp_key = 'CustomQubit'
        global_keys = []
        object_keys = [], # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        if self.dxf_path is None:
            print("please provide filepath for dxf")
            return
        
        doc = ezdxf.readfile(self.dxf_path)
        msp = doc.modelspace()  # contains all drawing entities
        
        block_name = str(s.block_i)
        new_block = s.doc.blocks.new(name=block_name)
        s.block_i = s.block_i + 1
        
        for e in msp:
            new_block.add_foreign_entity(e)
            
        s.drawing.add_blockref(block_name,self.offset,dxfattribs={
            'xscale': self.xscale,
            'yscale': self.yscale,
            'rotation': self.rotation
            })
        
        for ref in s.drawing.query(f'INSERT[name=="{block_name}"]'):
            ref.explode()