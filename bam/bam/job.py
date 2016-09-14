import copy
import json
import os
import time

import cherrypy

import elevation.cay_src as el_src
import cove
import model_metadata as model_md


class BoundingBoxJob(object):

    def __init__(self, app_config, ticket):
        '''
        app_config: the topoconf dict
        ticket: general specifications for the requested model
        '''
        self.app_config = app_config
        self.ticket = ticket

    def run(self):
        print 'starting'
        # elevation_data = self._query_elevation_data()
        # image_data = self._query_image_data()
        model_data = self.build_model()

        model_data['model_id'] = self.ticket.get_model_name()
        model_data['topo_url'] = 'http://' +  self.app_config['app_url'] + self.ticket.get_app_query_string()
        model_md.write_model_metadata(self.ticket.get_model_metadata_filepath(), model_data)

        return model_data

    def pick_model(self, model_config):
        model = None
        if self.ticket.inputs.style == "preview":
            model = cove.model.PreviewTerrainModel(model_config)
        else:
            model = cove.model.FourWallsModel(model_config)

        return model

    def build_model(self):
        # self.ticket.set_model_filepaths(self.app_config['model_dir'])

        model_config = self.ticket.get_builder_config()
        if not os.path.exists(self.ticket.get_model_filepath()) or \
           not os.path.exists(self.ticket.get_model_metadata_filepath()):

            self.ticket.data.query_data()
            model = self.pick_model(model_config)

            # try:
            model_data = model.build(self.ticket.get_style())
            # model_data = model.build('plain')
            # except Exception:
            #     cherrypy.log("ALERT: Hollow Build failed, reverting to Solid")
            #     cherrypy.log(str(model_config))
            #     model = cove.model.SolidElevationModel(model_config)
            #     model_data = model.build(self.ticket.get_style())
            #
            bbox = self.ticket.get_bbox()
            model_data['nlat'] = bbox.north
            model_data['slat'] = bbox.south
            model_data['elon'] = bbox.east
            model_data['wlon'] = bbox.west
            model_data['size'] = self.ticket.get_size()

        else:
            cherrypy.log("Model Cached!")
            with open(self.ticket.get_model_metadata_filepath()) as mjf:
                model_data = json.load(mjf)

        # we could update the ticket with the model_data

        return model_data
