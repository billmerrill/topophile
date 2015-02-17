import base64
import datetime
import json
import os
import cherrypy
import shapeways_printer as printer
import model_metadata as modelmd
import model_pricing
from mako.template import Template
from mako.lookup import TemplateLookup

class ShapewaysService(object):
    def __init__(self, config):
        self.lookup = TemplateLookup(directories=['html'])
        self.config = config

    def render(self, template, params = {}):
        tmpl = self.lookup.get_template(template)
        return tmpl.render(**params)
  
    def build_model_message(self, model, include_file = True):
        dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        m = {'fileName': 'Your New Model %s.stl' % dt_str,
            'description': 'Created on %s' % dt_str,
            'hasRightsToModel': 1,
            'acceptTermsAndConditions': 1,
            'isPrivate': 1,
            'isForSale': 1,
            'materials': {'6': {'isActive': 1, 'markup': 900.09, 'materialId': '6'}}}
                       
        if include_file: 
            model_file = os.path.join(self.config['model_dir'], model)
            with open(model_file, 'rb') as f:
                m['file'] = base64.b64encode(f.read())
            
        return m
        
    def set_price(self, swid, tpid, swdata):
        success = True
        model_data = modelmd.get_model_metadata(self.config['model_dir'], tpid)
        if not model_data:
            return False
    
        sw_markup = swdata['materials']['6']['markup']
        tp_markup = model_pricing.get_markup_by_size(model_data['size'])
        if sw_markup != tp_markup:
            msg = self.build_model_message(tpid, include_file=False)
            msg['materials']['6']['markup'] = tp_markup
            
            client = printer.new_shapeways_client()
            response = client.update_model_info(swid, msg)
       
        return success
    
    @cherrypy.expose
    def upload(self, model_id):
        model = model_id + ".stl"
        client = printer.new_shapeways_client()
        response = client.add_model(self.build_model_message(model))
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(response)
      
    @cherrypy.expose    
    def upload_to_store(self, model):
        client = printer.new_shapeways_client()
        response = client.add_model(self.build_model_message(model))
        return self.render("buy.html", {'modelUrl': response['urls']['privateProductUrl']['address'],
                                        'modelId': response['modelId']})
       
    @cherrypy.expose    
    def is_printable(self, swid, tpid):
        response = {'url': '', 'ready': False}
        client = printer.new_shapeways_client()
        model = client.get_model_info(int(swid))
        if 'materials' not in model or '6' not in model['materials']:
            response['errmsg'] = "Materials missing from response"
            return json.dumps(response)
            
        printable = model['materials']['6']['isPrintable'] == 1
        active = model['materials']['6']['isActive'] == 1
        response = {'url': model['urls']['privateProductUrl']['address']}
        response['ready'] = printable and active
        if response['ready']:
            print "UPDATING PRICE"
            response['ready'] = response['ready'] and self.set_price(swid, tpid, model)
        
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
        