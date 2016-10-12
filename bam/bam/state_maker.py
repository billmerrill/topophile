import shapefile

from geo import BoundingBox
import model_ticket
from topoconf import local_app_config as app_config

# Given a state shapefile, get the appropriate elevation DEM

class StateElevationMaker(object):

    def __init__(self, state_shapefile):
        self.state_shapefile = state_shapefile
        self.state_bbox = None
        self.ticket = None
        self.init_state_bbox()
        self._make_ticket()


    def init_state_bbox(self):
        reader = shapefile.Reader(self.state_shapefile)
        if len(reader.shapes()) > 1:
            raise Exception("Too many shapes in shapefile:", len(reader.shapes()))
        state_shp = reader.shape(0)
        bbox = state_shp.bbox
        self.state_bbox = BoundingBox(bbox[3], bbox[0], bbox[1], bbox[2])

    def _scale_state_extent_to_rez(self, rez):
        '''
        '''
        width = abs(self.state_bbox.west - self.state_bbox.east)
        height = abs(self.state_bbox.north - self.state_bbox.south)

        if width > height:
            height = rez * (height / width)
            width = rez
        else:
            width = rez * (width / height)
            height = rez
        return (width, height)



    def _make_ticket(self):
        size = 100
        rez = 200
        zfactor = 5.0
        self.ticket = model_ticket.get_ticket(app_config=app_config,
                               style='state-color',
                               bbox=self.state_bbox,
                               size=size,
                               rez=rez,
                               zmult=zfactor,
                               hollow=True)

        # in the web app, the front end controls the resolution, resolution is
        # specified by the rez param, which is really the number of data points on
        # long side (regardless of the physical size, so not really rez.)
        # anyways, here, take the ratio of the state extent sides and scale
        # them to the rez to control the elevation query size
        (width, height) = self._scale_state_extent_to_rez(rez)
        self.ticket.set_elevation_dimensions(int(round(float(width))),
                                       int(round(float(height))))

    def query_elevation(self):

        self.ticket.data.query_elevation()
