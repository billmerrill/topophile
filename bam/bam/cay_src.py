import requests 
import os.path
from contextlib import closing
import sys
import geohash

def make_img_filename(nwlat, nwlon, selat, selon):
    return "%s-%s.tif" % (geohash.encode(float(nwlat), float(nwlon)), geohash.encode(float(selat), float(selon)))
    

def get_elevation_url_parts(nwlat, nwlon, selat, selon):
    # http://climb.local/cgi-bin/mapserv?FORMAT=image/tiff&REQUEST=GetCoverage&map=/Library/WebServer/Documents/cay/wcs.map&SERVICE=WCS&VERSION=1.0.0&coverage=gmted&CRS=epsg:4236&BBOX=-121.9870000,46.6867333,-121.5270000,47.0084000&RESX=0.002083&RESY=0.002083
    
    server_base = "http://127.0.0.1/cgi-bin/mapserv?"
    bbox = "%s,%s,%s,%s"% (nwlon, selat, selon, nwlat) #-90,38,-89,39
    
    gmted_params = {
        'map':      '/Library/WebServer/Documents/cay/wcs.map',
        'SERVICE':  'WCS',
        'VERSION':  '1.0.0',
        'REQUEST':  'GetCoverage',
        'coverage': 'gmted_ds',
        'CRS':      'epsg:4236',
        'BBOX':     bbox,
        'RESX':     '0.002083',
        'RESY':     '0.002083',
        'FORMAT':   'image/tiff'
    }
    srtm_params = {
        'map':      '/Library/WebServer/Documents/cay/wcs-srtm.map',
        'SERVICE':  'WCS',
        'VERSION':  '1.0.0',
        'REQUEST':  'GetCoverage',
        'coverage': 'srtmgl1',
        'CRS':      'epsg:4236',
        'BBOX':     bbox,
        'RESX':     '0.000277777777778',
        'RESY':     '0.000277777777778',
        'FORMAT':   'image/tiff'
    }
    
    return server_base, srtm_params
        
        
def get_elevation(nwlat, nwlon, selat, selon, retry = 0):
    if retry == 2:
        return None
    
    base_url, params = get_elevation_url_parts(nwlat, nwlon, selat, selon)
    elevation_fn = make_img_filename(nwlat, nwlon, selat, selon)
    status = get_elevation_image(elevation_fn, base_url, params)
    
    # if fn is None:
    #     retry = retry+1
    #     return get_elevation(nwlat, nwlon, selat, selon, retry=retry)        
       
    return  {'filename': status['file'],
             'nwlat': nwlat,
             'nwlon': nwlon,
             'selat': selat,
             'selon': selon,
             'status': status['status']}
             
def get_elevation_image(filename, base_url, params):
     filename = os.path.join(os.getcwd(), 'app/elevation_cache', filename)
     ret = {'file':None, 'status':None}
     written = 0
     import pprint
     with closing(requests.get(base_url, params=params, stream=True)) as response:
     # Do things with the response here.
         pprint.pprint(response)
         ret['status'] = response.status_code
         if response.status_code == 200:
             with open(filename, "wb") as save:
                 for chunk in response.iter_content(chunk_size=1024): 
                     if chunk: # filter out keep-alive new chunks
                         save.write(chunk)
                         save.flush()
                         written = written + len(chunk)
             ret['file'] = filename
     
     print ("Bytes Written %s " % (written))
            
     return ret
             
             
def main():
    #bbox = "-121.9870000,46.6867333,-121.5270000,47.0084000"
    print get_elevation('38.2', '-90','38','-89.8')
    
main()
 