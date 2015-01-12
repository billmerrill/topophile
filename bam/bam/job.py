import cay_src as el_src
#import sample_src as el_src
import cove
import os
import time



class BoundingBoxJob(object):
    
    def __init__(self, nwlat, nwlon, selat, selon, size, rez, zfactor, hollow, model_style):
        '''
        nwlat - string - northwest corner latitude
        nwlon - string - northwest corner longitude
        selat - string - southeast corner latitude
        selon - string - southeast corner longitude
        size - number - model physical size, mm
        rez - number - data resolution of model's long side
        zfactor - elevation multiplier
        hollow - boolean
        '''
        self.nwlat = nwlat
        self.nwlon = nwlon
        self.selat = selat
        self.selon = selon
        self.rez = int(rez)
        self.size = int(size)
        self.zfactor = float(zfactor)
        self.hollow = hollow is not False
        self.model_style = model_style
        
    def run(self):
        t1 = time.time()
        elevation_data = el_src.get_elevation(self.nwlat, self.nwlon, self.selat, self.selon)
        if elevation_data is None:
            return None
        t2 = time.time()
            
        model_filename = self.build_model(elevation_data['filename'])
        
        t3 = time.time()
        print "-----Job Times------"
        print "-Elevation Data:\t", t2-t1
        print "-Model Build:\t", t3-t2
        return model_filename 
        
    def build_model(self, elevation_filename):
        dst_filename = os.path.split(elevation_filename)[1].replace('tif', 'stl')
        dst_filename = os.path.join(os.getcwd(), "app/model_cache", dst_filename) 
        model_config = { 'src': elevation_filename,
                         'dst': dst_filename,
                         'output_resolution': self.rez,
                         'output_physical_max': self.size,
                         'z_factor': self.zfactor,
                         'hollow': self.hollow}
                        
        if self.model_style == "preview":
            model = cove.model.PreviewTerrainModel(model_config)
        else:
            if self.hollow:
                model = cove.model.HollowElevationModel(model_config)
            else:
                model = cove.model.SolidElevationModel(model_config)
                
        model_data = model.build_stl()
        return model_data
        
        
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