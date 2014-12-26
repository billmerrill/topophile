import math
from indicies import * 
import numpy as np
from numpy.linalg import norm
import copy
from pprint import pprint

class CanvasShape(object):
    
    def get_triangles(self):
        pass 

class GridShape(object):
    
    def triangulate_square(self, square, invert_normal = False):
        ''' assume points like this for right hand rule
            0  1
            2  3
        '''
        tri = []
        if invert_normal:
            return [[square[0], square[1], square[3]],
                   [square[0], square[3], square[2]]]
        else:
            return [[square[0], square[3], square[1]],
                   [square[0], square[2], square[3]]]   
                   
                   
class MeshSandwich(GridShape):
    def __init__(self, top, bottom):
        if not (top.xsize == bottom.xsize and top.ysize == bottom.ysize):
            print ("CANT MAKE SAMMICHES")
            return
        self.xsize = top.xsize
        self.ysize = top.ysize
        self.top = top
        self.bottom = bottom
        
    def triangulate(self):
        triangles = self.top.triangulate()
        triangles.extend(self.bottom.triangulate())
        triangles.extend(self.triangulate_sides())    
        return triangles
    
    def triangulate_sides(self):
        triangles = []
        for sy in range(0, self.top.y_max()):
            triangles.extend(self.triangulate_square([self.top.get(0,sy),
                             self.top.get(0,sy+1),
                             self.bottom.get(0,sy),
                             self.bottom.get(0,sy+1)]))
            triangles.extend(self.triangulate_square([self.top.get(self.top.x_max(), sy+1),
                             self.top.get(self.top.x_max(), sy),
                             self.bottom.get(self.bottom.x_max(), sy+1),
                             self.bottom.get(self.bottom.x_max(), sy)]))
            
                            
        for sx in range(0, self.top.x_max()):
            triangles.extend(self.triangulate_square([self.top.get(sx+1,0),
                             self.top.get(sx,0),
                             self.bottom.get(sx+1,0),
                             self.bottom.get(sx,0)]))
            triangles.extend(self.triangulate_square([self.top.get(sx, self.top.y_max()),
                             self.top.get(sx+1, self.top.y_max()),
                             self.bottom.get(sx, self.bottom.y_max()),
                             self.bottom.get(sx+1, self.bottom.y_max())]))
                             
        return triangles
        
    def compute_volume(self):
        vol = 0.0
        for sy in range(0, self.top.y_max()):
            for sx in range(0, self.top.x_max()):
                vol += compute_elevation_facet_volume([self.top.get(sx,sy),
                                     self.top.get(sx, sy+1),
                                     self.top.get(sx+1, sy+1)],
                                     self.bottom.elevation)
                vol += compute_elevation_facet_volume([self.top.get(sx,sy),
                                  self.top.get(sx+1, sy),
                                  self.top.get(sx+1, sy+1)],
                                  self.bottom.elevation)
        
        return vol
        
    def compute_approx_volume(self):
        vol = {'min': 0.0,
                'avg': 0.0,
                'max': 0.0}
        # vol = 0.0
        corner0 = self.top.get(0,0)
        corner1 = self.top.get(self.top.x_max(), self.top.y_max())
        print (corner1[PX] - corner0[PY]), (corner1[PY] - corner0[PY])
        
        for sy in range(0, self.top.y_max()):
            for sx in range(0, self.top.x_max()):
                q = [self.top.get(sx, sy),
                     self.top.get(sx+1, sy),
                     self.top.get(sx, sy+1),
                     self.top.get(sx+1, sy+1)]
                vol['avg'] += compute_approx_square_vol(q)
                vol['min'] += compute_approx_square_min_vol(q)
                vol['max'] += compute_approx_square_max_vol(q)
                                 
        return vol

def compute_approx_square_vol(q):
    q = np.array(q)
    avg_height = np.mean(q[:,PZ])
    area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
    # print (q[3][PX] - q[0][PX]), (q[3][PY] - q[0][PY])
    # print area, avg_height
    return area * avg_height
    
def compute_approx_square_min_vol(q):
    q = np.array(q)
    height = np.min(q[:,PZ])
    area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
    # print (q[3][PX] - q[0][PX]), (q[3][PY] - q[0][PY])
    # print area, avg_height
    return area * height
    
def compute_approx_square_max_vol(q):
    q = np.array(q)
    height = np.max(q[:,PZ])
    area = abs((q[3][PX] - q[0][PX]) * (q[3][PY] - q[0][PY]))
    # print (q[3][PX] - q[0][PX]), (q[3][PY] - q[0][PY])
    # print area, avg_height
    return area * height
    
       
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

