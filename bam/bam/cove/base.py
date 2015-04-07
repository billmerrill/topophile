
class FourWallsBase(object):
    
    def __init__(self, top_corners, ceil_corners, floor_height):
        '''
        corners are four-tuples, starting +x+y and going counter-clockwise
        '''
        self.top_corners = top_corners
        self.ceil_corners = ceil_corners
        self.floor_height = floor_height
        
    def triangulate(self):
        ''' 
        Base normals are pointed negative Z, no need to invert
        '''
        oc = []
        for c in self.top_corners:
            oc.append((c[0], c[1], self.floor_height))
        ic = []
        for c in self.ceil_corners:
            ic.append((c[0], c[1], self.floor_height))
            
        tris = []
        for i,p in enumerate(self.top_corners):
            n = i%4
            tris.append((oc[i], ic[i], ic[n]))
            tris.append((oc[i], ic[n], oc[n]))
            
        return tris
        
        

class FourWallsModel(object):
    
    def __init__(self, top, ceiling, floor_height, wall_thickness):
        self.top = top
        self.ceiling = ceiling
        self.floor_height = floor_height
        self.wall_thickness = wall_thickness
        
    def triangulate(self):
        triangles = self.top.triangulate()
        triangles.extend(self.ceiling.triangulate(invert_normals=True))
        triangles.extend(self.triangulate_base())
        triangles.extend(self.triangulate_walls())
        
    def triangulate_base(self):
        pass
        
    def triangulate_walls(self):
        pass