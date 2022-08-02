from component import Component
from cpw.CPWLinearTaper import CPWLinearTaper

import numpy as np
from pt_operations import rotate_pt

class ThreeWayCoupler(Component):
    """
    
    three-way coupler, ends of three waveguides taper to form a hexagon-like
        structure.
    
    settings:
        pinw: pinw of connections
        gapw: gapw of connections
        cap_edge: length of one of the inner edges of the cpw caps (roughly the
            radius of the inner polygon)
        coupler_radius: distance from center to midpoint of edge between
            connections
        coupling_distance: coupling distance between centerpins
        length: length of cpw caps, from connection to 120° point
    
    """
    
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['cap_edge'] = 40
    _defaults['coupler_radius'] = 50
    _defaults['coupling_distance'] = 6
    _defaults['length'] = 40
    
    def __init__(self,structure, settings = {}, startjunc = None, cxns_names = ['connA', 'connB', 'connC']):
        
        self.chip = structure
        s = self.chip
        
        #settings
        
        comp_key = 'ThreeWayCoupler'
        global_keys = ['pinw','gapw']
        object_keys = ['pinw','gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        settings = self.settings
        
        self.pinw = settings['pinw']
        self.gapw = settings['gapw']
        self.cap_edge = settings['cap_edge']
        self.coupler_radius = settings['coupler_radius']
        self.coupling_distance = settings['coupling_distance']/2
        self.length = settings['length']
        
        if startjunc is None:
            startjunc = s.last.copyjunc()
        else:
            s.last = startjunc.copyjunc()
        
        self.gap_to_center = self.coupling_distance/np.sin(np.pi/3)
        self.center = startjunc.add(rotate_pt((self.length+self.gap_to_center,0),startjunc.direction),-180)

        self.cxns = {cxns_names[0]:s.last.reverse()}
        self.arm()
        
        s.last = self.center.add(rotate_pt((self.length+self.gap_to_center,0),startjunc.direction+60),60)
        self.cxns[cxns_names[1]] = s.last.reverse()
        self.arm()
        
        s.last = self.center.add(rotate_pt((self.length+self.gap_to_center,0),startjunc.direction-60),-60)
        self.cxns[cxns_names[2]] = s.last.reverse()
        self.arm()
        
        s.last = self.cxns[cxns_names[2]]
        
    def arm(self):
        
        s = self.chip
        
        sf = np.sin(np.pi/3) #sin factor 
        cf = np.cos(np.pi/3) #cos factor
        tf = np.tan(np.pi/3) #tan factor
        
        lengths = [self.length+self.gap_to_center-cf*self.coupler_radius, cf*self.coupler_radius-self.gap_to_center-cf*self.cap_edge, cf*self.cap_edge, self.gap_to_center]
        
        pinbend_tf = (sf*self.cap_edge-self.pinw/2)/(lengths[0]+lengths[1])        

        pinh = [sf*self.cap_edge-pinbend_tf*lengths[1], sf*self.cap_edge, 0, 0]
        gaph = [sf*self.coupler_radius, sf*self.coupler_radius-tf*lengths[1], tf*self.gap_to_center,0]
        
        pinws = [self.pinw]
        gapws = [self.gapw]
        for n in range(4):
            pinws.append(2*pinh[n])
            gapws.append(gaph[n]-pinh[n])
        
        for n in range(4):
            CPWLinearTaper(s, settings = {'length': lengths[n],
                                          'start_pinw': pinws[n],
                                          'start_gapw': gapws[n],
                                          'stop_pinw': pinws[n+1],
                                          'stop_gapw': gapws[n+1]
                                          })
 