class Mesh(GridShape):
    
    def __init__(self, xsize=0, ysize=0):
        self.xsize = xsize 
        self.ysize = ysize
        self.mesh = []
            
    def triangulate(self, invert_normal = False):
        triangles = []
        for sy in range(0, self.y_max()):
            for sx in range(0, self.x_max()):
                triangles.extend(self.triangulate_square([self.get(sx,sy),
                                     self.get(sx+1, sy),
                                     self.get(sx, sy+1),
                                     self.get(sx+1, sy+1)], 
                                     invert_normal))        
                                 
        return triangles
    

    def add_row(self, row):
        self.mesh.append(row)
        
    def x_max(self):
        return self.xsize-1
        
    def y_max(self):
        return self.ysize-1
        
    def __str__(self):
        strs = []
        for i in range(0, len(self.mesh)):
            strs.append(", ".join([str(x) for x in self.mesh[i]]))
        return "\n".join(strs)
               
    def copy(self, src, scalar = [1,1,1], translate = [0,0,0]):
        self.xsize = src.xsize
        self.ysize = src.ysize
        self.mesh = copy.deepcopy(src.mesh)
        self.transform(scalar, translate)
                                   
    def get_data_x_size(self):
        return abs(self.mesh[0][self.x_max()][PX] - self.mesh[0][0][PX])
        
    def get_data_y_size(self):
        return abs(self.mesh[self.y_max()][0][PY] - self.mesh[0][0][PY])
        
    def get_max_corner(self):
        return self.mesh[self.y_max()][self.x_max()]
        
    def get_low_z(self):
        return np.min(self.mesh[:,:,PZ])

    def get_high_z(self):
        return np.max(self.mesh[:,:,PZ])

    
    def get(self, x, y):
        return self.mesh[y][x]
        

    def transform(self, scalar, translate):
        self.mesh = np.multiply(scalar, self.mesh)
        self.mesh = np.add(translate, self.mesh)
        return self 
    
    def load_matrix(self, src):
        '''
        src: a 2 dimensional python array
        '''
        self.mesh = copy.deepcopy(src)
        self.ysize = len(src)
        self.xsize = len(src[0])
        
    def scale_to_output_size(self, max_output_size):
        input_max_data_size = max(self.get_data_x_size(), self.get_data_y_size())
        output_ratio = max_output_size / input_max_data_size
        self.transform([output_ratio, output_ratio, output_ratio], [0,0,0])
     
    def finalize_form(self, max_output_size, min_elevation, z_factor):
        largest_data_dim = max(self.get_data_x_size(), self.get_data_y_size())     
        ratio = max_output_size / largest_data_dim
        # self.transform([output_ratio, output_ratio, output_ratio])
        self.mesh = np.multiply([ratio, ratio, ratio * z_factor], self.mesh)
        
        translate_v  = [0,0,0]
        low_z = self.get_low_z()
        if low_z < min_elevation:
            self.mesh = self.mesh + [0,0, min_elevation - low_z]
            
    def create_ceiling(self, nz_mm, d_mesh_size):
        '''
        nz_mm: the size, in mm, of the walls of the hollowed model
        ceil_size: the resolution of the ceiling mesh
        '''
        nz_mm = np.array(nz_mm)
        
        pix_mm = [ abs(self.mesh[0][1][PX] - self.mesh[0][0][PX]),
                   abs(self.mesh[0][0][PY] - self.mesh[1][0][PY])]     
                   
              
        # number of pixels to skip on the borders     
        nz_pix = np.floor(nz_mm[0:1] / pix_mm)
        for a in [0,1]:
            if nz_pix[a] == 0:
                nx_pix[a] = 1
        
       
        # window on mesh data to be decimated
        src = self.mesh[nz_pix[PY]:-nz_pix[PY], nz_pix[PX]:-nz_pix[PX] ]
        
        #add 2 for the border values
        # dst = np.ndarray((dmesh_size[PY]+2, dmesh_size[PX]+2, 3))
        
        full_ceiling_mesh = np.ndarray((d_mesh_size[PY]+2, d_mesh_size[PX]+2, 3))

        cell_mesh = full_ceiling_mesh[1:-1,1:-1]
        
 
        # dst = np.ndarray((d_mesh_size[PY], d_mesh_size[PX], 3))
        # cell_mesh = np.ndarray((d_mesh_size[PY], d_mesh_size[PX], 3))
        cell_mesh_shape = np.array(cell_mesh.shape)

        #sample cell size in pixels
        pix_per_cell = np.floor(np.divide(src.shape, cell_mesh.shape))
        # the fractional remainder of the cell division
        fstep = np.modf(np.divide(src.shape, cell_mesh_shape.astype(float)))[0]
        
        
        # smooth the remainders out over the width of the mesh
        def acc(index, fstep):
            return int(math.modf(index * fstep)[1])

        #corners
        full_ceiling_mesh[0][0] = [ self.mesh[0][0][PX] + nz_mm[PX], 
                                    self.mesh[0][0][PY] + nz_mm[PY], 
                                    src[0][0][PZ] - nz_mm[PZ] ]
        
       
        full_ceiling_mesh[0][-1] = [ self.mesh[0][-1][PX] - nz_mm[PX],
                                     self.mesh[0][-1][PY] - nz_mm[PY],
                                     src[0][-1][PZ] - nz_mm[PZ] ]
        
        
    
        full_ceiling_mesh[-1][0] = [ self.mesh[-1][0][PX] + nz_mm[PX],
                                     self.mesh[-1][0][PY] - nz_mm[PY],
                                     src[-1][0][PZ] - nz_mm[PZ] ]
        
        
        
        full_ceiling_mesh[-1][-1] = [ self.mesh[-1][-1][PX] - nz_mm[PX],
                                      self.mesh[-1][-1][PY] - nz_mm[PY],
                                      src[-1][-1][PZ] - nz_mm[PZ]]
        
        print(full_ceiling_mesh[0][0],
                        full_ceiling_mesh[0][-1],
                        full_ceiling_mesh[-1][-1],
                        full_ceiling_mesh[-1][0]);
        
       
        if (True):
            for x in range(0, cell_mesh.shape[1]):
                # ternayies to not include the corner data points
                line = src[0, 
                           x * pix_per_cell[1] + acc(x, fstep[1] + (1 if x == 0 else 0)) :
                           (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1 - (1 if x == (cell_mesh_shape[1]-1) else 0 )]                            
                elevations = line[:,2]
                line_min = elevations.argmin()
                # x+1 to skip the cornder
                full_ceiling_mesh[0][x+1] = [ line[line_min][PX],
                                              self.mesh[0][0][PY] + nz_mm[PY],
                                              line[line_min][PZ] - nz_mm[PZ] ]
                                              
                pprint(full_ceiling_mesh[0][x+1])
            
                # ternayies to not include the corner data points
                line = src[-1, 
                           x * pix_per_cell[1] + acc(x, fstep[1] + (1 if x == 0 else 0)) :
                           (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1 - (1 if x == (cell_mesh_shape[1]-1) else 0 )]                            
                elevations = line[:,2]
                line_min = elevations.argmin()
                # x+1 to skip the cornder
                full_ceiling_mesh[-1][x+1] = [ line[line_min][PX],
                                               self.mesh[-1][0][PY] - nz_mm[PY],
                                               line[line_min][PZ] - nz_mm[PZ] ]
        
        
                pprint(full_ceiling_mesh[-1][x+1])
    
    
        if (True):
            for y in range(0, cell_mesh.shape[0]):
                # ternayies to not include the corner data points
                line = src[ y * pix_per_cell[0] + acc(y, fstep[0]) + (1 if y == 0 else 0) :
                            (y+1) * pix_per_cell[0] + acc(y, fstep[0]) - 1 - (1 if y == (cell_mesh_shape[0]-1) else 0),
                            0]
                elevations = line[:,2]
                line_min = elevations.argmin()
                # x+1 to skip the cornder
                full_ceiling_mesh[y+1][0] = [ self.mesh[0][0][PX] + nz_mm[PX],
                                              line[line_min][PY],
                                              line[line_min][PZ] - nz_mm[PZ] ]
                                              
                pprint(full_ceiling_mesh[0][x+1])
            
    
                # ternayies to not include the corner data points
                line = src[ y * pix_per_cell[0] + acc(y, fstep[0]) + (1 if y == 0 else 0) :
                            (y+1) * pix_per_cell[0] + acc(y, fstep[0]) - 1 - (1 if y == (cell_mesh_shape[0]-1) else 0),
                            -1]
                elevations = line[:,2]
                line_min = elevations.argmin()
                # x+1 to skip the cornder
                full_ceiling_mesh[y+1][-1] = [ self.mesh[0][-1][PX] - nz_mm[PX],
                                              line[line_min][PY],
                                              line[line_min][PZ] - nz_mm[PZ] ]    
            
            
                pprint(full_ceiling_mesh[y+1][-1])
        
    
        
       
        
        for y in range(0, cell_mesh.shape[0]):
            for x in range(0, cell_mesh.shape[1]):
                # define the sample area in which to find the min 
                
                # pprint({'y': 
                #     ( y * pix_per_cell[0] + acc(y, fstep[0]) , 
                #             (y+1) * pix_per_cell[0] + acc(y, fstep[1] - 1)),
                #             'x': 
                #             (x * pix_per_cell[1] + acc(x, fstep[1] ), 
                #             (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1)})
                # 
                
                cell = src[ y * pix_per_cell[0] + acc(y, fstep[0]) : 
                            (y+1) * pix_per_cell[0] + acc(y, fstep[1] - 1),
                            x * pix_per_cell[1] + acc(x, fstep[1] ): 
                            (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1]
                elevations = cell[:,:,2]
                cell_min = elevations.argmin()
                # get the x,y,z
                cell_mesh[y][x] = cell.ravel()[3*cell_min:3*cell_min+3] - [0,0,nz_mm[PZ]]
                            
                
        c = Mesh()
        print cell_mesh 
        c.load_matrix(full_ceiling_mesh)
        return c
        
        # top border lows
    
        # per row
            # left border low
            # cell lows
            # right border low
            
        # bottom border lows
        
        # extend borders to edge of neutral zone
        # lower heights of the border a bit to make a moulding
        
    
        
class HorizontalPointPlane(GridShape):
    
    def __init__(self, src_mesh, elevation):
        self.src_mesh = src_mesh
        self.elevation = elevation
        self.xsize = src_mesh.xsize
        self.ysize = src_mesh.ysize
        
    def get(self, x, y):
        orig = self.src_mesh.get(x,y)
        return [orig[PX], orig[PY], self.elevation]        
        
    def x_max(self):
        return self.xsize-1
        
    def y_max(self):
        return self.ysize-1
        
    def triangulate(self, invert_normal = False):
        triangles = []
        for sy in range(0, self.y_max()):
            for sx in range(0, self.x_max()):
                triangles.extend(self.triangulate_square([self.get(sx,sy),
                                     self.get(sx+1, sy),
                                     self.get(sx, sy+1),
                                     self.get(sx+1, sy+1)], 
                                     invert_normal))   
        return triangles
        
class MeshBasePlate(object):
    '''
    A custom set of triangles to draw a bottom plate
    '''
    
    def __init__(self, top, elevation=0):
        self.top = top
        self.xsize = top.xsize
        self.ysize = top.ysize
        self.elevation = elevation
    
    def get(self, x, y):
        orig = self.top.get(x,y)
        return [orig[PX], orig[PY], self.elevation]  
        
    def x_max(self):
        return self.xsize-1
        
    def y_max(self):
        return self.ysize-1        
    
    def triangulate(self):
        triangles = []
        
        def make_pt(x, y, z):
            orig = self.top.get(x,y)
            return (orig[PX],orig[PY],self.elevation)
            
        sample_height = self.top.y_max()+1
        sample_width = self.top.x_max()+1
        
        yhalf = sample_height / 2
        xhalf = sample_width / 2
        yquarter = sample_height / 4
        xquarter = sample_width / 4

        negx = make_pt(xquarter, yhalf, 0)
        posx = make_pt(xquarter + xhalf, yhalf, 0)
        negy = make_pt(xhalf, yquarter, 0)
        posy = make_pt(xhalf, yquarter + yhalf, 0)

        # star inset base
        for sy in range(0, sample_height-1):
            a_triangle = { TA: make_pt(0, sy, 0),
                           TB: negx,
                           TC: make_pt(0, sy+1, 0)}
            z_triangle = { TA: make_pt(sample_width-1, sy, 0),
                          TB: make_pt(sample_width-1, sy+1, 0),
                          TC: posx }

            triangles.append(a_triangle)
            triangles.append(z_triangle)

        for sx in range(0, sample_width-1):
            a_triangle = { TA: make_pt(sx, 0, 0),
                           TB: make_pt(sx+1, 0, 0),
                           TC: negy }
            z_triangle = { TA: make_pt(sx, sample_height-1, 0),
                           TB: posy,
                           TC: make_pt(sx+1, sample_height-1, 0) }

            triangles.append(a_triangle)
            triangles.append(z_triangle)


        a_triangle = { TA: make_pt(0,0,0),
                       TB: negy,
                       TC: negx }
        b_triangle = { TA: negy,
                       TB: make_pt(sample_width-1, 0, 0),
                       TC: posx }
        c_triangle = { TA: posx,
                       TB: make_pt(sample_width-1, sample_height-1, 0),
                       TC: posy }
        d_triangle = { TA: negx,
                       TB: posy,
                       TC: make_pt(0, sample_height-1, 0) }

        e_triangle = { TA: negy,
                       TB: posx,
                       TC: negx }

        f_triangle = { TA: posx,
                       TB: posy,
                       TC: negx }

        triangles.append(a_triangle)
        triangles.append(b_triangle)
        triangles.append(c_triangle)
        triangles.append(d_triangle)
        triangles.append(e_triangle)
        triangles.append(f_triangle)

        return triangles
    
        