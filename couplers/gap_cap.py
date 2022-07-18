from component import Component
from cpw.CPWStraight import CPWStraight

class GapCap(Component):
    """
    
    Capacitor formed by simply putting a gap between two head-on centerpins
    
    settings:
        pinw: pinw
        gapw: gapw
        gap: coupling distance
        buffer: length of CPWStraights on either end
    
    """
    
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['gap'] = 15
    _defaults['buffer'] = 10
    
    def __init__(self, structure, settings = {}, startjunc = None, cxns_names=['in','out']):
        
        s = structure
        
        if startjunc is None:
            startjunc = s.last.copyjunc()
        else:
            s.last = startjunc.copyjunc()
        
        startjunc = startjunc.reverse()
        
        comp_key = 'GapCap'
        global_keys = ['pinw','gapw']
        object_keys = ['pinw','gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        CPWStraight(s, settings = {'length':self.buffer,
                                   'pinw':self.pinw,
                                   'gapw':self.gapw
                                   })
        CPWStraight(s, settings = {'length':self.gap,
                                   'pinw':0,
                                   'gapw':self.gapw+self.pinw/2
                                   })
        CPWStraight(s, settings = {'length':self.buffer,
                                   'pinw':self.pinw,
                                   'gapw':self.gapw
                                   })
        
        self.cxns = {cxns_names[0]:startjunc.copyjunc(),cxns_names[1]:s.last.copyjunc()}

