import random
import time
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
        
    def new_upoader(model=model)
        id = str(random.getrandbits(8))
        self.clients[id] =  Client(
            consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
            consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
            callback_url = "http://localhost:9090:/upload?id=%smodel=%s" % (id,model))
            
    def _new_client(self):
        id = str(random.getrandbits(8))
        self.clients[id] =  Client(
            consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
            consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff")
        return id
    
    def delete(id):
        del(self.clients[id])
            
    
class ShapewaysService(object):
    def __init__(self):
        self.clients = ClientStore()
        self.lookup = TemplateLookup(directories=['html'])
  
    def build_model_message(self, model):
        m = {'filename': 'Your New Model %s' % int(time.time()),
            'hasrightsToModel': 1,
            'acceptTermsAndConditions': 1,
            'isPrivate': 1,
            'isForSale': 1,
            'materials': {
                    "6": 
                        { "id": 6,
                			'type': 'object',
                			'description': 'material object',
                			'properties': {
                				'markup': {
            					'type': 'float',
            					'description': 123.45},
            				'isActive': {
            					'type': 'boolean',
            					'description': 1 }
                			}
                        }}}
                        
        with open(model_file, 'rb' as f):
            p['file'] = base64.b64encode(f.read())
   
    
    def render(self, template, params = {}):
        tmpl = self.lookup.get_template(template)
        return tmpl.render(**params)
        
        
    @cherrypy.expose    
    def index(self):
        return self.render("index.html")
      
    @cherrypy.expose
    def start(self,  model):
        id, client = self.clients.new_uploader(model=model)
        params = {'auth_url' : client.connect()}
        return self.render("start.html", params)
        
    def upload(self, id, model):
        client = self.clients.get(id)
        client.add_model(self.build_model_message(model))
        
        
            
    @cherrypy.expose    
    def connect(self, model):
        auth_url = client.connect
        return lookup.get_template("connect.html").render()

if __name__ == '__main__':
    conf = {
        '/': {
         'tools.sessions.on': True,
        }
    }
    cherrypy.config.update("server.conf")
    cherrypy.quickstart(ShapewaysService(), '/', conf)