from string import Template

import numpy as np

from indicies import *
from mesh_volume import compute_exact_mesh_volume, compute_approx_mesh_volume, compute_elevation_facet_volume
import vrml_templates
from vrml_utils import points_to_text


class FourWallsBase(object):

    '''
    A base piece to connect the walls dropping down
    from the top mesh and the ceiling mesh.

    The primary job of the base is to transition between
    the different point counts between the two
    meshes, keeping the triangles correct
    '''

    def __init__(self, top, ceiling, floor_height):
        '''
        corners are four-tuples, starting nw and going counter-clockwise
        '''
        self.top = top
        self.ceiling = ceiling
        self.outer_corners = []
        self.inner_corners = []
        self.floor_height = floor_height
        self._set_corners()

    def _set_corners(self):
        oc = []
        for c in self.top.get_corners():
            oc.append((c[0], c[1], self.floor_height))
        ic = []
        for c in self.ceiling.get_corners():
            ic.append((c[0], c[1], self.floor_height))

        self.outer_corners = oc
        self.inner_corners = ic

    def triangulate(self):
        '''
        Base normals are pointed negative Z, no need to invert
        '''
        oc = self.outer_corners
        ic = self.inner_corners
        tris = []

        def mkpt(m, x, y):
            og = m.get(x, y)
            return (og[PX], og[PY], self.floor_height)

        # top mesh points
        for p in range(0, self.top.y_max()):
            tris.extend([
                (ic[0],
                 mkpt(self.top, 0, p + 1),
                 mkpt(self.top, 0, p)),

                (ic[2],
                 mkpt(self.top, -1, p),
                 mkpt(self.top, -1, p + 1))])

        for p in range(0, self.top.x_max()):
            tris.extend([
                (ic[1],
                 mkpt(self.top, p + 1, -1),
                 mkpt(self.top, p, -1)),

                (ic[3],
                 mkpt(self.top, p, 0),
                 mkpt(self.top, p + 1, 0))])

        # ceilng mesh points
        for p in range(0, self.ceiling.y_max()):
            tris.extend([
                (oc[1],
                 mkpt(self.ceiling, 0, p),
                 mkpt(self.ceiling, 0, p + 1)),

                (oc[3],
                 mkpt(self.ceiling, -1, p + 1),
                 mkpt(self.ceiling, -1, p))])

        for p in range(0, self.ceiling.x_max()):
            tris.extend([
                (oc[0],
                 mkpt(self.ceiling, p + 1, 0),
                 mkpt(self.ceiling, p, 0)),

                (oc[2],
                 mkpt(self.ceiling, p, -1),
                 mkpt(self.ceiling, p + 1, -1))])

        return tris

    def get_vrml(self):
        '''Draw four trapezoids to cover the base'''

        def get_point_list(pts):
            # handles the Z to Y conversion for vrml
            return "\n".join(" ".join([str(p[PX]), str(self.floor_height), str(-1*p[PY])]) for p in pts)

        coords = [self.outer_corners[0],  # 0
                  self.outer_corners[1],  # 1
                  self.outer_corners[2],  # 2
                  self.outer_corners[3],  # 3
                  self.inner_corners[0],  # 4
                  self.inner_corners[1],  # 5
                  self.inner_corners[2],  # 6
                  self.inner_corners[3]]  # 7

        faces = [
            # west
            0, 1, 5, 4, 0, -1,
            # south
            1, 2, 6, 5, 1, -1,
            # east
            2, 3, 7, 6, 2, -1,
            # north
            3, 0, 4, 7, 3, -1,
        ]
        # [str(x) for x in self.mesh[:, :, PZ].flatten().tolist()]), 80)

        base_shape = Template(vrml_templates.IndexedFaceSet).substitute(
            points=get_point_list(coords),
            coordinates=", ".join([str(x) for x in faces]),
            convex='TRUE')

        return base_shape


