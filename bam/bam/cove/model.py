import json
import os

import numpy as np

from mesh import Mesh, MeshSandwich, MeshBasePlate
from base import FourWallsCreator
from stl_canvas import STLCanvas
from builder import Builder
from elevation import Elevation
from indicies import *
from vrml_canvas import VRMLCanvas

# TODO Organize model more, pull meta work into base class


class Model(object):

    def __init__(self, config):
        self.builder = Builder(config)

    def _get_real_world_specs(self, terrain):
        x_meters = terrain[0][-1][PX] - terrain[0][0][PX]
        y_meters = abs(terrain[-1][0][PY] - terrain[0][0][PY])
        z_low_meters = np.min(terrain[:, :, PZ])
        z_high_meters = np.max(terrain[:, :, PZ])
        return [x_meters, y_meters, z_high_meters - z_low_meters]


class PreviewTerrainModel(Model):

    def build_stl(self):
        elevation = Elevation(self.builder)
        elevation.load_dataset()
        # elevation.display_summary()
        if self.builder.get_resample_elevation():
            elevation_data = elevation.get_meters_ndarray()
        else:
            elevation_data = elevation.get_raw_meters()

        real_world_specs = self._get_real_world_specs(elevation_data)

        top = Mesh()
        top.load_matrix(elevation_data)
        top.finalize_form(self.builder.get_physical_max(),
                          self.builder.get_min_thickness()[PZ],
                          self.builder.get_z_factor())
        top.rest_z_at_zero()

        max_cube = (
            top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        print("Physical Size: %s x %s x %s" % max_cube)

        canvas = STLCanvas()
        canvas.add_shape(top)
        canvas.write_stl(
            self.builder.get_output_file_name(), make_positive=False)

        desc = {'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': top.get_high_z() - top.get_low_z(),
                'area-mm2':  0,  # unneeded
                'volume-mm3': 0,
                'z-exagg': self.builder.get_z_factor()}

        # Scales are not needed foer the preview, don't compute them.k
        desc['x_mm_is_m'] = 1
        desc['y_mm_is_m'] = 1
        desc['z_mm_is_m'] = 1

        elevation.close_dataset()

        return desc


class SolidElevationModel(Model):

    def _compute_model_z_size(self, sandwich):
        top_max_z = sandwich.top.get_high_z()
        return top_max_z - sandwich.bottom.elevation

    def build_stl(self):
        elevation = Elevation(self.builder)
        elevation.load_dataset()
        # elevation.display_summary()
        elevation_data = elevation.get_meters_ndarray()

        real_world_specs = self._get_real_world_specs(elevation_data)

        top = Mesh()
        top.load_matrix(elevation_data)
        top.finalize_form(self.builder.get_physical_max(),
                          self.builder.get_min_thickness()[PZ],
                          self.builder.get_z_factor())

        max_cube = (
            top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        print("Physical Size: %s x %s x %s" % max_cube)

        bottom = MeshBasePlate(top, 0)
        sandwich = MeshSandwich(top, bottom)
        canvas = STLCanvas()
        canvas.add_shape(sandwich)
        model_area = canvas.compute_area()
        model_volume = sandwich.compute_volume()

        canvas.write_stl(self.builder.get_output_file_name())

        desc = {'size': self.builder.get_physical_max(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': self._compute_model_z_size(sandwich),
                'area-mm2':  model_area,
                'volume-mm3': model_volume,
                'z-exagg': self.builder.get_z_factor()}
        desc['x_mm_is_m'] = real_world_specs[PX] / desc['x-size-mm']
        desc['y_mm_is_m'] = real_world_specs[PY] / desc['y-size-mm']
        desc['z_mm_is_m'] = real_world_specs[PZ] / top.get_features_height()

        elevation.close_dataset()

        return desc


class FourWallsModel(Model):

    def _is_buildable(self, top):
        # don't bother making it hollow if the piece is too narrow in a
        # dimension
        x_min_thick = self.builder.get_min_thickness()[1]
        y_min_thick = self.builder.get_min_thickness()[0]
        if ((top.get_data_x_size() <= (3 * x_min_thick)) or
                (top.get_data_y_size() <= (3 * y_min_thick))):
            print "Make Solid: too narrow: %s %s" % (top.get_data_x_size(), top.get_data_y_size())
            return False

        return True

    def build_vrml(self):
        print "STARTING FOUR WALLS VRML MODEL", self.builder
        elevation = Elevation(self.builder)
        elevation.load_dataset()
        # elevation.display_summary()
        elevation_data = elevation.get_meters_ndarray()
        real_world_specs = self._get_real_world_specs(elevation_data)

        top = Mesh()
        top.load_matrix(elevation_data)
        top.finalize_form(self.builder.get_physical_max(),
                          self.builder.get_min_thickness()[PZ],
                          self.builder.get_z_factor())

        cdf = self.builder.get_ceiling_decimation_factor()
        interior_ceiling = top.create_ceiling(
            self.builder.get_min_thickness(), cdf)
        interior_ceiling.transform_border_stepwise(
            (1, 1, 0.7), (0, 0, 0.1), (0, 0, 0), (0, 0, 0), 3)  # bevel the crown
        # XXX what does this mean in vrml
        # interior_ceiling.invert_normals = True  # interior faces point inward

        self.floor_height = 0
        full_model = FourWallsCreator(top, interior_ceiling, self.floor_height)

        canvas = VRMLCanvas()
        canvas.add_element(full_model)

        model_volume = full_model.get_volume()
        # model_area = canvas.compute_area()
        model_area = 999

        print("Starting tapeout")

        output_filename = self.builder.get_output_file_name()
        fn, ext = os.path.splitext(output_filename)
        vrml_name = ".".join([fn, 'wrl'])
        canvas.write_vrml(vrml_name)

        desc = {'size': self.builder.get_physical_max(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': full_model.get_z_size(),
                'area-mm2':  model_area,
                'volume-mm3': model_volume,
                'z-exagg': self.builder.get_z_factor()}
        desc['x_mm_is_m'] = real_world_specs[PX] / desc['x-size-mm']
        desc['y_mm_is_m'] = real_world_specs[PY] / desc['y-size-mm']

        z_scale = 1
        feature_height = top.get_features_height()
        if feature_height > 0:
            z_scale = real_world_specs[PZ] / feature_height
        desc['z_mm_is_m'] = z_scale

        elevation.close_dataset()

        return desc

    def build_stl(self):
        print "STARTING FOUR WALLS MODEL", self.builder
        elevation = Elevation(self.builder)
        elevation.load_dataset()
        # elevation.display_summary()
        elevation_data = elevation.get_meters_ndarray()
        real_world_specs = self._get_real_world_specs(elevation_data)

        top = Mesh()
        top.load_matrix(elevation_data)
        top.finalize_form(self.builder.get_physical_max(),
                          self.builder.get_min_thickness()[PZ],
                          self.builder.get_z_factor())

        if not self._is_buildable(top):
            raise ValueError("Model is too narrow for 4 walls style")

        cdf = self.builder.get_ceiling_decimation_factor()
        interior_ceiling = top.create_ceiling(
            self.builder.get_min_thickness(), cdf)
        interior_ceiling.transform_border_stepwise(
            (1, 1, 0.7), (0, 0, 0.1), (0, 0, 0), (0, 0, 0), 3)  # bevel the crown
        interior_ceiling.invert_normals = True  # interior faces point inward

        self.floor_height = 0
        full_model = FourWallsCreator(top, interior_ceiling, self.floor_height)

        max_cube = (
            top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        # print("Physical Size: %s x %s x %s" % max_cube)

        canvas = STLCanvas()
        canvas.add_shape(full_model)
        model_volume = full_model.get_volume()

        model_area = canvas.compute_area()

        print("Starting tapeout")
        canvas.write_stl(self.builder.get_output_file_name())

        desc = {'size': self.builder.get_physical_max(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': full_model.get_z_size(),
                'area-mm2':  model_area,
                'volume-mm3': model_volume,
                'z-exagg': self.builder.get_z_factor()}
        desc['x_mm_is_m'] = real_world_specs[PX] / desc['x-size-mm']
        desc['y_mm_is_m'] = real_world_specs[PY] / desc['y-size-mm']

        z_scale = 1
        feature_height = top.get_features_height()
        if feature_height > 0:
            z_scale = real_world_specs[PZ] / feature_height
        desc['z_mm_is_m'] = z_scale

        elevation.close_dataset()

        return desc
