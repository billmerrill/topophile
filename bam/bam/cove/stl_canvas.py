import struct
import math
import numpy as np
from numpy.linalg import norm
from indicies import *


class STLCanvas:

    def __init__(self):
        self.triangles = []

    def compute_normal(self, triangle):
        Nraw = np.cross(np.subtract(triangle[TA], triangle[TB]),
                        np.subtract(triangle[TA], triangle[TC]))
        hypo = math.sqrt(Nraw[PX]**2 + Nraw[PY]**2 + Nraw[PZ]**2)
        if hypo == 0:
            print "WARNING: divide by zero implies busted model"
            print triangle

        N = (Nraw[PX] / hypo,
             Nraw[PY] / hypo,
             Nraw[PZ] / hypo)
        return N

    def add_shape(self, shape):
        self.triangles.extend(shape.triangulate())

    def compute_area(self):
        area = 0.0
        for tri in self.triangles:
            area += .5 * \
                norm(np.cross(np.subtract(tri[TB], tri[TA]),
                              np.subtract(tri[TB], tri[TC])))
        return area

    def make_positive(self, base=[1, 1, 1]):
        ''' make sure all of the model is at or above base '''
        pts = np.array(
            [coord for tri in self.triangles for pt in tri for coord in pt])
        self.triangles = pts.reshape(-1, 3, 3)
        mmin = [self.triangles[:, :, PX].min(),
                self.triangles[:, :, PY].min(),
                self.triangles[:, :, PZ].min()]

        trans = np.subtract(base, mmin)
        if not np.equal(trans, [0.0, 0.0, 0.0]).all():
            self.triangles = np.add(self.triangles, trans)

    def write_stl(self, outfile, make_positive=True):
        '''
        outfile: string - filename for stl output
        make_positive: bool - STL requires positive values, zero values
                              are useful for previews
        '''
        print ("Writing %s triangles" % len(self.triangles))
        if make_positive:
            self.make_positive()
        with open(outfile, 'wb') as dest_file:
            dest_file.write(
                struct.pack("80sI", b'Quick Release Lever', len(self.triangles)))
            for tri in self.triangles:
                normal = self.compute_normal(tri)
                data = [normal[PX], normal[PY], normal[PZ],
                        tri[TA][PX], tri[TA][PY], tri[TA][PZ],
                        tri[TB][PX], tri[TB][PY], tri[TB][PZ],
                        tri[TC][PX], tri[TC][PY], tri[TC][PZ], 0]
                dest_file.write(struct.pack("12fH", *data))
