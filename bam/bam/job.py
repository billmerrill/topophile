import elevation.cay_src as el_src
import cove
import os
import time
import cherrypy
import json
import model_metadata as model_md


class BoundingBoxJob(object):

    def __init__(self, app_config, ticket):
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
        self.app_config = app_config
        self.ticket = ticket

    def run(self):
        t1 = time.time()

        self.ticket.set_elevation_filepath(
            self.app_config['elevation_dir'], ".tif")

        if not os.path.exists(self.ticket.get_elevation_filepath()):
            bbox = self.ticket.inputs.bbox

            if self.app_config['ms_scaling']:
                elevation_data = el_src.get_scaled_elevation(self.app_config,
                                                             self.ticket.get_elevation_filepath(),
                                                             bbox.north, bbox.west, bbox.south, bbox.east,
                                                             self.ticket.get_elevation_dimensions())
            else:
                elevation_data = el_src.get_elevation(self.app_config, self.ticket.get_elevation_filepath(
                ), bbox.north, bbox.west, bbox.south, bbox.east)

            if elevation_data is None:
                return None
        else:
            cherrypy.log("Elevation Cached!")

        t2 = time.time()

        # self.ticket.set_elevation_filename(elevation_data['filename'])

        model_data = self.build_model()
        model_data['model_id'] = self.ticket.get_model_name()
        model_data['topo_url'] = 'http://' + \
            self.app_config['app_url'] + self.ticket.get_app_query_string()
        model_md.write_model_metadata(
            self.ticket.get_model_metadata_filepath(), model_data)

        t3 = time.time()
        # cherrypy.log("-Job: %s %s,%s-%s,%s" % (self.ticket.inputs.style, self.inputs.nwlat, self.nwlon, self.selat, self.selon))
        cherrypy.log("-Elevation Data:\t%s" % (t2 - t1))
        cherrypy.log("-Model Build:\t%s" % (t3 - t2))
        return model_data

    def pick_model(self, model_config):
        model = None
        if self.ticket.inputs.style == "preview":
            model = cove.model.PreviewTerrainModel(model_config)
        else:
            model = cove.model.FourWallsModel(model_config)

        return model

    def build_model(self):
        self.ticket.set_model_filepaths(self.app_config['model_dir'], ".stl")

        model_config = self.ticket.get_builder_config()
        if not os.path.exists(self.ticket.get_model_filepath()) or \
           not os.path.exists(self.ticket.get_model_metadata_filepath()):

            model = self.pick_model(model_config)

            try:
                model_data = model.build_stl()
            except Exception:
                cherrypy.log("ALERT: Hollow Build failed, reverting to Solid")
                cherrypy.log(str(model_config))
                model = cove.model.SolidElevationModel(model_config)
                model_data = model.build_stl()

            bbox = self.ticket.get_bbox()
            model_data['nlat'] = bbox.north
            model_data['slat'] = bbox.south
            model_data['elon'] = bbox.east
            model_data['wlon'] = bbox.west
            model_data['size'] = self.ticket.get_size()

            if self.app_config['run_vrml']:
                if isinstance(model, cove.model.FourWallsModel):
                    model.build_vrml()

        else:
            cherrypy.log("Model Cached!")
            with open(self.ticket.get_model_metadata_filepath()) as mjf:
                model_data = json.load(mjf)

        # we could update the ticket with the model_data

        return model_data
