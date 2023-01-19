from cpw.CPWStraight import CPWStraight
from cpw.CPWBend import CPWBend
from pt_operations import rotate_pt
from component import Component

import numpy as np

class CouplingStraight(Component):
    """
    A hanger resonator coupled to a section of feedline. Currently, the ground
        plane remains between the two if coupling_gap>2*gapw
    settings:
        pinw: pinw
        gapw: gapw
        radius: radius of bend of hanger
        length: length of segment of feedline
        buffer: endcap of hanger
        coupling_gap: distance between centerpins
        coupling_straight: length of hanger straight
        add_hanger: if True, draws the first three pieces of the hanger as detailed below
        
        ---the direction of the feedline is UP---
        leftright: controls whether the hanger is to the left or right of the
            feedline. takes 'left' or 'right'
        updown: control whether the hanger points along the feedline or against
            it. 'up' goes along with the feedline, 'down' goes against
        
    the pieces of the hanger are drawn in the following order:
        1. endcap of length buffer
        2. straight of length coupling_straight
        3. 90° bend away from feedline of r = radius
        
    Additional methods:
        hanger_length: returns the length of the hanger
    """
    
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['radius'] = 100
    _defaults['length'] = 200
    _defaults['coupling_straight'] = 50
    _defaults['coupling_gap'] = 8.372
    _defaults['buffer'] = 40
    _defaults['leftright'] = 'right'
    _defaults['updown'] = 'down'
    _defaults['add_hanger'] = True
    
    def __init__(self, structure, settings = {}, startjunc = None, cxns_names=['in','out','hanger']):
        
        s = structure
        
        comp_key = 'CouplingStraight'
        global_keys = ['pinw','gapw','gapw','radius']
        object_keys = ['pinw','gapw','coupling_gap','radius'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        if startjunc is None:
            startjunc = s.last.copyjunc()
        else:
            s.last = startjunc.copyjunc()
        
        if self.leftright == 'right':
            lrc = -1
        elif self.leftright == 'left':
            lrc = 1
        else:
            lrc = -1
            print('Invalid argument for leftright, default value used')
        
        if self.updown == 'down':
            udc = 1
        elif self.updown == 'up':
            udc = 0
        else:
            udc = 1
            print('Invalid argument for updown, default value used')
        
        startjunc = startjunc.reverse()
        self.cxns = {cxns_names[0]:startjunc.copyjunc()}
        
        if (self.coupling_gap < self.gapw):
            print("WARNING: COUPLING_GAP MAY BE TOO SMALL AT {}".format(startjunc.coords))
        
        CPWStraight(s, settings = {'length':self.length,
                                   'pinw':self.pinw,
                                   'gapw':self.gapw
                                   })
        
        self.cxns[cxns_names[1]] = s.last.copyjunc()
        s.last = s.last.add(rotate_pt(((udc-1)*self.length,lrc*(self.pinw+self.coupling_gap)),s.last.direction),udc*180)
        
        if self.settings['add_hanger'] == True:
            CPWStraight(s, settings = {'length':self.buffer,
                                       'pinw':0,
                                       'gapw':self.gapw+self.pinw/2
                                       })
            CPWStraight(s, settings = {'length':self.coupling_straight,
                                       'pinw':self.pinw,
                                       'gapw':self.gapw
                                       })
            CPWBend(s, settings = {'turn_angle':lrc*(-2*udc+1)*90,
                                   'pinw':self.pinw,
                                   'gapw':self.gapw,
                                   'radius':self.radius
                                   })
        
        self.cxns[cxns_names[2]] = s.last.copyjunc()

        s.last = self.cxns[cxns_names[1]].copyjunc()
    
    def hanger_length(self):
        return self.coupling_straight + np.pi*self.radius/2