class FourWallsCreator(object):

    '''
    Assemble the top and ceiling meshes
    into a hollow model with 4 walls supporting the
    roof
    '''

    def __init__(self, top, ceiling, floor_height):
        self.top = top
        self.ceiling = ceiling
        self.floor_height = floor_height
        self.base = FourWallsBase(self.top,
                                  self.ceiling,
                                  self.floor_height)
        self.top_corners = top.get_corners()
        self.ceiling_corners = ceiling.get_corners()

    def get_z_size(self):
        return self.top.get_high_z() - self.floor_height

    def get_vrml(self):
        top_vrml = self.top.get_vrml()
        base_vrml = self.base.get_vrml()
        ceiling_vrml = self.ceiling.get_irregular_grid_vrml()
        walls_vrml = self.get_walls_vrml()

        return "\n".join([base_vrml, walls_vrml, ceiling_vrml, top_vrml])

    def get_vrml_wall(self, c0, c1, c2, c3, edge):
        '''
            Build a wall that contains a top edge from
            a Mesh, a bottom from Base.  May be the
            interior or exterior of the model.


            c0 /\/\/\/\/\/\/\/\/\/\/\ c3
               |                    |
            c1 +--------------------+ c2

            edge -- an array of points on the edge of a mesh, ordered
                    from c3 to c0, not include c3 or c0
        '''
        coords = [c0, c1, c2, c3]
        coords.extend(edge)  # trim the corner points, reverse the order
        face_indices = [0, 1, 2, 3]
        face_indices.extend(range(4, 2+len(edge)))  # end is4 minus corners

        wall_vrml = Template(vrml_templates.IndexedFaceSet).substitute(
            points=points_to_text(coords),
            coordinates=(", ".join([str(x) for x in face_indices])),
            convex='FALSE')

        return wall_vrml

    def get_wall_helper(self, mesh_edge, mesh_corners, base_corners, left_side, right_side):
        return self.get_vrml_wall(mesh_corners[left_side],
                                  base_corners[left_side],
                                  base_corners[right_side],
                                  mesh_corners[right_side],
                                  mesh_edge)  # trim corners, reverse order

    def get_walls_vrml(self):
        nodes = []

        # outer
        edge = self.top.get_edge("west")[1:-1][::-1]
        nodes.append(self.get_wall_helper(edge, self.top_corners, self.base.outer_corners, 0, 1))

        edge = self.top.get_edge("south")[1:-1][::-1]
        nodes.append(self.get_wall_helper(edge, self.top_corners, self.base.outer_corners, 1, 2))

        edge = self.top.get_edge("east")[1:-1]
        nodes.append(self.get_wall_helper(edge, self.top_corners, self.base.outer_corners, 2, 3))

        edge = self.top.get_edge("north")[1:-1]
        nodes.append(self.get_wall_helper(edge, self.top_corners, self.base.outer_corners, 3, 0))

        # # inner

        edge = self.ceiling.get_edge("west")[1:-1][::-1]
        nodes.append(self.get_wall_helper(edge, self.ceiling_corners, self.base.inner_corners, 0, 1))

        edge = self.ceiling.get_edge("south")[1:-1][::-1]
        nodes.append(self.get_wall_helper(edge, self.ceiling_corners, self.base.inner_corners, 1, 2))

        edge = self.ceiling.get_edge("east")[1:-1]
        nodes.append(self.get_wall_helper(edge, self.ceiling_corners, self.base.inner_corners, 2, 3))

        edge = self.ceiling.get_edge("north")[1:-1]
        nodes.append(self.get_wall_helper(edge, self.ceiling_corners, self.base.inner_corners, 3, 0))

        return "\n".join(nodes)

    def triangulate(self):
        triangles = self.top.triangulate()
        triangles.extend(self.ceiling.triangulate())
        triangles.extend(self.base.triangulate())
        triangles.extend(self.triangulate_walls())
        return triangles

    def triangulate_walls(self):
        triangles = self.triangulate_wallside(self.top, outside_wall=True)
        triangles.extend(
            self.triangulate_wallside(self.ceiling, outside_wall=False))
        return triangles

    def triangulate_wallside(self, top, outside_wall):
        invert = not outside_wall

        def mkpt(m, x, y):
            og = m.get(x, y)
            return (og[PX], og[PY], self.floor_height)

        def quad(square):
            ''' assume points like this for right hand rule
                0  1
                2  3
            '''
            if invert:
                sqtr = []
                # don't produce non-triangles, the inner wall might not be
                # needed
                if square[3][PZ] != square[1][PZ]:
                    sqtr.append([square[0], square[1], square[3]])
                if square[0][PZ] != square[2][PZ]:
                    sqtr.append([square[0], square[3], square[2]])
                return sqtr
            else:
                return [[square[0], square[3], square[1]],
                        [square[0], square[2], square[3]]]

        tris = []
        for p in range(0, top.y_max()):
            tris.extend(quad((
                top.get(0, p),
                top.get(0, p + 1),
                mkpt(top, 0, p),
                mkpt(top, 0, p + 1)
            )))
            tris.extend(quad((
                top.get(-1, p + 1),
                top.get(-1, p),
                mkpt(top, -1, p + 1),
                mkpt(top, -1, p))
            ))

        for p in range(0, top.x_max()):
            tris.extend(quad((
                top.get(p, -1),
                top.get(p + 1, -1),
                mkpt(top, p, -1),
                mkpt(top, p + 1, -1))))

            tris.extend(quad((
                top.get(p + 1, 0),
                top.get(p, 0),
                mkpt(top, p + 1, 0),
                mkpt(top, p, 0))))

        return tris

    def get_volume(self):
        outer_volume = compute_approx_mesh_volume(self.top, self.floor_height)
        inner_volume = compute_exact_mesh_volume(
            self.ceiling, self.floor_height)
        return outer_volume - inner_volume
