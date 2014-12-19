from mesh import Mesh, HorizontalPointPlane, MeshSandwich, MeshBasePlate
from stl_canvas import STLCanvas
from builder import Builder
from elevation import Elevation
from indicies import *


class Model(object):
    
    def __init__(self, config):
        self.builder = Builder(config)

class SolidElevationModel(Model):
   
    def _raise_the_roof(self, top):
        low_z = top.get_low_z()
        min_thick = self.builder.get_min_thickness()
        if low_z < min_thick[PZ]:
            roof_xform_vector = (0, 0, min_thick[PZ] - low_z)
            print ("Raising the roof %s" % roof_xform_vector[PZ])
            top.transform((1,1,1), roof_xform_vector)
            
    def _compute_model_z_size(self, sandwich):
        top_max_z = sandwich.top.get_high_z()
        return top_max_z - sandwich.bottom.elevation
            
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
       
        print("Top plate physical size: %s x %s " % (top.get_data_x_size(), top.get_data_y_size()))

        bottom = MeshBasePlate(top, 0)
        
        sandwich = MeshSandwich(top, bottom)
        
        canvas = STLCanvas()
        canvas.add_shape(sandwich)
        canvas.write_stl(self.builder.get_output_file_name())
        
        desc = {'filename': self.builder.get_output_file_name(),
                'x-size': top.get_data_x_size(),
                'y-size': top.get_data_y_size(),
                'z-size': self._compute_model_z_size(sandwich) }
                
        elevation.close_dataset()
        
        return desc