import UserDict


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
    
    
    def __init__(self, bbox, size, rez, zmult, hollow, style):
        self.inputs = DotDict({
            'bbox': bbox,
            'size': size,
            'rez': rez,
            'zmult': zmult,
            'hollow': hollow,
            'style': style})
    
        self.outputs = DotDict({
            'model_filename': None,
            'elevation_filename': None,
            'x-size-mm': None,
            'y-size-mm': None,
            'z-size-mm': None,
            'area-mm2':  None,
            'volume-mm3': None})
        
    def get_base_filename(self):
        return '{geohash}-{style}-{size}-{rez}'.format( geohash=self.inputs.bbox.get_geohash(), style=self.inputs.style, size=self.inputs.size, rez=self.inputs.rez)
            
    def get_builder_config(self):
        return { 'src': self.outputs.elevation_filename,
                 'dst': self.outputs.model_filename,
                 'output_resolution': self.inputs.rez,
                 'output_physical_max': self.inputs.size,
                 'z_factor': self.inputs.zmult,
                 'hollow': self.inputs.hollow}

    def set_model_filename(self, name):
        self.outputs.model_filename = name
        
    def set_elevation_filename(self, name):
        self.outputs.elevation_filename = name