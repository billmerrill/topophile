import os
import job
import json
import model_ticket as mt
from geo import BoundingBox


class STLModelService(object):
    exposed = True

    def __init__(self, app_config):
        self.app_config = app_config

    def GET(self, nwlat, nwlon, selat, selon, size, rez, zfactor, model_style, hollow=False, **kwargs):
        '''
        use the bounding box to query for elevation data, and build a model
        return the stl file
        '''
        ticket = mt.get_ticket(app_config=self.app_config,
                               style=model_style,
                               bbox=BoundingBox(float(nwlat), float(nwlon),
                                                float(selat), float(selon)),
                               size=int(size),
                               rez=int(rez),
                               zmult=float(zfactor),
                               hollow=hollow,
                               resample=(not self.app_config['ms_scaling']))
        if 'width' in kwargs and 'height' in kwargs:
            ticket.set_elevation_dimensions(int(round(float(kwargs['width']))),
                                            int(round(float(kwargs['height']))))

        gig = job.BoundingBoxJob(self.app_config, ticket)
        model = gig.run()
        if model is None:
            return "GB Error"

        model['url'] = self.app_config[
            'model_home_url'] + model['model_id'] + ".stl"

        if self.app_config['run_vrml']:
            ticket.inputs.style = 'frosted'
            ticket.data.init_files()
            newgig = job.BoundingBoxJob(self.app_config, ticket)
            newmodel = newgig.run()

        return json.dumps(model)
