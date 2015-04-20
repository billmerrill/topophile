from model import SolidElevationModel, HollowTestModel, HollowElevationModel
from pprint import pprint


model_config = { 'src': 'c236gcce2jb0-c236r2812p84.tif',
                 'output_resolution': 200,
                 'output_physical_max': 100,
                 'z_factor': 1.8,
                 'min_model_thickness': [2,2,2]
                 }

fw_model_config = {
        'dst': '/home/billmerrill/webapps/model_cache/c28gb66h0j84-c294bcjjb021-cube-100-200-1_5.stl',
        'hollow': u'1',
        'output_physical_max': 100,
        'output_resolution': 200,
        'resample_elevation': False,
        'src': '/home/billmerrill/topo-cache/b1/elevation_cache/c28gb66h0j84-c294bcjjb021-100-200.tif',
        'z_factor': 1.5}



def solid():
    model = SolidElevationModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
def hollow():
    model = HollowElevationModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
def test_hollow():
    model = HollowTestModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
def fw_test():
    model = FourWallsModel(fw_model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
    
# main()      
# test_hollow()
# solid()
# hollow()