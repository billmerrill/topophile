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

    def _make_ticket(self):
        size = 200
        rez = 100
        zfactor = 5.0
        self.ticket = model_ticket.get_ticket(app_config=app_config,
                               style='state-color',
                               bbox=self.state_bbox,
                               size=size,
                               rez=rez,
                               zmult=zfactor,
                               hollow=True)

        # XXX TODO figure out sizing, this is not the way to do it
        width = abs(self.state_bbox.west - self.state_bbox.east) * 100
        height = abs(self.state_bbox.north - self.state_bbox.south) * 100
        self.ticket.set_elevation_dimensions(int(round(float(width))),
                                       int(round(float(height))))

    def query_elevation(self):

        self.ticket.data.query_elevation()
