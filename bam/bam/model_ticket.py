import UserDict
import os
from basethirtysix import to_base36

import cherrypy

import elevation.cay_src as el_src
import geo


def get_ticket(**kwargs):
    return BBoxModelTicket(**kwargs)


class DotDict(object):
    def __init__(self, d={}):
        self.d = d

    def __getattr__(self, key):
        return self.d[key]

    def __setattr(self, key, value):
        self.d[key] = value

class ModelDataManager(object):

    def __init__(self, app_config, ticket):
        self.app_config = app_config
        self.ticket = ticket
        self.elevation_dir = app_config['elevation_dir']
        self.model_dir = app_config['model_dir']

        self.elevation_filename = ''
        self.image_filename = ''
        self.model_filename = ''
        self.metadata_filename = ''

        self.elevation_data = None
        self.image_data = None
        self.model_data = None

    def init_files(self, flavor=None):
        if not flavor:
            flavor = self.ticket.get_style()

        uniq = self.ticket.get_model_name()
        self.elevation_filename = os.path.join(self.elevation_dir, uniq + '.tif')

        self.metadata_filename = os.path.join(self.model_dir, uniq + ".json")

        if flavor == 'preview' or flavor == 'plain':
            self.model_filename = os.path.join(self.model_dir, uniq + '.stl')
        elif flavor == 'frosted' or flavor == 'state-color':
            try:
                os.mkdir(os.path.join(self.model_dir, uniq))
            except OSError:
                pass
            self.image_filename = os.path.join(self.model_dir, uniq, 'terrain.png')
            self.model_filename = os.path.join(self.model_dir, uniq, 'model.wrl')
        else:
            cherrypy.log("This is not flavor country, setup error.")

    def query_data(self, flavor=None):
        if not flavor:
            flavor = self.ticket.get_style()

        self.query_elevation()
        if flavor == 'frosted':
            self.query_image()

    def query_elevation(self):
        elevation_data = {}
        if not os.path.exists(self.elevation_filename) or self.app_config['disable_elevation_cache']:
            bbox = self.ticket.inputs.bbox
            elevation_data = el_src.get_scaled_elevation(self.app_config,
                                                         self.elevation_filename,
                                                         bbox.north, bbox.west, bbox.south, bbox.east,
                                                         self.ticket.get_elevation_dimensions())
        else:
            cherrypy.log("Elevation Cached!")
        self.elevation_data = elevation_data

    def query_statemaker_elevation(self):
        elevation_data = {}
        if not os.path.exists(self.elevation_filename) or self.app_config['disable_elevation_cache']:
            bbox = self.ticket.inputs.bbox
            print 'ticket statemaker bbox', bbox, bbox.north
            elevation_data = el_src.get_scaled_elevation(self.app_config,
                                                         self.elevation_filename,
                                                         bbox.north, bbox.west, bbox.south, bbox.east,
                                                         self.ticket.get_elevation_dimensions(),
                                                         proj='3857')
        else:
            cherrypy.log("Elevation Cached!")
        self.elevation_data = elevation_data

    def query_image(self):
        image_data = {}
        bbox = self.ticket.inputs.bbox
        image_data = el_src.get_bluemarble(self.app_config,
                                           self.image_filename,
                                           bbox.north, bbox.west, bbox.south, bbox.east,
                                           self.ticket.get_elevation_dimensions())
        self.image_data = image_data




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

    def __init__(self, app_config, bbox, size, rez, zmult, hollow, style):
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

        self.data = ModelDataManager(app_config, self)
        self.data.init_files()


    def get_style(self):
        return self.inputs.style

    def get_elevation_name(self):
        return '{geohash}-{size}-{rez}'.format( geohash=self.inputs.bbox.get_geohash(), style=self.inputs.style, size=self.inputs.size, rez=self.inputs.rez)

    def get_model_name(self):
        zstr = str(self.inputs.zmult).replace(".", "_")
        return '{geohash}-{style}-{size}-{rez}-{zmult}'.format( geohash=self.inputs.bbox.get_geohash(), style=self.inputs.style, size=self.inputs.size, rez=self.inputs.rez, zmult=zstr  )

    def get_builder_config(self):
        return {'src': self.get_elevation_filepath(),
                'dst': self.get_model_filepath(),
                'output_resolution': self.inputs.rez,
                'output_physical_max': self.inputs.size,
                'z_factor': self.inputs.zmult,
                'hollow': self.inputs.hollow}

    def get_model_filepath(self):
        return self.data.model_filename

    def get_model_metadata_filepath(self):
        return self.data.metadata_filename

    def get_elevation_filepath(self):
        return self.data.elevation_filename

    def get_image_filepath(self):
        return self.data.image_filename

    def get_hollow(self):
        return self.inputs.hollow

    def set_elevation_dimensions(self, width, height):
        self.inputs.elevation_width = width
        self.inputs.elevation_height = height

    def get_elevation_dimensions(self):
        return {'x': self.inputs.elevation_width,
                'y': self.inputs.elevation_height}

    def get_bbox(self):
        return self.inputs.bbox

    def get_app_query_string(self):
        return "?b=%s&e=%s" % (self.inputs.bbox.get_geohash(), to_base36(int(self.inputs.zmult * 10)))

    def get_size(self):
        return self.inputs.size
