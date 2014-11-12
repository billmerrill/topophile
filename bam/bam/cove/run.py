from model import SolidElevationModel


model_config = { 'src': '539445F7-171F-49C0-96C4-99826E684551.tif',
                 'output_resolution': 50,
                 'output_physical_max': 200,
                 'z_factor': 20
                 }

def main():
    model = SolidElevationModel(model_config)
    model.build_stl()
    
main()      