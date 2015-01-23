import json
import re
import cherrypy
import shapeways_printer as printer

class ModelPricing(object):
    def __init__(self, config):
        self.config = config
        
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
            
        with open("%s/%s.json" % (self.config['model_dir'], model_id)) as mjf:
            model_data = json.load(mjf)

        if type(mult) is not float:
            mult = float(mult)
        if mult != 1.0:
            model_data = exagerate_model(model_data, mult)

        return json.dumps(printer.price_model(model_data))