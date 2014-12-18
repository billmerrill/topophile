from model import SolidElevationModel


model_config = { 'src': 'c236gcce2jb0-c236r2812p84.tif',
                 'output_resolution': 50,
                 'output_physical_max': 100,
                 'z_factor': 1.5
                 }

def main():
    model = SolidElevationModel(model_config)
    model.build_stl()
    
main()      