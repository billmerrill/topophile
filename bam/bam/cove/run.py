from model import SolidElevationModel, HollowTestModel
from pprint import pprint


model_config = { 'src': 'c236gcce2jb0-c236r2812p84.tif',
                 'output_resolution': 50,
                 'output_physical_max': 10,
                 'z_factor': 1.8
                 }


def solid():
    model = SolidElevationModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
def test_hollow():
    model = HollowTestModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
    
# main()      
test_hollow()