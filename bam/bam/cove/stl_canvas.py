import struct
import math
import numpy as np
from numpy.linalg import norm

from indicies import *

class STLCanvas:
    
    def __init__(self):
        self.triangles = []
        
    def compute_normal(self, triangle):
        Nraw = np.cross( np.subtract(triangle[TA], triangle[TB]),
                                   np.subtract(triangle[TA], triangle[TC]) )
        hypo = math.sqrt(Nraw[PX]**2 + Nraw[PY]**2 + Nraw[PZ]**2)
        N = (Nraw[PX] / hypo,
             Nraw[PY] / hypo,
             Nraw[PZ] / hypo)
        return N

    def add_shape(self, shape):
        self.triangles.extend(shape.triangulate())
    
    def compute_area(self):
        area = 0.0
        for tri in self.triangles:
            area += .5 * norm( np.cross( np.subtract(tri[TB], tri[TA]), np.subtract(tri[TB], tri[TC])))
        return area
            
        
    def make_positive(self, base=[1,1,1]):
        thresh = [1,1,1]
        for tx, tri in enumerate(self.triangles):
            for pt in [TA, TB, TC]:
                thresh[PX] = min(thresh[PX], tri[pt][PX])
                thresh[PY] = min(thresh[PY], tri[pt][PY])
                thresh[PZ] = min(thresh[PZ], tri[pt][PZ])

        if thresh != base:
            inc = np.subtract(base, thresh)
            print("Moving model by %s" % inc)
            for tx, tri in enumerate(self.triangles):
                for pt in [TA,TB,TC]:
                    self.triangles[tx][pt] = np.add(tri[pt], inc)
        
    def write_stl(self, outfile):
        print ("Writing %s triangles" % len(self.triangles))
        # self.make_positive()
        with open(outfile, 'wb') as dest_file:
            dest_file.write(struct.pack("80sI", b'Quick Release Lever', len(self.triangles)))
            for tri in self.triangles:
                normal = self.compute_normal(tri)
                data = [normal[PX], normal[PY], normal[PZ],
                    tri[TA][PX], tri[TA][PY], tri[TA][PZ],
                    tri[TB][PX], tri[TB][PY], tri[TB][PZ],
                    tri[TC][PX], tri[TC][PY], tri[TC][PZ],0]
                dest_file.write(struct.pack("12fH", *data))

