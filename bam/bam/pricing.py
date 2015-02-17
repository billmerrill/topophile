import json
import re
import cherrypy
import shapeways_printer as printer
import model_pricing as pricer
import math



class ModelPricing(object):
    def __init__(self, config):
        self.config = config
        
    exposed = True
    def GET(self, model_id):
        def topo_pricing(size, sw_pricing):
            sw_error_correction = 1.8
            topo_pricing = {}
            for i in sw_pricing:
                print 'PRICED: sw: ', sw_pricing[i], ' errcor: ', sw_error_correction, ' markup: ', pricer.get_markup_by_size(size) 
                topo_pricing[i] = sw_pricing[i] * sw_error_correction + pricer.get_markup_by_size(size)
                
            return topo_pricing
            
        def approx_price(pricing):
            for i in pricing:
                pricing[i] = math.ceil(pricing[i])
            return pricing
        
        # alphanumeric, _ only
        if re.search("[^\w\-]",model_id):
            raise cherrypy.HTTPError("403 Forbidden", "You are not allowed to access this resource.")
       
        model_data = {}
            
        with open("%s/%s.json" % (self.config['model_dir'], model_id), 'rb') as mjf:
            model_data = json.load(mjf)
            
        pricing = topo_pricing(model_data['size'], printer.price_model(model_data))
        pricing = approx_price(pricing)

        return json.dumps(pricing)