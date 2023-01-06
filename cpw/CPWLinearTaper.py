from pt_operations import rotate_pt, rotate_pts
import sdxf
from junction import junction
from component import Component

class CPWLinearTaper(Component):
    """A section of CPW which (linearly) tapers from one set of start_pinw and start_gapw to stop_pinw and stop_gapw over length=length"""
    
    _defaults = {}
    _defaults['length'] = 100
    _defaults['start_pinw'] = 20
    _defaults['stop_pinw'] = 20
    _defaults['start_gapw'] = 8.372
    _defaults['stop_gapw'] = 8.372
    
    def __init__(self, structure,startjunc=None, settings = {}, cxns_names=['in','out']):
        #load attributes
        s=structure
        
        comp_key = 'CPWLinearStraight'
        global_keys = ['pinw','pinw','gapw','gapw']
        object_keys = ['start_pinw','stop_pinw','start_gapw','stop_gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        settings = self.settings
        
        if startjunc is None: startjunc=s.last.copyjunc()
        
        if self.length==0:
                s.last = startjunc.copyjunc()
                return
        
        coords = startjunc.coords
        #define geometry of gaps
        gap1= [ 
            (coords[0],coords[1]+self.start_pinw/2),
            (coords[0]+self.length,coords[1]+self.stop_pinw/2),
            (coords[0]+self.length,coords[1]+self.stop_pinw/2+self.stop_gapw),
            (coords[0],coords[1]+self.start_pinw/2+self.start_gapw),
            (coords[0],coords[1]+self.start_pinw/2)
            ]
                    
        gap2= [ 
            (coords[0],coords[1]-self.start_pinw/2),
            (coords[0]+self.length,coords[1]-self.stop_pinw/2),
            (coords[0]+self.length,coords[1]-self.stop_pinw/2-self.stop_gapw),
            (coords[0],coords[1]-self.start_pinw/2-self.start_gapw),
            (coords[0],coords[1]-self.start_pinw/2)
            ]
        
        #rotate structure to proper orientation
        gap1=rotate_pts(gap1,startjunc.direction,coords)
        gap2=rotate_pts(gap2,startjunc.direction,coords)

        #create polylines and append to drawing
        s.drawing.append(sdxf.PolyLine(gap1))
        s.drawing.append(sdxf.PolyLine(gap2))
        
        #update last anchor position
        stop_coords=rotate_pt((coords[0]+self.length,coords[1]),startjunc.direction,coords)
        stopjunc = junction(stop_coords,startjunc.direction)
        s.last=stopjunc.copyjunc()
        
        startjunc.direction = startjunc.direction - 180
        self.cxns = {cxns_names[0]:startjunc, cxns_names[1]:stopjunc}