import math
from indicies import * 
import numpy as np
from numpy.linalg import norm
import copy
from pprint import pprint
from mesh_volume import compute_elevation_facet_volume, compute_approx_square_vol, \
    compute_approx_square_min_vol, compute_approx_square_max_vol

class CanvasShape(object):
    
    def get_triangles(self):
        pass 

class GridShape(object):
    
    def triangulate_square(self, square, invert_normals = False):
        ''' assume points like this for right hand rule
            0  1
            2  3
        '''
        if invert_normals:
            return [[square[0], square[1], square[3]],
                   [square[0], square[3], square[2]]]
        else:
            return [[square[0], square[3], square[1]],
                   [square[0], square[2], square[3]]]   
                   
                   
class MeshSandwich(GridShape):
    def __init__(self, top, bottom, invert_normals=False):
        if not (top.xsize == bottom.xsize and top.ysize == bottom.ysize):
            print ("CANT MAKE SAMMICHES")
            return
        self.xsize = top.xsize
        self.ysize = top.ysize
        self.top = top
        self.bottom = bottom
        self.invert_normals = invert_normals
        
    def triangulate(self):
        triangles = self.top.triangulate(invert_normals = self.invert_normals)
        triangles.extend(self.bottom.triangulate(invert_normals = self.invert_normals))
        triangles.extend(self.triangulate_sides())    
        return triangles
    
    def triangulate_sides(self):
        triangles = []
        for sy in range(0, self.top.y_max()):
            triangles.extend(self.triangulate_square([self.top.get(0,sy),
                             self.top.get(0,sy+1),
                             self.bottom.get(0,sy),
                             self.bottom.get(0,sy+1)],
                             self.invert_normals))
            triangles.extend(self.triangulate_square([self.top.get(self.top.x_max(), sy+1),
                             self.top.get(self.top.x_max(), sy),
                             self.bottom.get(self.bottom.x_max(), sy+1),
                             self.bottom.get(self.bottom.x_max(), sy)],
                             self.invert_normals))
            
                            
        for sx in range(0, self.top.x_max()):
            triangles.extend(self.triangulate_square([self.top.get(sx+1,0),
                             self.top.get(sx,0),
                             self.bottom.get(sx+1,0),
                             self.bottom.get(sx,0)],
                             self.invert_normals))
            triangles.extend(self.triangulate_square([self.top.get(sx, self.top.y_max()),
                             self.top.get(sx+1, self.top.y_max()),
                             self.bottom.get(sx, self.bottom.y_max()),
                             self.bottom.get(sx+1, self.bottom.y_max())],
                             self.invert_normals))
                             
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
        
    def compute_approx_volume(self, val='avg'):
        '''
        NOTE: This methods only work for gridded trianlges.  They won't work 
            for the freely decimated interiors
        '''
        volume = 0.0
        meth = None
        if val == 'avg':
            meth = compute_approx_square_vol
        elif val == 'min':
            meth = compute_approx_square_min_vol
        else:
            meth = compute_approx_square_max_vol
        for sy in range(0, self.top.y_max()):
            for sx in range(0, self.top.x_max()):
                volume += meth([self.top.get(sx, sy),
                     self.top.get(sx+1, sy),
                     self.top.get(sx, sy+1),
                     self.top.get(sx+1, sy+1)], self.bottom.elevation)
        return volume


