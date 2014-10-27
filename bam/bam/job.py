from gbsrc import get_elevation
import cove

class ModelJob(object):
    
    def __init__(self, nwlat, nwlon, selat, selon, rez, size):
        '''
        nwlat - string - northwest corner latitude
        nwlon - string - northwest corner longitude
        selat - string - southeast corner latitude
        selon - string - southeast corner longitude
        rez - number - data resolution of model's long side
        size - number - model physical size, mm
        '''
        self.nwlat = nwlat
        self.nwlon = nwlon
        self.selat = selat
        self.selon = selon
        self.rez = rez
        self.size = size
        
    def run(self):
        elevation_fn = self.get_elevation()
        model_fn = self.build_model(elevation_fn, self.rez, self.size)
        return model_fn
        
    
    def get_elevation(self):
        filename = get_elevation(self.nwlat, self.nwlon, self.selat, self.selon)
        
        
    def build_model(self, elevation_filename, size, rez):
        model_config = { 'src': elevation_filename,
                         'dst': 'test-data/latest-output.stl',
                         'output_resolution': rez,
                         'output_physical_max': size }
        model = cove.model.SolidElevationModel(model_config)
        return model.build_stl()
            
        