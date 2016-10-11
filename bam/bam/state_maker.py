import shapefile

from geo import BoundingBox
from topoconfig import local_app_config as app_config

# Given a state shapefile, get the appropriate elevation DEM

class StateElevationMaker(object):

    def __init__(self, state_shapefile):
        self.state_shapefile = state_shapefile
        self.state_bbox = None
        self.ticket = None
        self.init_state_bbox()
        self._make_ticket


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
        ticket = mt.get_ticket(app_config=self.app_config,
                               style=model_style,
                               bbox=self.state_bbox,
                               size=size,
                               rez=rez,
                               zmult=zfactor,
                               hollow=hollow)

    def query_bbox_elevation(self):

        pass
