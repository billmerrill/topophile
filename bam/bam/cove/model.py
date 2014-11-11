from mesh import Mesh, HorizontalPointPlane, MeshSandwich, MeshBasePlate
from stl_canvas import STLCanvas
from builder import Builder
from elevation import Elevation


class Model(object):
    
    def __init__(self, config):
        self.builder = Builder(config)

class SolidElevationModel(Model):
    
    def build_stl(self):
        
        elevation = Elevation(self.builder)
        elevation.load_dataset()
        elevation.display_summary()
        print ("loading elevation")
        elevation_data = elevation.get_meters_matrix()
        print ("Elevation is %s x %s" % (len(elevation_data), len(elevation_data[0])))
        
        print ("starting mesh")
        
        top = Mesh()
        top.load_matrix(elevation_data) 
        top.transform((1,1,self.builder.get_z_factor()), (0,0,0))
        top.scale_to_output_size(self.builder.get_physical_max())
        
        print("Top plate physical size: %s x %s " % (top.get_data_x_size(), top.get_data_y_size()))

        print ("starting bottom")
        bottom = MeshBasePlate(top, 0)
        
        sammy = MeshSandwich(top, bottom)
        
        canvas = STLCanvas()
        print ("building sandwich")
        canvas.add_shape(sammy)
        print("writing stl")
        canvas.write_stl(self.builder.get_output_file_name())
        
        elevation.close_dataset()
        return(self.builder.get_output_file_name())