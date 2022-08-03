# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:38:45 2022

@author: Kollarlab
"""

import numpy as np
from component import Component
import sdxf
from pt_operations import rotate_pt, rotate_pts, translate_pts, arc_pts, orient_pts, mirror_pts, translate_pt, orient_pt
from junction import junction
from component import Component

from qubits.notch import QubitNotchFromJunc

class SawtoothQubit(Component):
    """
    draws qubit paddles with pocket + teeth
    
    settings:
        pinw: pinw of CPW the notch attaches to
        gapw: gapw of CPW the notch attaches to
        taper_angle: inner angle of tapers on both sides of the notch
        notch_type: currently only takes 'trapezoid'
        leftright: if refjunc.direction is up, draws the notch on the 'left' or
            'right' side of the CPW
        refjunc: endpoint of CPW the notch attaches to
        offset: if refjunc.direction is up, positive offset shifts the notch 
            down along the CPW
            
        h_padding: distance between notch taper and paddle
        v_padding: distance between notch wall and paddle
        updown: "points" the paddles either in refjunc.direction ('up') or the 
            reverse ('down')
        tooth_height: height of a tooth
        tooth_spacing: distance between consecutive teeth on opposite paddles.
            (for example teeth on the same paddle are separated by
             2*tooth_spacing+tooth_width)
        tooth_width: width of a tooth
        
        paddle_length: length of entire paddle (including pocket)
        paddle_width: width of paddle NOT INCLUDING tooth_height
        buffer: length of paddle where there will be no teeth (and a pocket)
        
        pocket_offset: distance from edge of pocket to end of paddle
        pocket_depth: depth of pocket
        pocket_length: full length of pocket (not just the length of the
            deepest part of the pocket)
        pocket_wall_angle: angle the wall makes with the side of the paddle
            that is "cut out"
    
    it is somewhat hard to describe these things, there are pictures in docs
    """
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['refjunc'] = None
    _defaults['offset'] = 0
    _defaults['pin_gap'] = 8.372
    _defaults['leftright'] = 'right'
    _defaults['taper_angle'] = 60
    
    _defaults['h_padding'] = 10
    _defaults['v_padding'] = 20
    _defaults['updown'] = 'up'
    
    _defaults['tooth_height'] = 16
    _defaults['tooth_spacing'] = 8
    _defaults['tooth_width'] = 8
    _defaults['paddle_length'] = 600
    _defaults['paddle_width'] = 16
    _defaults['paddle_gap'] = 24
    
    _defaults['buffer'] = 24
    _defaults['pocket_offset'] = 8
    _defaults['pocket_depth'] = 8
    _defaults['pocket_length'] = 16
    _defaults['pocket_wall_angle'] = 60
    
    def __init__(self,structure,settings):
        
        s = structure
        
        comp_key = 'ExampleQubit'
        global_keys = ['pinw','gapw','pin_gap']
        object_keys = ['pinw','gapw','gapw'], # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        coords = self.refjunc.coords
        direction = self.refjunc.direction + 180
        
        if self.paddle_gap - self.tooth_height < 6:
            print('paddle_gap-tooth_height < 6um may cause fab  issues @ {}'.format(coords))
        if self.tooth_height < 6:
            print("tooth_height < 6um may cause fab issues @ {}".format(coords))
        if self.tooth_spacing < 6:
            print("tooth-spacing < 6um may cause fab issues @ {}".format(coords))
        if self.tooth_width < 6:
            print("tooth_width < 6um may cause fab issues @ {}".format(coords))
        
        tf = np.tan(np.pi*self.taper_angle/180)

        len_unit = 2*(self.tooth_width + self.tooth_spacing)
        unit = [[(0,self.paddle_width),
                 (self.tooth_width+self.tooth_spacing,self.paddle_width),
                 (self.tooth_width+self.tooth_spacing,self.paddle_width+self.tooth_height),
                 (2*self.tooth_width+self.tooth_spacing,self.paddle_width+self.tooth_height),
                 (2*self.tooth_width+self.tooth_spacing,self.paddle_width)
                 ],
                [(0,self.paddle_width+self.paddle_gap-self.tooth_height),
                 (self.tooth_width,self.paddle_width+self.paddle_gap-self.tooth_height),
                 (self.tooth_width,self.paddle_width+self.paddle_gap),
                 (len_unit,self.paddle_width+self.paddle_gap),
                 ]
                ]
        
        pocket = [[(0,self.paddle_width),
                   (self.pocket_depth/np.tan(self.pocket_wall_angle*np.pi/180),self.paddle_width-self.pocket_depth),
                   (self.pocket_length-self.pocket_depth/np.tan(self.pocket_wall_angle*np.pi/180),self.paddle_width-self.pocket_depth),
                   (self.pocket_length,self.paddle_width)
                   ]]
        
        pocket.append(mirror_pts(pocket[0],0,(0,self.paddle_width + 0.5*self.paddle_gap)))
        
        num_units = np.floor((self.paddle_length - self.buffer)/len_unit).astype(int)
        
        paddle1 = [(0,0)]
        paddle2 = [(0,2*self.paddle_width+self.paddle_gap)]
        
        for n in range(num_units):
            paddle1 = paddle1 + translate_pts(unit[0],(n*len_unit,0))
            paddle2 = paddle2 + translate_pts(unit[1],(n*len_unit,0))
        
        rem = (self.paddle_length - self.buffer) % num_units
        if rem >= 2*self.tooth_width+self.tooth_spacing:
            paddle1 = paddle1 + translate_pts(unit[0],(num_units*len_unit,0))
            paddle2 = paddle2 + translate_pts(unit[1],(num_units*len_unit,0))
        elif rem >= self.tooth_width:
            paddle2 = paddle2 + translate_pts(unit[1],(num_units*len_unit,0))
        
        paddle1 = paddle1 + translate_pts(pocket[0],(self.paddle_length-self.pocket_offset-self.pocket_length,0))
        paddle2 = paddle2 + translate_pts(pocket[1],(self.paddle_length-self.pocket_offset-self.pocket_length,0))
        
        paddle1 = paddle1 + [(self.paddle_length,self.paddle_width),
                             (self.paddle_length,0),
                             (0,0)
                             ]
        paddle2 = paddle2 + [(self.paddle_length,self.paddle_width+self.paddle_gap),
                             (self.paddle_length,2*self.paddle_width+self.paddle_gap),
                             (0,2*self.paddle_width+self.paddle_gap)
                             ]
        
        if self.updown == 'up':
            paddle1 = mirror_pts(paddle1,90,(self.paddle_length/2,0))
            paddle2 = mirror_pts(paddle2,90,(self.paddle_length/2,0))
        elif self.updown != 'down':
            print('updown should be set to either \'up\' or \'down\', {} was passed instead'.format(self.updown))
        
        self.height = self.pin_gap - (self.gapw + 0.5*self.pinw) + 2*self.paddle_width + self.paddle_gap + self.v_padding
        self.length = self.paddle_length + 2*self.height/tf + 2*self.h_padding
        
        coords_p1 = orient_pt((self.offset+self.h_padding+self.height/tf,self.pin_gap + self.pinw/2),direction,coords)
        paddle1 = orient_pts(paddle1,direction,coords_p1)
        
        coords_p2 = orient_pt((self.offset+self.h_padding+self.height/tf,self.pin_gap + self.pinw/2),direction,coords)
        paddle2 = orient_pts(paddle2,direction,coords_p2)
        
        if self.leftright == 'left':
            paddle1 = mirror_pts(paddle1,direction,coords)
            paddle2 = mirror_pts(paddle2,direction,coords)
        
        s.drawing.append(sdxf.PolyLine(paddle1))
        s.drawing.append(sdxf.PolyLine(paddle2))
        
        QubitNotchFromJunc(s,settings = {'pinw': self.pinw,
                                          'gapw': self.gapw,
                                          'height': self.height,
                                          'length': self.length,
                                          'taper_angle': self.taper_angle,
                                          'leftright': self.leftright,
                                          'refjunc': self.refjunc,
                                          'offset': self.offset})
