import base64
import json
import os
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
            
    
class ShapewaysService(object):
    def __init__(self):
        self.clients = ClientStore()
        self.lookup = TemplateLookup(directories=['html'])
  
    def build_model_message(self, model):
        m = {'fileName': 'Your New Model %s.stl' % int(time.time()),
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
        return self.render("index.html")
      
    @cherrypy.expose
    def start(self,  model):
        id, client = self.clients.new_uploader(model=model)
        params = {'auth_url' : client.connect()}
        return self.render("start.html", params)
        
    #http://localhost:9090:/upload?id=107model=xn69kk97zuxg-xn69jb1jbn2h.stl?&oauth_token=e246c8a38b100a5e07ec91d7a4f7eb22b0a737be&oauth_verifier=ad4e54
    @cherrypy.expose
    def upload(self, id, model,**kwargs):
        # shapeways throwin in a ?
        if model[-1] == '?':
            model = model[:-1]
        id, client = self.clients.get(id)
        client.verify(kwargs['oauth_token'], kwargs['oauth_verifier'])
        response = client.add_model(self.build_model_message(model))
        cherrypy.response.headers['Content-Type']= 'application/json'
        return json.dumps(response)
        
        
            
    @cherrypy.expose    
    def connect(self, model):
        auth_url = client.connect
        return lookup.get_template("connect.html").render()
        
    @cherrypy.expose    
    def upload_to_store(self, model):
        client = Client(
            consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
            consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
            oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
            oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
            callback_url="http://localhost:3000/callback"
        )
        
        response = client.add_model(self.build_model_message(model))
        return self.render("buy.html", {'url': response['urls']['privateProductUrl']['address']})
       

if __name__ == '__main__':
    conf = {
        '/': {
         'tools.sessions.on': True,
        }
    }
    cherrypy.config.update("server.conf")
    cherrypy.quickstart(ShapewaysService(), '/', conf)