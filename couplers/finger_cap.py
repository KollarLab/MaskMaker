from component import Component
from cpw.CPWLinearTaper import CPWLinearTaper
from pt_operations import rotate_pts, translate_pts, rotate_pt
from mask import MaskError
from junction import junction

class FingerCap(Component):
    """
    A CPW finger capacitor
    
    settings:
        num_fingers: total number of fingers between the two sides. must be at 
            least 2. 
        finger_length: length of fingers
        finger_width: width of fingers
        finger_gap: distance between fingers
        taper_length: length of CPWLinearTaper on either side of the capacitor
        cap_gapw: gapw of coupling section (surrounding fingers)
        cxn_pinw: pinw at connections
        cxn_gapw: gapw at connections
    """
    
    _defaults = {}
    _defaults['num_fingers'] = 6
    _defaults['finger_length'] = 45
    _defaults['finger_width'] = 6
    _defaults['finger_gap'] = 6
    _defaults['cap_gapw'] = None
    _defaults['taper_length'] = 40    
    _defaults['cxn_pinw'] = 20
    _defaults['cxn_gapw'] = 8.372
    
    def __init__(self,structure,settings={},startjunc=None,cxns_names=['in','out']):
        
        s=structure
        
        comp_key = 'FingerCap'
        global_keys = ['pinw','gapw']
        object_keys = ['cxn_pinw','cxn_gapw'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        
       #number of fingers
        
        self.pinw = self.num_fingers*self.finger_width+ (self.num_fingers-1)*self.finger_gap    #effective center pin width sum of finger gaps and widths
        self.length=self.finger_length+self.finger_gap
        self.total_length=self.finger_length+self.finger_gap+2.*self.taper_length

        pinw=self.pinw
        if self.cap_gapw is None: self.cap_gapw=self.pinw*self.cxn_gapw/self.cxn_pinw
        gapw=self.cap_gapw
        
        if startjunc is None:
            startjunc = s.last.copyjunc()
        else:
            s.last = startjunc.copyjunc()
        
        if self.num_fingers<2:
            raise MaskError("CPWFingerCap must have at least 2 fingers!")
        if self.finger_width < 6:
            print("finger_width < 6um may cause fab issues @ {}".format(startjunc.coords))
        if self.finger_width < 6:
            print("finger_gap < 6um may cause fab issues @ {}".format(startjunc.coords))
        
        self.cxns = {cxns_names[0]:startjunc.reverse()}
        
        CPWLinearTaper(structure, settings = {'length': self.taper_length,
                                              'start_pinw': self.cxn_pinw,
                                              'start_gapw': self.cxn_gapw,
                                              'stop_pinw': pinw,
                                              'stop_gapw': gapw
                                              })
        start=structure.last.coords
        
        
        center_width=self.num_fingers*self.finger_width+ (self.num_fingers-1)*self.finger_gap
        length=self.finger_length+self.finger_gap
        
        gap1=[  (start[0],start[1]-center_width/2),
                (start[0]+length,start[1]-center_width/2),
                (start[0]+length,start[1]-center_width/2-gapw),
                (start[0],start[1]-center_width/2-gapw),
                (start[0],start[1]-center_width/2)
            ]

        gap2=[  (start[0],start[1]+center_width/2),
                (start[0]+length,start[1]+center_width/2),
                (start[0]+length,start[1]+center_width/2+gapw),
                (start[0],start[1]+center_width/2+gapw),
                (start[0],start[1]+center_width/2)
            ]

        gap1=rotate_pts(gap1,s.last.direction,start)
        gap2=rotate_pts(gap2,s.last.direction,start)
        stop=rotate_pt((start[0]+length,start[1]),s.last.direction,start)
        s.last=junction(stop, s.last.direction)

        s.drawing.add_lwpolyline(gap1)
        s.drawing.add_lwpolyline(gap2)

        #draw finger gaps
        for ii in range(self.num_fingers-1):
            if ii%2==0:
                pts=self.left_finger_points(self.finger_width,self.finger_length,self.finger_gap)
            else:
                pts=self.right_finger_points(self.finger_width,self.finger_length,self.finger_gap)
            pts=translate_pts(pts,start)
            pts=translate_pts(pts,(0,ii*(self.finger_width+self.finger_gap)-self.pinw/2))
            pts=rotate_pts(pts,s.last.direction,start)
            s.drawing.add_lwpolyline(pts)

        #draw last little box to separate sides
        pts = [ (0,0),(0,self.finger_width),(self.finger_gap,self.finger_width),(self.finger_gap,0),(0,0)]
        pts=translate_pts(pts,start)
        #if odd number of fingers add box on left otherwise on right
        pts=translate_pts(pts,( ((self.num_fingers+1) %2)*(length-self.finger_gap),(self.num_fingers-1)*(self.finger_width+self.finger_gap)-self.pinw/2))
        pts=rotate_pts(pts,s.last.direction,start)
        s.drawing.add_lwpolyline(pts)
        
        CPWLinearTaper(structure, settings = {'length': self.taper_length,
                                              'start_pinw': pinw,
                                              'start_gapw': gapw,
                                              'stop_pinw': self.cxn_pinw,
                                              'stop_gapw': self.cxn_gapw
                                              })
         
        self.cxns[cxns_names[1]] = s.last.copyjunc()
       
    def left_finger_points(self,finger_width,finger_length,finger_gap):      
        pts= [  (0,0),
                (0,finger_width+finger_gap),
                (finger_length+finger_gap,finger_width+finger_gap),
                (finger_length+finger_gap,finger_width),
                (finger_gap,finger_width),
                (finger_gap,0),
                (0,0)
            ]
                
        return pts
        
    def right_finger_points(self,finger_width,finger_length,finger_gap):         
        pts = [ (finger_length+finger_gap,0),
                (finger_length+finger_gap,finger_width+finger_gap),
                (0,finger_width+finger_gap),
                (0,finger_width),
                (finger_length,finger_width),
                (finger_length,0),
                (finger_length+finger_gap,0)
                ]
        return pts
 