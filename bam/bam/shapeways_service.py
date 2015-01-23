import base64
import datetime
import json
import os
import cherrypy
import shapeways_printer as printer
from mako.template import Template
from mako.lookup import TemplateLookup

class ShapewaysService(object):
    def __init__(self, config):
        self.lookup = TemplateLookup(directories=['html'])
        self.config = config

    def render(self, template, params = {}):
        tmpl = self.lookup.get_template(template)
        return tmpl.render(**params)
  
    def build_model_message(self, model):
        m = {'fileName': 'Your New Model %s.stl' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'hasRightsToModel': 1,
            'acceptTermsAndConditions': 1,
            'isPrivate': 1,
            'isForSale': 1,
            'materials': {'6': {'isActive': 1, 'markup': 900.09, 'materialId': '6'}}}
                        
        model_file = os.path.join(self.config['model_dir'], model)
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
        