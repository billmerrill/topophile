import os
import job
import json
import model_ticket as mt
from geo import BoundingBox

class STLModelService(object):
    exposed = True
    def __init__(self, app_config):
        self.app_config = app_config
   
    def GET(self, nwlat, nwlon, selat, selon, size, rez, zfactor, hollow=False, model_style="cube"):
        '''
        use the bounding box to query for elevation data, and build a model
        return the stl file
        '''
        ticket = mt.get_ticket(style=model_style, bbox = BoundingBox(nwlat, nwlon, selat, selon), size=int(size), rez=int(rez), zmult=float(zfactor), hollow=hollow)
        gig = job.BoundingBoxJob(self.app_config, ticket)
        model = gig.run()
        if model is None:
            return "GB Error"
        model['url'] = "http://127.0.0.1:9999/" + os.path.split(model['filename'])[1]
        model['model_id'] = os.path.splitext(os.path.split(model['filename'])[1])[0]
        del(model['filename'])
        return json.dumps(model)
        
    def POST(self, elevation, size=200, rez=50):
        '''
        accept an uploaded geotiff, return an stl model
        '''
        elevation_data = tempfile.NamedTemporaryFile(delete=False)
        try:
            while True:
                data = elevation.file.read(1024)
                if not data:
                    break
                elevation_data.write(data)
                
            elevation_data.seek(0)
            elevation_data.flush()
            
            gig = job.GeoTiffJob(elevation_data.name, size, rez)
            model_fn = gig.run()
        finally:
            elevation_data.close()
            
        return model_fn