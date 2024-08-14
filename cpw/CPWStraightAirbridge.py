import sdxf
from pt_operations import rotate_pts, rotate_pt
from junction import Junction
from component import Component

class CPWStraight_AB(Component):
    """
    A straight section of CPW transmission line
    """
    
    _defaults = {}
    _defaults['length'] = 100
    _defaults['pinw'] = 20
    _defaults['gapw'] = 8.372
    _defaults['ABwidth'] = 40
    _defaults['ABheight'] = 40
    _defaults['ABlength'] = 60 # or 50
    _defaults['ABgap'] = 200
    _defaults['ABstep2gap'] = 5
    
    def __init__(self,structure,startjunc=None,settings={}, cxns_names = ['in','out']):
        """ Adds a straight section of CPW transmission line of length = length to the structure"""        
        s=structure
        
        comp_key = 'CPWStraight'
        global_keys = ['pinw','gapw','ABwidth','ABheight','ABlength','ABgap','ABstep2gap']
        object_keys = ['pinw','gapw','ABwidth','ABheight','ABlength','ABgap','ABstep2gap'] # which correspond to the extract global_keys
        Component.__init__(self,structure,comp_key,global_keys,object_keys,settings)
        settings = self.settings
        
        length = settings['length']
        pinw = settings['pinw']
        gapw = settings['gapw']
        ABwidth = settings['ABwidth']
        ABheight = settings['ABheight']
        ABlength = settings['ABlength']
        ABgap = settings['ABgap']
        ABstep2gap = settings['ABstep2gap']
                
        if startjunc is None: startjunc=s.last.copyjunc()
        
        if self.length==0: 
                s.last = startjunc.copyjunc()
                return

        coords = startjunc.coords
        
        gap1=[(coords[0],coords[1]+pinw/2),
              (coords[0]+length,coords[1]+pinw/2),
              (coords[0]+length,coords[1]+pinw/2+gapw),
              (coords[0],coords[1]+pinw/2+gapw),
              (coords[0],coords[1]+pinw/2)]

        gap2=[(coords[0],coords[1]-pinw/2),
              (coords[0]+length,coords[1]-pinw/2),
              (coords[0]+length,coords[1]-pinw/2-gapw),
              (coords[0],coords[1]-pinw/2-gapw),
              (coords[0],coords[1]-pinw/2)]
        

        # ABgap
        ABnum = int((length/2)/ABgap)
        if (ABnum*ABgap + (1/2)*ABwidth) <= length/2:
            iter_num = ABnum
        else: 
            iter_num = ABnum-1

        if 200 <= length:
        # ABbox1 : top abstep1
        # ABbox2 : bottom abstep1
        # ABbox3 : abstep2
             ABbox1 = []
             ABbox2 = []
             ABbox3 = []
             ABbox1.append([(coords[0]+length/2-ABwidth/2,coords[1]+ABlength/2), 
                            (coords[0]+length/2+ABwidth/2,coords[1]+ABlength/2), 
                            (coords[0]+length/2+ABwidth/2,coords[1]+ABlength/2+ABheight), 
                            (coords[0]+length/2-ABwidth/2,coords[1]+ABlength/2+ABheight), 
                            (coords[0]+length/2-ABwidth/2,coords[1]+ABlength/2)])
             ABbox2.append([(coords[0]+length/2-ABwidth/2,coords[1]-ABlength/2), 
                            (coords[0]+length/2+ABwidth/2,coords[1]-ABlength/2), 
                            (coords[0]+length/2+ABwidth/2,coords[1]-ABlength/2-ABheight), 
                            (coords[0]+length/2-ABwidth/2,coords[1]-ABlength/2-ABheight), 
                            (coords[0]+length/2-ABwidth/2,coords[1]-ABlength/2)])
             ABbox3.append([(coords[0]+length/2-ABwidth/2-ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap), 
                            (coords[0]+length/2+ABwidth/2+ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap), 
                            (coords[0]+length/2+ABwidth/2+ABstep2gap,coords[1]-ABlength/2-ABheight-ABstep2gap), 
                            (coords[0]+length/2-ABwidth/2-ABstep2gap,coords[1]-ABlength/2-ABheight-ABstep2gap), 
                            (coords[0]+length/2-ABwidth/2-ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap)])
             #right ABbox
             for i in range(iter_num):
                ABbox1.append([(coords[0]+length/2-ABwidth/2+ABgap*(i+1),coords[1]+ABlength/2), 
                               (coords[0]+length/2+ABwidth/2+ABgap*(i+1),coords[1]+ABlength/2), 
                               (coords[0]+length/2+ABwidth/2+ABgap*(i+1),coords[1]+ABlength/2+ABheight), 
                               (coords[0]+length/2-ABwidth/2+ABgap*(i+1),coords[1]+ABlength/2+ABheight), 
                               (coords[0]+length/2-ABwidth/2+ABgap*(i+1),coords[1]+ABlength/2)])
                ABbox2.append([(coords[0]+length/2-ABwidth/2+ABgap*(i+1),coords[1]-ABlength/2), 
                               (coords[0]+length/2+ABwidth/2+ABgap*(i+1),coords[1]-ABlength/2), 
                               (coords[0]+length/2+ABwidth/2+ABgap*(i+1),coords[1]-ABlength/2-ABheight), 
                               (coords[0]+length/2-ABwidth/2+ABgap*(i+1),coords[1]-ABlength/2-ABheight), 
                               (coords[0]+length/2-ABwidth/2+ABgap*(i+1),coords[1]-ABlength/2)])
                ABbox3.append([(coords[0]+length/2-ABwidth/2+ABgap*(i+1)-ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap), 
                               (coords[0]+length/2+ABwidth/2+ABgap*(i+1)+ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap), 
                               (coords[0]+length/2+ABwidth/2+ABgap*(i+1)+ABstep2gap,coords[1]-ABlength/2-ABheight-ABstep2gap), 
                               (coords[0]+length/2-ABwidth/2+ABgap*(i+1)-ABstep2gap,coords[1]-ABlength/2-ABheight-ABstep2gap), 
                               (coords[0]+length/2-ABwidth/2+ABgap*(i+1)-ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap)])
             # left ABbox
             for i in range(iter_num):
                ABbox1.append([(coords[0]+length/2-ABwidth/2-ABgap*(i+1),coords[1]+ABlength/2), 
                               (coords[0]+length/2+ABwidth/2-ABgap*(i+1),coords[1]+ABlength/2), 
                               (coords[0]+length/2+ABwidth/2-ABgap*(i+1),coords[1]+ABlength/2+ABheight), 
                               (coords[0]+length/2-ABwidth/2-ABgap*(i+1),coords[1]+ABlength/2+ABheight), 
                               (coords[0]+length/2-ABwidth/2-ABgap*(i+1),coords[1]+ABlength/2)])
                ABbox2.append([(coords[0]+length/2-ABwidth/2-ABgap*(i+1),coords[1]-ABlength/2), 
                               (coords[0]+length/2+ABwidth/2-ABgap*(i+1),coords[1]-ABlength/2), 
                               (coords[0]+length/2+ABwidth/2-ABgap*(i+1),coords[1]-ABlength/2-ABheight), 
                               (coords[0]+length/2-ABwidth/2-ABgap*(i+1),coords[1]-ABlength/2-ABheight), 
                               (coords[0]+length/2-ABwidth/2-ABgap*(i+1),coords[1]-ABlength/2)])
                ABbox3.append([(coords[0]+length/2-ABwidth/2-ABgap*(i+1)-ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap), 
                               (coords[0]+length/2+ABwidth/2-ABgap*(i+1)+ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap), 
                               (coords[0]+length/2+ABwidth/2-ABgap*(i+1)+ABstep2gap,coords[1]-ABlength/2-ABheight-ABstep2gap), 
                               (coords[0]+length/2-ABwidth/2-ABgap*(i+1)-ABstep2gap,coords[1]-ABlength/2-ABheight-ABstep2gap), 
                               (coords[0]+length/2-ABwidth/2-ABgap*(i+1)-ABstep2gap,coords[1]+ABlength/2+ABheight+ABstep2gap)])
             for i in range(2*iter_num+1):
                ABbox1[i] = rotate_pts(ABbox1[i],startjunc.direction,coords)
                ABbox2[i] = rotate_pts(ABbox2[i],startjunc.direction,coords)
                ABbox3[i] = rotate_pts(ABbox3[i],startjunc.direction,coords)

        # return list in rotate_pts
        gap1=rotate_pts(gap1,startjunc.direction,coords)
        gap2=rotate_pts(gap2,startjunc.direction,coords)


        

        # stop coord
        stop_coords=rotate_pt((coords[0]+length,coords[1]),startjunc.direction,coords)
        stopjunc=Junction(stop_coords,startjunc.direction)
        
        s.last = stopjunc.copyjunc()
        

        # Draw box
        s.drawing.add_lwpolyline(gap1)
        s.drawing.add_lwpolyline(gap2)
        if 200 <= length:
            for i in range(2*iter_num+1):
                s.drawing.add_lwpolyline(ABbox1[i])
                s.drawing.add_lwpolyline(ABbox2[i])
                s.drawing.add_lwpolyline(ABbox3[i])

        startjunc = startjunc.reverse()
                
        self.cxns = {cxns_names[0]:startjunc, cxns_names[1]:stopjunc}

