import os
import tempfile
import json
import re
import cherrypy
import cove.model
import job
import shapeways_printer as printer


MODEL_DIR = os.path.join(os.getcwd(), "app/model_cache")

class ModelStub(object):
    exposed = True

    def GET(self, *args, **kwargs):
        '''
        use the bounding box to query for elevation data, and build a model
        return the stl file
        '''
        model = {'url': "http://127.0.0.1:9999/3E225D98-E9FE-458F-A1D2-EFD54FCBAF26.stl",
                 'x-size': 100.0,
                 'y-size': 75.0,
                 'z-size': 90.0}
        return json.dumps(model)
        
class ModelPricing(object):
    exposed = True
    def GET(self, model_id):
        # alphanumeric, _ only
        if re.search("[^\w\-]",model_id):
            raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
        
        mjf = open ("%s/%s.json" % (MODEL_DIR, model_id))
        model_data = json.load(mjf)
        mjf.close()
        

        return json.dumps(printer.price_model(model_data))
    

class STLModelService(object):
    exposed = True
    def __init__(self):
        self.test = ModelStub()
        self.price = ModelPricing()
   
    def GET(self, nwlat, nwlon, selat, selon, size, rez, zfactor, hollow=False, model_style="cube"):
        '''
        use the bounding box to query for elevation data, and build a model
        return the stl file
        '''
        gig = job.BoundingBoxJob(nwlat, nwlon, selat, selon, size, rez, zfactor, hollow, model_style)
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
        
def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'


if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    conf = {
        '/': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.sessions.on': True,
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'application/json')],
         'tools.CORS.on': True
        }
    }
    cherrypy.quickstart(STLModelService(), '/', conf)