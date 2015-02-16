import json
import re
import cherrypy
import shapeways_printer as printer
import math

class ModelPricing(object):
    def __init__(self, config):
        self.config = config
        
    exposed = True
    def GET(self, model_id):
        def topo_pricing(size, sw_pricing):
            markup_table = {50: 5.18, 100:10.36, 200:20.70}
            sw_error_correction = 1.8
            topo_pricing = {}
            for i in sw_pricing:
                print 'PRICED: sw: ', sw_pricing[i], ' errcor: ', sw_error_correction, ' markup: ', markup_table[size]
                topo_pricing[i] = sw_pricing[i] * sw_error_correction + markup_table[size]
                
            return topo_pricing
            
        def approx_price(pricing):
            for i in pricing:
                pricing[i] = math.ceil(pricing[i])
            return pricing
        
        # alphanumeric, _ only
        if re.search("[^\w\-]",model_id):
            raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
       
        model_data = {}
            
        with open("%s/%s.json" % (self.config['model_dir'], model_id)) as mjf:
            model_data = json.load(mjf)
            
        pricing = topo_pricing(model_data['size'], printer.price_model(model_data))
        pricing = approx_price(pricing)

        return json.dumps(pricing)