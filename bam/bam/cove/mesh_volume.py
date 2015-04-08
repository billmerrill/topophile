from indicies import *
import numpy as np
from numpy.linalg import norm

'''
methods for measuring the volume of a shape 
created by enclosing space of an elevation mesh
with an imaged floor
'''


def compute_exact_mesh_volume(mesh, floor_height):
    vol = 0.0
    for sy in range(0, mesh.y_max()):
        for sx in range(0, mesh.x_max()):
            vol += compute_elevation_facet_volume([mesh.get(sx,sy),
                                 mesh.get(sx, sy+1),
                                 mesh.get(sx+1, sy+1)],
                                 floor_height)
            vol += compute_elevation_facet_volume([mesh.get(sx,sy),
                              mesh.get(sx+1, sy),
                              mesh.get(sx+1, sy+1)],
                              floor_height)
    return vol

def compute_approx_mesh_volume(mesh, floor_height):
        '''
        Much faster than exact, avg the height of voxel's top
        verticies, use that to compute a box volume.
        '''
        
        def avg_height_volume(cell):
            q = np.array(cell)
            avg_height = np.mean(q[:, PZ])
            area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
            return area * (avg_height - floor_height)

        volume = 0.0
        for sy in range(0, mesh.y_max()):
            for sx in range(0, mesh.x_max()):
                volume += avg_height_volume([mesh.get(sx, sy),
                     mesh.get(sx+1, sy),
                     mesh.get(sx, sy+1),
                     mesh.get(sx+1, sy+1)])
        return volume       


def compute_approx_square_vol(q, bottom_height):   
    q = np.array(q)
    avg_height = np.mean(q[:,PZ])
    area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
    # print (q[3][PX] - q[0][PX]), (q[3][PY] - q[0][PY])
    # print area, avg_height
    return area * (avg_height - bottom_height)
    
def compute_approx_square_min_vol(q, bottom_height):
    q = np.array(q)
    height = np.min(q[:,PZ])
    area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
    # print (q[3][PX] - q[0][PX]), (q[3][PY] - q[0][PY])
    # print area, avg_height
    return area * (height - bottom_height)
    
def compute_approx_square_max_vol(q, bottom_height):
    q = np.array(q)
    height = np.max(q[:,PZ])
    area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
    # print (q[3][PX] - q[0][PX]), (q[3][PY] - q[0][PY])
    # print area, avg_height
    return area * (height - bottom_height)

def compute_polyhedron_volume(t):
    a,b,c,d = t
    return (1.0/6.0) * norm( 
        np.dot(np.subtract(a,d), 
            np.cross(
                np.subtract(b,d), 
                np.subtract(c,d))))
        
def compute_elevation_facet_volume(ele, floor):
    '''
    compute the volume under the elevation triangle facet, down to zero.
    assumes elevation is positive.
    
    The elevation triangle is described by the points Ea, Eb, Ec.
    
    break volume into two parts.
    1.
    A base triange at Z=0, described by points Ba, Bb, Bc.
    A triangular prism has triange B as a based, and rises to meet
    the lowest z value in the E.
    
    A divider triangle is created, Ea, Pb, Pc, this is the top of the 
    prism
    
    2.  
    The remainder of the volume is a pyramid defined by 
    EaEbEc and EaPbPc
    
    Divide that 5-sided poly into 2 tetrahedrons, compute their volume.
    
    '''
    
    # find the lowest point in the elevation triangle
    # axis[0] is the lowest
    E = np.array(ele)
    # print 'E', E
    minarg = np.argmin(E[:,PZ])
    axis = (minarg, (minarg+1)%3, (minarg+2)%3)

    base = E.copy()
    base[:,PZ] = floor 
    # print 'B', base
    
    base_area = .5 * norm(np.cross(
        np.subtract(base[TB], base[TA]), 
        np.subtract(base[TB], base[TC])))
    # print 'Base Area', base_area, base[axis[0]][PZ]
    prism_volume = base_area * (E[axis[0]][PZ] - floor)
 
    # pyramid triangle is the top of the prism, a side of the pyramid with E,
    # joined with E triangle at its lowest point, E[axis[0]]
    pyramid = E.copy()
    pyramid[axis[1]][PZ] = pyramid[axis[0]][PZ]
    pyramid[axis[2]][PZ] = pyramid[axis[0]][PZ]
    
    t1 = [E[axis[0]], E[axis[1]], E[axis[2]], pyramid[axis[1]]]
    t2 = [E[axis[0]], E[axis[2]], pyramid[axis[1]], pyramid[axis[2]]]
    
    t1_vol = compute_polyhedron_volume(t1)
    t2_vol = compute_polyhedron_volume(t2)
   
    # print "%s, %s, %s" % (prism_volume, t1_vol, t2_vol)
    return prism_volume + t1_vol + t2_vol