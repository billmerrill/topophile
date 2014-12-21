from model import SolidElevationModel
from pprint import pprint


model_config = { 'src': 'c236gcce2jb0-c236r2812p84.tif',
                 'output_resolution': 50,
                 'output_physical_max': 100,
                 'z_factor': 1.8
                 }

def main():
    model = SolidElevationModel(model_config)
    model_data = model.build_stl()
    pprint(model_data)
    
    
main()      