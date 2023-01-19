from cpw.CPWLinearTaper import CPWLinearTaper
from cpw.CPWStraight import CPWStraight
from component import Component

class Bondpad(Component):
    """
    
    creates a bondpad
        
    settings:
        pinw: pinw of connection
        gapw: gapw of connection
        launcher_pinw: max pinw of launcher (fattest part)
        launcher_gapw: max gapw of launcher (fattest part)
        taper_length: length to get from pinw/gapw to 
            launcher_pinw/launcher_gapw
        launcher_padding: gap on end of bondpad opposite connection
        bond_pad_length: length of fattest part of bondpad
        spec: see note below
        
        if spec is 'auto', 
            if startjunc is specified,
                the bondpad is a starting bondpad, and is drawn in the direction of 
                startjunc with the connection at startjunc (the rest of the bondpad 
                is drawn 'behind' startjunc)
            if startjunc is not specified
                the bondpad is an ending bondpad, and is drawn in the opposite 
                direction, with the connection at startjunc (the startjunc and the 
                connection end up being in opposite directions) 
        if spec is 'start'
            the bondpad is a starting bondpad
        if spec is 'end'
            the bondpad is an ending bondpad
    """
    _defaults = {}
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['launcher_pinw'] = 400
    _defaults['launcher_gapw'] = 167.44
    _defaults['taper_length'] = 300
    _defaults['launcher_padding'] = 167.44
    _defaults['bond_pad_length'] = 350
    _defaults['spec'] = 'auto'

    def __init__(self, structure, settings = {}, startjunc = None, cxns_names = ['out']):
        comp_key = 'Bondpad'
        global_keys = ['pinw','gapw']
        object_keys = ['pinw','gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
        s = structure
        
        if self.spec == 'start':
            s.last = startjunc.reverse()
        elif self.spec == 'end':
            startjunc = s.last.reverse()
        else:
            if startjunc is None: # end
                startjunc = s.last.reverse()
            else: # start
                s.last = startjunc.reverse()
        
        CPWLinearTaper(s, settings = {'length':self.taper_length,
                                      'start_pinw':self.pinw,
                                      'start_gapw':self.gapw,
                                      'stop_pinw':self.launcher_pinw,
                                      'stop_gapw':self.launcher_gapw
                                      })

        CPWStraight(s, settings = {'length':self.bond_pad_length,
                                   'pinw':self.launcher_pinw,
                                   'gapw':self.launcher_gapw
                                   })

        CPWStraight(s, settings = {'length':self.launcher_padding,
                                   'pinw':0,
                                   'gapw':self.launcher_pinw/2 + self.launcher_gapw
                                   })
        
        s.last = startjunc.copyjunc()
        
        self.cxns = {cxns_names[0]:startjunc.copyjunc()}

