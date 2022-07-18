from numpy import sin, cos, pi

def rotate_pt(p,angle,center=(0,0)):
    """rotates point p=(x,y) about point center (defaults to (0,0)) by CCW angle (in degrees)"""
    dx=p[0]-center[0]
    dy=p[1]-center[1]
    theta=pi*angle/180
    return (center[0]+dx*cos(theta)-dy * sin(theta),center[1]+dx * sin(theta)+dy * cos(theta))
        
def rotate_pts(points,angle,center=(0,0)):
    """Rotates an array of points one by one using rotate_pt"""
    return [rotate_pt(p,angle,center) for p in points]

def translate_pt(p,offset):
    """Translates point p=(x,y) by offset=(x,y)"""
    return (p[0]+offset[0],p[1]+offset[1])

def translate_pts(points,offset):
    """Translates an array of points one by one using translate_pt"""
    return [translate_pt(p,offset) for p in points]

def orient_pt(p,angle,offset):
    """Orient_pt rotates point p=(x,y) by angle (in degrees) and then translates it to offset=(x,y)"""
    return translate_pt(rotate_pt(p,angle),offset)

def orient_pts(points,angle,offset):
    """Orients an array of points one by one using orient_pt"""
    return [orient_pt(p,angle,offset) for p in points]

def scale_pt(p,scale):
    """Scales p=(x,y) by scale"""
    return (p[0]*scale[0],p[1]*scale[1])

def scale_pts(points,scale):
    """Scales an array of points one by one using scale_pt"""    
    return [scale_pt(p,scale) for p in points]

def mirror_pt(p, axis_angle,axis_pt):
    """Mirrors point p about a line at angle "axis_angle" intercepting point "axis_pt" """
    theta=axis_angle*pi/180.
    return (axis_pt[0] + (-axis_pt[0] + p[0])* cos(2 * theta ) + (-axis_pt[1] + p[1])*sin(2 *theta), 
            p[1] + 2 * (axis_pt[1] - p[1])* cos(theta)**2 + (-axis_pt[0] + p[0])* sin(2*theta) )

def mirror_pts(points,axis_angle,axis_pt):
    """Mirrors an array of points one by one using mirror_pt"""    
    return [mirror_pt(p,axis_angle,axis_pt) for p in points]

def rectangle_points(size,orientation=0,center=(0,0)):
    return orient_pts([ (-size[0]/2.,-size[1]/2.),(size[0]/2.,-size[1]/2.),(size[0]/2.,size[1]/2.),(-size[0]/2.,size[1]/2.),(-size[0]/2.,-size[1]/2.)],orientation,center)

def arc_pts(start_angle,stop_angle,radius,segments=360):
    pts=[]
    for ii in range(segments):
        theta=(start_angle+ii/(segments-1.)*(stop_angle-start_angle))*pi/180.
        p=(radius*cos(theta),radius*sin(theta))
        pts.append(p)
    return pts