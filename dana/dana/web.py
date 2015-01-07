import base64
import datetime
import json
import os
import random
import cherrypy
from shapeways.client import Client
from mako.template import Template
from mako.lookup import TemplateLookup

MODEL_DIR = "/Users/bill/topo/bam/bam/app/model_cache"



class ClientStore(object):
    
    def __init__(self):
        random.seed()
        self.clients = {}
        
    def get(self, id=None):
        if not id in self.clients:
            id = self._new_client()
            
        return (id, self.clients[id])
        
    def new_uploader(self, model):
        id = str(random.getrandbits(8))
        self.clients[id] =  Client(
            consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
            consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
            callback_url = "http://localhost:9090/upload?id=%s&model=%s" % (id,model))
        return (id, self.clients[id])
            
    def _new_client(self):
        id = str(random.getrandbits(8))
        self.clients[id] =  Client(
            consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
            consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff")
        return id
    
    def delete(id):
        del(self.clients[id])

def new_shapeways_client():
    return Client(
        consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
        consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
        oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
        oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
    )
        
                
    
class ShapewaysService(object):
    def __init__(self):
        self.clients = ClientStore()
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
   
    
    def render(self, template, params = {}):
        tmpl = self.lookup.get_template(template)
        return tmpl.render(**params)
        
        
    @cherrypy.expose    
    def index(self):
        return self.render("noop.html")
      
    @cherrypy.expose    
    def test(self):
        return self.render("index.html")
        
    @cherrypy.expose    
    def upload_to_store(self, model):
        client = new_shapeways_client()
        response = client.add_model(self.build_model_message(model))
        return self.render("buy.html", {'modelUrl': response['urls']['privateProductUrl']['address'],
                                        'modelId': response['modelId']})
       
    @cherrypy.expose    
    def is_printable(self, id):
        client = new_shapeways_client()
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
       

if __name__ == '__main__':
    conf = {
        '/': {
         'tools.sessions.on': True,
         },
         '/static': {
         'tools.staticdir.on' : True,
         'tools.staticdir.dir' : "/Users/bill/topo/dana/dana/static"
        }
    }
    cherrypy.config.update("server.conf")
    cherrypy.quickstart(ShapewaysService(), '/', conf)