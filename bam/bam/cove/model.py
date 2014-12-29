import json
from mesh import Mesh, HorizontalPointPlane, MeshSandwich, MeshBasePlate, HollowBottomDiamondWalls
from stl_canvas import STLCanvas
from builder import Builder
from elevation import Elevation
from indicies import *


class Model(object):
    
    def __init__(self, config):
        self.builder = Builder(config)

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
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': self._compute_model_z_size(sandwich), 
                'area-mm2':  model_area,
                'volume-mm3': model_volume}
        
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

    def _compute_volume(outer, inner):
        ''' this ignores the volume lost to the relief diamond '''
        return outer.compute_volume - inner.compute_volume
            
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
        
        model_area = canvas.compute_area()
        model_volume = self._compute_volume(sandwich,inner_sandwich)
        # 
        canvas.write_stl(self.builder.get_output_file_name())
        # 
        desc = {'filename': self.builder.get_output_file_name(),
                'x-size-mm': top.get_data_x_size(),
                'y-size-mm': top.get_data_y_size(),
                'z-size-mm': self._compute_model_z_size(sandwich),
                'area-mm2':  model_area,
                'volume-mm3': model_volume}
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