import UserDict
import os


BBOX = 'cube'

def get_ticket(**kwargs):
    return BBoxModelTicket(**kwargs)

class DotDict(object):
    def __init__(self, d={}):
        self.d = d
    def __getattr__(self, key):
        return self.d[key]
    def __setattr(self, key, value):
        self.d[key] = value

    
class BBoxModelTicket(object):
    '''
    inputs:
        bbox: a BoundingBox of the geographic extents of this model
        size: the size, in mm, of the longest side of the model (x or y, z not included atm)
        rez: the number of data points along the longest side (same as above)
        zmult: elevation exageration multiplier
        hollow: should the model be hollow
        
    outputs:
    '''
    
    
    def __init__(self, bbox, size, rez, zmult, hollow, style, resample):
        self.inputs = DotDict({
            'bbox': bbox,
            'size': size,
            'rez': rez,
            'zmult': zmult,
            'hollow': hollow,
            'style': style,
            'resample_elevation': resample})
    
        self.outputs = DotDict({
            'model_filename': None,
            'elevation_filename': None,
            'x-size-mm': None,
            'y-size-mm': None,
            'z-size-mm': None,
            'area-mm2':  None,
            'volume-mm3': None})
        
    def get_elevation_name(self):
        return '{geohash}-{size}-{rez}'.format( geohash=self.inputs.bbox.get_geohash(), style=self.inputs.style, size=self.inputs.size, rez=self.inputs.rez)
        
    def get_model_name(self):
        zstr = str(self.inputs.zmult).replace(".", "_")
        return '{geohash}-{style}-{size}-{rez}-{zmult}'.format( geohash=self.inputs.bbox.get_geohash(), style=self.inputs.style, size=self.inputs.size, rez=self.inputs.rez, zmult=zstr  )
            
    def get_builder_config(self):
        return { 'src': self.get_elevation_filepath(),
                 'dst': self.get_model_filepath(),
                 'output_resolution': self.inputs.rez,
                 'output_physical_max': self.inputs.size,
                 'z_factor': self.inputs.zmult,
                 'hollow': self.inputs.hollow,
                 'resample_elevation': self.inputs.resample_elevation}

    def get_model_filepath(self):
        return self.outputs.model_filename
        
    def get_model_metadata_filepath(self):
        return self.outputs.model_metadata
        
    def get_elevation_filepath(self):
        return self.outputs.elevation_filename
    
    def set_model_filepaths(self, dst_dir, model_ext):
        self.outputs.model_filename = os.path.join(dst_dir, self.get_model_name() + model_ext)
        self.outputs.model_metadata = os.path.join(dst_dir, self.get_model_name() + ".json")
        
    def set_elevation_filepath(self, dst_dir, ele_ext):
        self.outputs.elevation_filename = os.path.join(dst_dir, self.get_elevation_name() + ele_ext)
    
    def get_hollow(self):
        return self.inputs.hollow
        
    def set_elevation_dimensions(self, width, height):
        self.inputs.elevation_width = width;
        self.inputs.elevation_height = height;
        
    def get_elevation_dimensions(self):
        return {'x': self.inputs.elevation_width,
                'y': self.inputs.elevation_height}
    
    def get_bbox(self):
        return self.inputs.bbox
        
    def get_app_query_string(self):
        return "?b=%s" % self.inputs.bbox.get_geohash()