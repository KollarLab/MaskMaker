import sdxf
from pt_operations import rotate_pts, rotate_pt
from junction import junction
from component import Component

class CPWStraight(Component):
    """
    A straight section of CPW transmission line
    """
    
    _defaults = {}
    _defaults['length'] = 100
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    
    def __init__(self,structure,startjunc=None,settings={}, cxns_names = ['in','out']):
        """ Adds a straight section of CPW transmission line of length = length to the structure"""        
        s=structure
        
        comp_key = 'CPWStraight'
        global_keys = ['pinw','gapw']
        object_keys = ['pinw','gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        settings = self.settings
        
        length = settings['length']
        pinw = settings['pinw']
        gapw = settings['gapw']
        
        if length==0: return
        
        if startjunc is None: startjunc=s.last.copyjunc()
            
        coords = startjunc.coords
        
        gap1=[  (coords[0],coords[1]+pinw/2),
                (coords[0]+length,coords[1]+pinw/2),
                (coords[0]+length,coords[1]+pinw/2+gapw),
                (coords[0],coords[1]+pinw/2+gapw),
                (coords[0],coords[1]+pinw/2)
                ]

        gap2=[  (coords[0],coords[1]-pinw/2),
                (coords[0]+length,coords[1]-pinw/2),
                (coords[0]+length,coords[1]-pinw/2-gapw),
                (coords[0],coords[1]-pinw/2-gapw),
                (coords[0],coords[1]-pinw/2)
                ]
        
        gap1=rotate_pts(gap1,startjunc.direction,coords)
        gap2=rotate_pts(gap2,startjunc.direction,coords)
        
        stop_coords=rotate_pt((coords[0]+length,coords[1]),startjunc.direction,coords)
        stopjunc=junction(stop_coords,startjunc.direction)
        
        s.last = stopjunc.copyjunc()
        
        s.drawing.append(sdxf.PolyLine(gap1))
        s.drawing.append(sdxf.PolyLine(gap2))
    
        startjunc = startjunc.reverse()
                
        self.cxns = {cxns_names[0]:startjunc, cxns_names[1]:stopjunc}

