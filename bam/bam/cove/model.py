import json
from mesh import Mesh, HorizontalPointPlane, MeshSandwich, MeshBasePlate, HollowBottomDiamondWalls
from stl_canvas import STLCanvas
from builder import Builder
from elevation import Elevation
from indicies import *
import numpy as np

#TODO Organize model more, pull meta work into base class
class Model(object):
    def __init__(self, config):
        self.builder = Builder(config)
        
    def _get_real_world_specs(self, terrain):
        x_meters = terrain[0][-1][PX] - terrain[0][0][PX]
        y_meters = abs(terrain[-1][0][PY] - terrain[0][0][PY])
        z_low_meters = np.min(terrain[:,:,PZ])
        z_high_meters = np.max(terrain[:,:,PZ])
        return [x_meters, y_meters, z_high_meters - z_low_meters]
    

class PreviewTerrainModel(Model):
    def _write_model_metadata(self, m):
        data_filename = m['filename'].replace('stl', 'json')
        jf = open(data_filename, 'wb')
        json.dump(m,jf)
        jf.close()
            
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
      
        max_cube = (top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        print("Physical Size: %s x %s x %s" % max_cube)

        canvas = STLCanvas()
        canvas.add_shape(top)
        canvas.write_stl(self.builder.get_output_file_name(), make_positive=False)
        
        model_area = canvas.compute_area()
        model_volume = 0
       
        desc = {'filename': self.builder.get_output_file_name(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': top.get_high_z() - top.get_low_z(),
                'area-mm2':  model_area,
                'volume-mm3': model_volume}
        desc['x-mm-is-m'] = real_world_specs[PX] / desc['x-size-mm']
        desc['y-mm-is-m'] = real_world_specs[PY] / desc['y-size-mm']
        desc['z-mm-is-m'] = real_world_specs[PZ] / top.get_features_height()

        
        self._write_model_metadata(desc)
                
        elevation.close_dataset()
        
        return desc



class SolidElevationModel(Model):
   
    def _compute_model_z_size(self, sandwich):
        top_max_z = sandwich.top.get_high_z()
        return top_max_z - sandwich.bottom.elevation
    
    def _write_model_metadata(self, m):
        data_filename = m['filename'].replace('stl', 'json')
        jf = open(data_filename, 'wb')
        json.dump(m,jf)
        jf.close()
            
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
      
        max_cube = (top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        print("Physical Size: %s x %s x %s" % max_cube)

        bottom = MeshBasePlate(top, 0)
        sandwich = MeshSandwich(top, bottom)
        canvas = STLCanvas()
        canvas.add_shape(sandwich)
        model_area = canvas.compute_area()
        model_volume = sandwich.compute_volume()
        
        canvas.write_stl(self.builder.get_output_file_name())
        
        desc = {'filename': self.builder.get_output_file_name(),
                'size': self.builder.get_physical_max(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': self._compute_model_z_size(sandwich), 
                'area-mm2':  model_area,
                'volume-mm3': model_volume}
        desc['x-mm-is-m'] = real_world_specs[PX] / desc['x-size-mm']
        desc['y-mm-is-m'] = real_world_specs[PY] / desc['y-size-mm']
        desc['z-mm-is-m'] = real_world_specs[PZ] / top.get_features_height()
        
        self._write_model_metadata(desc)
                
        elevation.close_dataset()
        
        return desc

class HollowElevationModel(Model):
   
    def _compute_model_z_size(self, sandwich):
        top_max_z = sandwich.top.get_high_z()
        return top_max_z - sandwich.bottom.elevation
    
    def _write_model_metadata(self, m):
        data_filename = m['filename'].replace('stl', 'json')
        jf = open(data_filename, 'wb')
        json.dump(m,jf)
        jf.close()

    def _compute_volume(self, outer, inner=None):
        volume = outer.compute_approx_volume('avg')
        if inner:
            volume = volume - inner.compute_volume()
            
        return volume
        
    def _compute_exact_volume(self, outer, inner=None):
        volume = outer.compute_volume()
        if inner:
            volume = volume - inner.compute_volume()
            
        return volume
        
    def build_stl(self):
        print "STARTING HOLLOW MODEL", self.builder
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
        make_hollow = True                    

        # 3mm gap for material flow, + the floor thickness required for hollow model
        if top.get_low_z() < (3 + self.builder.get_min_thickness()[PZ]):
            print "Make Solid: too low: %s" % top.get_low_z()
            make_hollow = False
           
        # don't bother making it hollow if the piece is too narrow in a dimension
        x_min_thick = self.builder.get_min_thickness()[1]
        y_min_thick = self.builder.get_min_thickness()[0]
        if ((top.get_data_x_size() <= (3 * x_min_thick)) or \
           (top.get_data_y_size() <= (3 * y_min_thick))):
            print "Make Solid: too narrow: %s %s" % (top.get_data_x_size(), top.get_data_y_size())
            make_hollow = False;
                            
        bottom = MeshBasePlate(top, 0, make_hollow)
        sandwich = MeshSandwich(top, bottom)
        
        if make_hollow:
            cdf = self.builder.get_ceiling_decimation_factor()
            interior_ceiling = top.create_ceiling(
                self.builder.get_min_thickness(), cdf)
            interior_ceiling.transform_border_stepwise((1,1,0.7), (0,0,0.1), (0,0,0), (0,0,0), 3) # bevel the crown 
            interior_ceiling.invert_normals = True  # interior faces point inward
            
            diamond = bottom.get_relief_diamond()
            interior_floor = MeshBasePlate(interior_ceiling, self.builder.get_min_thickness()[PZ], hollow=True, invert_normals=True)
            interior_floor.set_relief_diamond(diamond)
            diamond_walls = HollowBottomDiamondWalls(interior_floor, bottom)
          
            inner_sandwich = MeshSandwich(interior_ceiling, interior_floor, invert_normals=True)
            
        max_cube = (top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        # print("Physical Size: %s x %s x %s" % max_cube)
        
        canvas = STLCanvas()
        canvas.add_shape(sandwich)
        model_volume = 0
        if make_hollow:
            print "Made Hollow"
            canvas.add_shape(inner_sandwich)
            canvas.add_shape(diamond_walls)
            model_volume = self._compute_volume(sandwich,inner_sandwich)
        else:
            print "Made Solid"
            model_volume = self._compute_volume(sandwich)
        
        model_area = canvas.compute_area()
        
        print("Starting tapeout")
        canvas.write_stl(self.builder.get_output_file_name())
        # 
        desc = {'filename': self.builder.get_output_file_name(),
                'size': self.builder.get_physical_max(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': self._compute_model_z_size(sandwich),
                'area-mm2':  model_area,
                'volume-mm3': model_volume}
        desc['x-mm-is-m'] = real_world_specs[PX] / desc['x-size-mm']
        desc['y-mm-is-m'] = real_world_specs[PY] / desc['y-size-mm']
        desc['z-mm-is-m'] = real_world_specs[PZ] / top.get_features_height()
        self._write_model_metadata(desc)
        
        elevation.close_dataset()
        
        return desc
        
        
class HollowTestModel(Model):
   
    def _compute_model_z_size(self, sandwich):
        top_max_z = sandwich.top.get_high_z()
        return top_max_z - sandwich.bottom.elevation
    
    def _write_model_metadata(self, m):
        data_filename = m['filename'].replace('stl', 'json')
        jf = open(data_filename, 'wb')
        json.dump(m,jf)
        jf.close()
            
    def build_stl(self):
        elevation = Elevation(self.builder)
        elevation.load_dataset()
        # elevation.display_summary()
        elevation_data = elevation.get_meters_ndarray()
        
        top = Mesh()
        top.load_matrix(elevation_data) 
        top.finalize_form(self.builder.get_physical_max(), 
                            self.builder.get_min_thickness()[PZ],
                            self.builder.get_z_factor())
                            
                            
        hollow_ceiling = top.create_ceiling(
            self.builder.get_min_thickness(), 
            self.builder.get_ceiling_decimation_factor())
      
        max_cube = (top.get_data_x_size(), top.get_data_y_size(), top.get_high_z())
        print("Physical Size: %s x %s x %s" % max_cube)
        
        
        

        bottom = MeshBasePlate(top, 0, True)
        diamond = bottom.get_relief_diamond()
        hollow_bottom = MeshBasePlate(hollow_ceiling, self.builder.get_min_thickness()[PZ], True)
        hollow_bottom.set_relief_diamond(diamond)
        
        diamond_walls = HollowBottomDiamondWalls(hollow_bottom, bottom)
       
        sandwich = MeshSandwich(top, bottom)
        inner_sandwich = MeshSandwich(hollow_ceiling, hollow_bottom)
        canvas = STLCanvas()
        canvas.add_shape(inner_sandwich)
        canvas.add_shape(sandwich)
        canvas.add_shape(diamond_walls)
        
        # model_area = canvas.compute_area()
        # model_volume = sandwich.compute_volume()
        # 
        canvas.write_stl(self.builder.get_output_file_name())
        # 
        desc = {'filename': self.builder.get_output_file_name(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size()}
        #         'z-size-mm': self._compute_model_z_size(sandwich), 
        #         'area-mm2':  model_area,
        #         'volume-mm3': model_volume}
        # 
        # self._write_model_metadata(desc)
                
        elevation.close_dataset()
        
        return desc