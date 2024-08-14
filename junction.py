import numpy as np

class Junction():
    """
    junction is an object that just contains tuple coordinates and a direction
    the idea is that at some point, the user can draw CPWs using functions like
        connect(junc1,junc2)
    the cxns attribute for each CPW component is a dictionary of junctions
    the last attribute of Chip, which is used to keep track of the current
        location and direction, is a junction (changed from MMP, where 
        location and direction were stored differently)
        
    attributes:
        copyjunc: returns a copy of the function. unsure if this is useful,
            i was just unsure about the way python handles memory. i didn't
            want to run into an issue where copying the junction in Chip.last
            caused a connection between for example a junction in cxns and the
            current position
        add: returns a junction with (x,y) offset and a change in direction
        reverse: just adds 180 to direction and returns the new junction
        
    neither reverse nor add modify the original junction
        
    """
    def __init__(self,coords,direction):
        if type(coords) == tuple and (type(direction) == float or type(direction) == int):
            if len(coords) == 2:
                if (np.isscalar(coords[0]) == True) and (np.isscalar(coords[1]) == True):
                    self.coords = coords
                    self.direction = direction
                else:
                    raise TypeError("coordinates must contain two scalars")
                    return
            else:
                raise TypeError("coordinates must contain two numbers")
                return
        else:
            raise TypeError("junction coordinates not a tuple or junction direction not a number")
            return
    def __str__(self):
        return f'junction at {self.coords} facing {self.direction} degrees'
    def copyjunc(self):
        return Junction(self.coords,self.direction)
    def add(self,coords,direction):
        net_direction = (self.direction + direction) % 360
        return Junction((self.coords[0]+coords[0],self.coords[1]+coords[1]),net_direction)
    def reverse(self):
        net_direction = (self.direction + 180) % 360
        return Junction(self.coords,net_direction)