class Mesh(GridShape):
    
    def __init__(self, xsize=0, ysize=0, invert=False):
        self.xsize = xsize 
        self.ysize = ysize
        self.mesh = []
        self.invert_normals = invert
            
    def triangulate(self, invert_normals = False):
        triangles = []
        invert = invert_normals or self.invert_normals
        for sy in range(0, self.y_max()):
            for sx in range(0, self.x_max()):
                triangles.extend(self.triangulate_square([self.get(sx,sy),
                                     self.get(sx+1, sy),
                                     self.get(sx, sy+1),
                                     self.get(sx+1, sy+1)], 
                                     invert_normals=invert))        
                                 
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
        
    def get_corners(self):
        '''
        starting at nw and going around counter-clockwise
        '''
        return [self.mesh[0,0],
                self.mesh[-1,0],
                self.mesh[-1,-1],
                self.mesh[0,-1]]
        
    def get_low_z(self):
        return np.min(self.mesh[:,:,PZ])

    def get_high_z(self):
        return np.max(self.mesh[:,:,PZ])
        
    def get_features_height(self):
        return self.get_high_z() - self.get_low_z()
    
    def rest_z_at_zero(self):
        self.mesh = np.subtract(self.mesh, [0,0,self.get_low_z()])
    
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
        
    def finalize_form(self, max_output_size, min_elevation, z_factor):
        largest_data_dim = max(self.get_data_x_size(), self.get_data_y_size())     
        ratio = max_output_size / largest_data_dim
        # self.transform([output_ratio, output_ratio, output_ratio])
        self.mesh = np.multiply([ratio, ratio, ratio * z_factor], self.mesh)
        
        translate_v  = [0,0,0]
        low_z = self.get_low_z()
        if low_z < min_elevation:
            self.mesh = self.mesh + [0,0, min_elevation - low_z]
            
    def create_ceiling(self, nz_mm, dezfactor):
        '''
        nz_mm: the size, in mm, of the walls of the hollowed model
        ceil_size: the resolution of the ceiling mesh
        '''
        dezfactor = np.array(dezfactor)

        nz_mm = np.array(nz_mm)
        pix_mm = [ abs(self.mesh[0][1][PX] - self.mesh[0][0][PX]),
                   abs(self.mesh[0][0][PY] - self.mesh[1][0][PY])]     
                   
        # number of pixels to skip on the borders     
        nz_pix = np.ceil(nz_mm[0:2] / pix_mm)
        for a in [0,1]:
            if nz_pix[a] == 0:
                nx_pix[a] = 1
       
        # window on mesh data to be decimated, doesn't include the data "in the walls"
        src = self.mesh[nz_pix[0]:-nz_pix[0], nz_pix[1]:-nz_pix[1] ]
        
        srcshape = np.array((src.shape[0], src.shape[1]))
        # the basic shape of the ceiling mesh
        d_mesh_size = np.divide(srcshape, dezfactor) 
        
        
        # increase the size out the output to include a ring of edge pixels
        full_ceiling_mesh = np.ndarray((d_mesh_size[0]+2, d_mesh_size[1]+2, 3))
        cell_mesh = full_ceiling_mesh[1:-1,1:-1]
        
        # filter view of the output, address values to be filled by scanning an area
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
                                    self.mesh[0][0][PY] - nz_mm[PY], 
                                    src[0][0][PZ] - nz_mm[PZ] ]
        
       
        full_ceiling_mesh[0][-1] = [ self.mesh[0][-1][PX] - nz_mm[PX],
                                     self.mesh[0][-1][PY] - nz_mm[PY],
                                     src[0][-1][PZ] - nz_mm[PZ] ]
        
        
    
        full_ceiling_mesh[-1][0] = [ self.mesh[-1][0][PX] + nz_mm[PX],
                                     self.mesh[-1][0][PY] + nz_mm[PY],
                                     src[-1][0][PZ] - nz_mm[PZ] ]
        
        
        
        full_ceiling_mesh[-1][-1] = [ self.mesh[-1][-1][PX] - nz_mm[PX],
                                      self.mesh[-1][-1][PY] + nz_mm[PY],
                                      src[-1][-1][PZ] - nz_mm[PZ]]
        

        # top and bottom edges stretched ot exact dimensions
       
        # print cell_mesh
        if (True):
            for x in range(0, cell_mesh.shape[1]):
                # ternaries to not include the corner data points
                # the line includes all the pixels along y=0 and x from the begning to the end of a cell
                line = src[0, 
                           x * pix_per_cell[1] + acc(x, fstep[1] + (1 if x == 0 else 0)) :
                           (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1 - (1 if x == (cell_mesh_shape[1]-1) else 0 )]                            
                elevations = line[:,2]
                line_min = elevations.argmin()
                # x+1 to skip the cornder
                full_ceiling_mesh[0][x+1] = [ line[line_min][PX],
                                              self.mesh[0][0][PY] - nz_mm[PY],
                                              line[line_min][PZ] - nz_mm[PZ] ]
                                              
            
                # ternaries to not include the corner data points
                line = src[-1, 
                           x * pix_per_cell[1] + acc(x, fstep[1] + (1 if x == 0 else 0)) :
                           (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1 - (1 if x == (cell_mesh_shape[1]-1) else 0 )]                            
                elevations = line[:,2]
                line_min = elevations.argmin()
                # x+1 to skip the cornder
                full_ceiling_mesh[-1][x+1] = [ line[line_min][PX],
                                               self.mesh[-1][0][PY] + nz_mm[PY],
                                               line[line_min][PZ] - nz_mm[PZ] ]
        
        
    
        # left and right edges stretched ot exact dimensions
    
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
            
            
        
    
        
       
        # cell samples
        for y in range(0, cell_mesh.shape[0]):
            for x in range(0, cell_mesh.shape[1]):
                # define the sample area in which to find the min 
                
                
                cell = src[ y * pix_per_cell[0] + acc(y, fstep[0]) + (1 if y == 0 else 0) : 
                            (y+1) * pix_per_cell[0] + acc(y, fstep[0]) - 1 - (1 if y == cell_mesh_shape[0]-1 else 0),
                            x * pix_per_cell[1] + acc(x, fstep[1]) + (1 if x == 0 else 0): 
                            (x+1) * pix_per_cell[1] + acc(x, fstep[1]) - 1 - (1 if x == cell_mesh_shape[1]-1 else 0)]
                elevations = cell[:,:,2]
                cell_min = elevations.argmin()
                # get the x,y,z
                cell_mesh[y][x] = cell.ravel()[3*cell_min:3*cell_min+3] - [0,0,nz_mm[PZ]]
                            
                
        c = Mesh()
        # print cell_mesh 
        c.load_matrix(full_ceiling_mesh)
        return c
        
    def transform_border_points(self, scale, translate):
        #x    
        self.mesh[0,:] = np.multiply(self.mesh[0,:], np.array(scale))
        self.mesh[0,:] = np.add(self.mesh[0,:], np.array(translate))
        self.mesh[-1,:] = np.multiply(self.mesh[-1,:], np.array(scale))
        self.mesh[-1,:] = np.add(self.mesh[-1,:], np.array(translate))
        
        #y
        self.mesh[1:-1,0] = np.multiply(self.mesh[1:-1,0], np.array(scale))
        self.mesh[1:-1,0] = np.add(self.mesh[1:-1,0], np.array(translate))
        self.mesh[1:-1,-1] = np.multiply(self.mesh[1:-1,-1], np.array(scale))
        self.mesh[1:-1,-1] = np.add(self.mesh[1:-1,-1], np.array(translate))
        
    def transform_border(self, scale, translate, depth=1):
        #x    
        self.mesh[0:depth,:] = np.multiply(self.mesh[0:depth,:], np.array(scale))
        self.mesh[0:depth,:] = np.add(self.mesh[0:depth,:], np.array(translate))
        self.mesh[-depth:,:] = np.multiply(self.mesh[-depth:,:], np.array(scale))
        self.mesh[-depth:,:] = np.add(self.mesh[-depth:,:], np.array(translate))
        
        #y
        self.mesh[depth:-depth,0:depth] = np.multiply(self.mesh[depth:-depth,0:depth], np.array(scale))
        self.mesh[depth:-depth,0:depth] = np.add(self.mesh[depth:-depth,0:depth], np.array(translate))
        self.mesh[depth:-depth,-depth:] = np.multiply(self.mesh[depth:-depth,-depth:], np.array(scale))
        self.mesh[depth:-depth,-depth:] = np.add(self.mesh[depth:-depth,-depth:],np.array(translate))
        
    def transform_border_stepwise(self, scale_start, scale_step, translate_start, translate_step, depth=1):
        scale_start = np.array(scale_start)
        scale_step = np.array(scale_step)
        translate_start = np.array(translate_start)
        translate_step = np.array(translate_step)
        #x    

        def transform_edge(ystart, ystop, xstart, xstop):
            yslice = slice(ystart, ystop if ystop != 0 else None)
            xslice = slice(xstart, xstop if xstop != 0 else None)
            self.mesh[yslice,xslice] = np.multiply(self.mesh[yslice, xslice], np.add(scale_start, d*scale_step))
            self.mesh[yslice,xslice] = np.add(self.mesh[yslice,xslice], np.add(translate_start, d*translate_step))
            
        for d in range(depth):
            #x
            transform_edge(d,     d+1, d, -d)
            transform_edge(-d-1, -d,   d, -d)
            #y
            transform_edge(d+1, -d-1,  d,    d+1)
            transform_edge(d+1, -d-1, -d-1, -d)
        
        
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


class HollowBottomDiamondWalls(GridShape):
    
    def __init__(self, inner_bottom, outer_bottom):
        self.inner = inner_bottom
        self.outer = outer_bottom
        
    def triangulate(self):
        triangles = []
        
        inn = self.inner.get_relief_diamond()
        out = self.outer.get_relief_diamond()
        squares = [ [out[0], out[3], inn[0], inn[3] ],
                    [out[1], out[2], inn[1], inn[2] ],
                    [out[2], out[0], inn[2], inn[0] ],
                    [out[3], out[1], inn[3], inn[1] ]]
        for x in squares:
            triangles.extend(self.triangulate_square(x))
            
        return triangles
        
        
        
class MeshBasePlate(object):
    '''
    A custom set of triangles to draw a bottom plate
    '''
    
    def __init__(self, top, elevation=0, hollow=False, invert_normals=False):
        self.top = top
        self.xsize = top.xsize
        self.ysize = top.ysize
        self.elevation = elevation
        self.hollow = hollow 
        self.config_geometry()
        self.set_relief_diamond()
        self.invert_normals = invert_normals
        
    
    def get(self, x, y):
        orig = self.top.get(x,y)
        return [orig[PX], orig[PY], self.elevation]  
        
    def x_max(self):
        return self.xsize-1
        
    def y_max(self):
        return self.ysize-1        
        
    def make_pt(self, x, y, z):
        orig = self.top.get(x,y)
        return (orig[PX],orig[PY],self.elevation)
        
    def config_geometry(self):
        self.plate_y = self.top.y_max()+1
        self.plate_x = self.top.x_max()+1
        
    def set_relief_diamond(self, override_diamond=[]):
        if override_diamond:
            od = []
            for pt in override_diamond:
                od.append((pt[PX], pt[PY], self.elevation))
            self.negx, self.posx, self.negy, self.posy = od
        else :
            yhalf = self.plate_y / 2
            xhalf = self.plate_x / 2
            yquarter = self.plate_y / 4
            xquarter = self.plate_x / 4

            self.negx = self.make_pt(xquarter, yhalf, 0)
            self.posx = self.make_pt(xquarter + xhalf, yhalf, 0)
            self.negy = self.make_pt(xhalf, yquarter, 0)
            self.posy = self.make_pt(xhalf, yquarter + yhalf, 0)
            
    def get_relief_diamond(self):
        return [self.negx, self.posx, self.negy, self.posy]
        
    def triangulate(self, invert_normals=False):
        triangles = []
        
            
        sample_height = self.plate_y
        sample_width = self.plate_x
        
        negx, posx, negy, posy = self.get_relief_diamond()

        # star inset base
        for sy in range(0, sample_height-1):
            a_triangle = [  self.make_pt(0, sy, 0),
                            negx,
                            self.make_pt(0, sy+1, 0)]
            z_triangle = [  self.make_pt(sample_width-1, sy, 0),
                           self.make_pt(sample_width-1, sy+1, 0),
                           posx ]

            triangles.append(a_triangle)
            triangles.append(z_triangle)

        for sx in range(0, sample_width-1):
            a_triangle = [  self.make_pt(sx, 0, 0),
                            self.make_pt(sx+1, 0, 0),
                            negy ]
            z_triangle = [  self.make_pt(sx, sample_height-1, 0),
                            posy,
                            self.make_pt(sx+1, sample_height-1, 0) ]

            triangles.append(a_triangle)
            triangles.append(z_triangle)


        a_triangle = [  self.make_pt(0,0,0),
                        negy,
                        negx ]
        b_triangle = [  negy,
                        self.make_pt(sample_width-1, 0, 0),
                        posx ]
        c_triangle = [  posx,
                        self.make_pt(sample_width-1, sample_height-1, 0),
                        posy ]
        d_triangle = [  negx,
                        posy,
                        self.make_pt(0, sample_height-1, 0) ]

        triangles.append(a_triangle)
        triangles.append(b_triangle)
        triangles.append(c_triangle)
        triangles.append(d_triangle)
        
        if not self.hollow:
            e_triangle = [  negy,
                            posx,
                            negx ]

            f_triangle = [  posx,
                            posy,
                            negx ]

            triangles.append(e_triangle)
            triangles.append(f_triangle)
            
        if self.invert_normals or invert_normals:
            new_tris = []
            for t in triangles:
                new_tris.append( [t[TA], t[TC], t[TB]])
            triangles = new_tris
            
        return triangles
    
    