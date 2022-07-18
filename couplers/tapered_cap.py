from component import Component
from cpw.CPWLinearTaper import CPWLinearTaper
from cpw.CPWStraight import CPWStraight

class TaperedCap(Component):
    """
    
    Similar to a GapCap, but the centerpins are tapered at the gap
    
    settings:
        pinw_start: pinw at connection
        pinw_stop: pinw at cap gap
        gapw_start: gapw at connection
        gapw_stop: gapw at cap gap
        length: length of linear tapers (not including gap)
        gap: distance between pins
    """
    
    _defaults = {}
    _defaults['pinw_start'] = 20
    _defaults['gapw_start'] = 8.372
    _defaults['pinw_stop'] = 2*20
    _defaults['gapw_stop'] = 2*8.372
    _defaults['length'] = 40
    _defaults['gap'] = 10
    
    def __init__(self, structure, settings = {}, startjunc = None, cxns_names=['in','out']):
        
        s = structure
        
        if startjunc is None:
            startjunc = s.last.copyjunc()
        else:
            s.last = startjunc.copyjunc()
        
        startjunc = startjunc.reverse()
        
        comp_key = 'TaperedCap'
        global_keys = ['pinw','gapw']
        object_keys = ['pinw_start','gapw_start'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        CPWLinearTaper(s, settings = {'length': self.length/2,
                                      'start_pinw': self.pinw_start,
                                      'start_gapw': self.gapw_start,
                                      'stop_pinw': self.pinw_stop,
                                      'stop_gapw': self.gapw_stop
                                      })
        CPWStraight(s, settings = {'length':self.gap,
                                   'pinw':0,
                                   'gapw':self.gapw_stop+self.pinw_stop/2
                                   })
        CPWLinearTaper(s, settings = {'length': self.length/2,
                                      'start_pinw': self.pinw_stop,
                                      'start_gapw': self.gapw_stop,
                                      'stop_pinw': self.pinw_start,
                                      'stop_gapw': self.gapw_start
                                      })
        
        self.cxns = {cxns_names[0]:startjunc.copyjunc(),cxns_names[1]:s.last.copyjunc()}
        