# import gb_src as el_src
import sample_src as el_src
import cove
import os

class BoundingBoxJob(object):
    
    def __init__(self, nwlat, nwlon, selat, selon, size, rez, zfactor):
        '''
        nwlat - string - northwest corner latitude
        nwlon - string - northwest corner longitude
        selat - string - southeast corner latitude
        selon - string - southeast corner longitude
        size - number - model physical size, mm
        rez - number - data resolution of model's long side
        zfactor - elevation multiplier
        '''
        self.nwlat = nwlat
        self.nwlon = nwlon
        self.selat = selat
        self.selon = selon
        self.rez = int(rez)
        self.size = int(size)
        self.zfactor = float(zfactor)
        
    def run(self):
        elevation_data = el_src.get_elevation(self.nwlat, self.nwlon, self.selat, self.selon)
        if elevation_data is None:
            return None
            
        model_filename = self.build_model(elevation_data['filename'])
        return model_filename 
        
    def build_model(self, elevation_filename):
        dst_filename = os.path.split(elevation_filename)[1].replace('tif', 'stl')
        dst_filename = os.path.join(os.getcwd(), "app/model_cache", dst_filename) 
        model_config = { 'src': elevation_filename,
                         'dst': dst_filename,
                         'output_resolution': self.rez,
                         'output_physical_max': self.size,
                         'z_factor': self.zfactor}
        model = cove.model.SolidElevationModel(model_config)
        return model.build_stl()
            
class GeoTiffJob(object):
    
    def __init__(self, geo_src, size, rez):
        self.geo_src = geo_src
        self.size = size
        self.rez = rez
    
    def run(self):
        dst_filename = os.path.split(self.geo_src)[1] + ".stl"
        dst_filename = os.path.join(os.getcwd(), "app/model_cache", dst_filename)
        model_config = { 'src': self.geo_src,
                         'dst': dst_filename,
                         'output_resolution': self.rez,
                         'output_physical_max': self.size }
        model = cove.model.SolidElevationModel(model_config)
        return model.build_stl()