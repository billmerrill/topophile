import base64
import datetime
import json
import os
import traceback
import cherrypy
import shapeways_printer as printer
import model_metadata as modelmd
import model_pricing
import model_serial
from mako.template import Template
from mako.lookup import TemplateLookup

class ShapewaysService(object):
    def __init__(self, config):
        self.lookup = TemplateLookup(directories=['html'])
        self.config = config


    def render(self, template, params = {}):
        tmpl = self.lookup.get_template(template)
        return tmpl.render(**params)


    def _format_scale(self, meters_per_mm):
        # per cm
        value = meters_per_mm * 10.0 
        unit = 'm'
        if value > 1500:
            unit = 'km'
            value = value / 1000.0
           
        value = round(value, 3)
        return "1 cm = %s %s" % (value, unit)
            
 
    def _build_description(self, model_data):
        center_lat = (model_data.get('nlat', 0) + model_data.get('slat', 0)) / 2.0
        center_lon = (model_data.get('elon', 0) + model_data.get('wlon', 0)) / 2.0
        
        desc_values = {
        'serial_number': model_data.get('sn', "42"),
        'born_on': datetime.datetime.now().strftime("%d %B %Y"),
        'topo_url': model_data.get('topo_url', 'http://topophile.com'),
        'latitude': round(center_lat, 4),
        'longitude': round(center_lon, 4),
        'exag': model_data.get('z-exagg', "1"),
        'h_scale': self._format_scale(model_data.get('x_mm_is_m', "unknown")),
        'v_scale': self._format_scale(model_data.get('z_mm_is_m', "unknown"))}
        
        return '''
<h3>Topophile Model #%(serial_number)s</h3>
Created on %(born_on)s<br>
<a href="%(topo_url)s">%(topo_url)s</a><br>
<br>
<table style="width: 30em;">
<tbody>
<tr style="border-bottom: 1px dashed #ccc; margin-bottom: .5em;">
    <td>Geographic Center</td>
    <td>%(latitude)s N, %(longitude)s E</td>
</tr>
<tr style="border-bottom: 1px dashed #ccc; margin-bottom: .5em;">
    <td>Horizontal Scale</td>
    <td>%(h_scale)s</td>
</tr>
<tr style="border-bottom: 1px dashed #ccc; margin-bottom: .5em;">
    <td>Vertical Scale</td>
    <td>%(v_scale)s</td>
</tr>
<tr style="border-bottom: 1px dashed #ccc; margin-bottom: .5em;">
    <td>Elevation Exaggeration</td>
    <td>%(exag)s x</td> 
</tr>
</tbody>
</table>''' % (desc_values)
        
  
    def build_model_message(self, model_data, include_file = True):
        dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        sn = "5991"
        try:
            sn = model_serial.new_serial_number(self.config['serial_store'])
        except Exception:
                cherrypy.log("Serial Number Failure")
                cherrypy.log(traceback.format_exc)
                sn = "5991"

        model_data['sn'] = sn
        desc = self._build_description(model_data)
            
        m = {'fileName': 'Topophile Model #%s.stl' % sn,
            'description': desc,
            'hasRightsToModel': 1,
            'acceptTermsAndConditions': 1,
            'isPrivate': 1,
            'isForSale': 1,
            'materials': {'6': {'isActive': 1, 
                                'markup': model_pricing.get_model_service_markup(), 
                                'materialId': '6'}}}
                       
        if include_file: 
            model_file = os.path.join(self.config['model_dir'], model_data['model_id']) + '.stl'
            with open(model_file, 'rb') as f:
                m['file'] = base64.b64encode(f.read())
            
        return m
        
 
    @cherrypy.expose
    def upload(self, model_id):
        model_data = modelmd.get_model_metadata(self.config['model_dir'], model_id)
        
        client = printer.new_shapeways_client()
        response = client.add_model(self.build_model_message(model_data))
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(response)
      
    @cherrypy.expose    
    def upload_to_store(self, model_id):
        model_data = modelmd.get_model_metadata(self.config['model_dir'], model_id)
        client = printer.new_shapeways_client()
        response = client.add_model(self.build_model_message(model_data))
        return self.render("buy.html", {'modelUrl': response['urls']['privateProductUrl']['address'],
                                        'modelId': response['modelId']})
       
    @cherrypy.expose    
    def is_printable(self, swid, tpid, name=""):
        response = {'url': '', 'ready': False}
        client = printer.new_shapeways_client()
        if name:
            model = client.update_model_info(int(swid), {'title': name})
        else:
            model = client.get_model_info(int(swid))
            
        if 'materials' not in model or '6' not in model['materials']:
            response['errmsg'] = "Materials missing from response"
            return json.dumps(response)
            
        # printable = model['materials']['6']['isPrintable'] == 1
        printable = model['printable'] == 'yes'
        active = model['materials']['6']['isActive'] == 1
        response = {'url': model['urls']['privateProductUrl']['address']}
        response['ready'] = printable and active
       
        # setting a fixed markup - reenable if doing a percentage
        # if response['ready']:
        #    print "UPDATING PRICE"
        #    response['ready'] = response['ready'] and self.set_price(swid, tpid, model)
        
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
        