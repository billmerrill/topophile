import base64
import datetime
import os
import tempfile
import json
import re
import cherrypy
import cove.model
import job
import shapeways_printer as printer
from mako.template import Template
from mako.lookup import TemplateLookup


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
    def GET(self, model_id, mult=1.0):
        def exagerate_model(model, mult):
            res = model
            res['x-size-mm'] = model['x-size-mm'] * mult
            res['y-size-mm'] = model['y-size-mm'] * mult
            res['z-size-mm'] = model['z-size-mm'] * mult
            res['area-mm2'] = model['area-mm2'] * mult * mult
            res['volume-mm3'] = model['volume-mm3'] * mult * mult * mult
            return res
        
        # alphanumeric, _ only
        if re.search("[^\w\-]",model_id):
            raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
       
        model_data = {}
            
        with open("%s/%s.json" % (MODEL_DIR, model_id)) as mjf:
            model_data = json.load(mjf)

        if type(mult) is not float:
            mult = float(mult)
        if mult != 1.0:
            model_data = exagerate_model(model_data, mult)

        return json.dumps(printer.price_model(model_data))
        
    
class TestyClass(object):
    exposed = True
    @cherrypy.expose
    def index(self):
        return "I went to stock market today. I did a business."

class STLModelService(object):
    exposed = True
   
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

class ShapewaysService(object):
    def __init__(self):
        self.lookup = TemplateLookup(directories=['html'])
  
    def build_model_message(self, model):
        m = {'fileName': 'Your New Model %s.stl' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'hasRightsToModel': 1,
            'acceptTermsAndConditions': 1,
            'isPrivate': 1,
            'isForSale': 1,
            'materials': {'6': {'isActive': 1, 'markup': 900.09, 'materialId': '6'}}}
                        
        model_file = os.path.join(MODEL_DIR, model)
        with open(model_file, 'rb') as f:
            m['file'] = base64.b64encode(f.read())
            
        return m
      
    @cherrypy.expose    
    def upload_to_store(self, model):
        client = printer.new_shapeways_client()
        response = client.add_model(self.build_model_message(model))
        return self.render("buy.html", {'modelUrl': response['urls']['privateProductUrl']['address'],
                                        'modelId': response['modelId']})
       
    @cherrypy.expose    
    def is_printable(self, id):
        client = printer.new_shapeways_client()
        model = client.get_model_info(int(id))
        printable = model['materials']['6']['isPrintable'] == 1
        active = model['materials']['6']['isActive'] == 1
        response = {'url': model['urls']['privateProductUrl']['address']}
        response['ready'] = printable and active
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(response)
        
    @cherrypy.expose    
    def fake_buy(self ):
        p = {'modelUrl': 'http://foo.bar/model.com', 'modelId': '3009591'}
        return self.render("buy.html",p)
    
    @cherrypy.expose    
    def fake_ready(self ):
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps({'url': 'http://fakecom/model/dot/click/click',
                            'ready': True})
        
class RootClass(object):
    exposed = True
    def __init__(self):
        self.build = STLModelService()
        self.price = ModelPricing()
        self.vincent = TestyClass()
        self.printer = ShapewaysService()
        
def CORS():
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'


if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    conf = {
        '/': {
         'tools.sessions.on': True,
         'tools.CORS.on': True
        },
        '/build': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/price': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/static': {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : "/Users/bill/topo/bam/bam/static"
        }
    }
    cherrypy.quickstart(RootClass(), '/', conf)