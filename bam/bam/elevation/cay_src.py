import requests 
import os.path
from contextlib import closing
import sys
import geohash
import pyproj

googp = pyproj.Proj(init='epsg:3857')
geop = pyproj.Proj(init='epsg:4236')

def get_sphere_merc_bbox(nwlat, nwlon, selat, selon):
    # se = pyproj.trans-13559317.321564,5918366.22606463)
    # nw = pyproj.transform(geop, googp, nwlat, nwlon)
    # se = pyproj.transform(geop, googp, selat, selon)
    nw = pyproj.transform(geop, googp, nwlon, nwlat)
    se = pyproj.transform(geop, googp, selon, selat)

    # bbox = "%s,%s,%s,%s"% (nwlon, selat, selon, nwlat) #-90,38,-89,39
    bbox = "%s,%s,%s,%s"% (nw[0], se[1], se[0], nw[1]) #-90,38,-89,39
    return bbox
    
def get_rezs(bbox, dims):
    bbox = [float(x) for x in bbox.split(',')]
    rez = {}
    rez['x'] = (bbox[2] - bbox[0])/float(dims['x'])
    rez['y'] = (bbox[3] - bbox[1])/float(dims['y'])
    return rez

def get_elevation_url_parts(app_config, nwlat, nwlon, selat, selon, dimensions=False):
    # http://climb.local/cgi-bin/mapserv?FORMAT=image/tiff&REQUEST=GetCoverage&map=/Library/WebServer/Documents/cay/wcs.map&SERVICE=WCS&VERSION=1.0.0&coverage=gmted&CRS=epsg:4236&BBOX=-121.9870000,46.6867333,-121.5270000,47.0084000&RESX=0.002083&RESY=0.002083
    
    # server_base = "http://127.0.0.1/cgi-bin/mapserv?"
    server_base = app_config['elevation_server']
    
    # gmted_params = {
    #     'map':      '/Library/WebServer/Documents/cay/wcs.map',
    #     'SERVICE':  'WCS',
    #     'VERSION':  '1.0.0',
    #     'REQUEST':  'GetCoverage',
    #     'coverage': 'gmted_ds',
    #     'CRS':      'epsg:4236',
    #     'BBOX':     bbox,
    #     'RESX':     '0.002083',
    #     'RESY':     '0.002083',
    #     'FORMAT':   'image/tiff'
    # }
    if dimensions:
        bbox = get_sphere_merc_bbox(nwlat,nwlon, selat, selon)
        rezs = get_rezs(bbox, dimensions)
        # Get elevation data by resolution or dimension,
        # turns out about the same
        if True:
            srtm_params = {
                'map':      '/Library/WebServer/Documents/cay/new-srtm-wcs.map',
                'SERVICE':  'WCS',
                'VERSION':  '1.0.0',
                'REQUEST':  'GetCoverage',
                'coverage': 'srtmgl1',
                'CRS':      'epsg:3857',
                'BBOX':      bbox,
                'RESX':      rezs['x'],
                'RESY':      rezs['y'],
                'FORMAT':   'image/tiff' }
        else:
            srtm_params = {
                'map':      '/Library/WebServer/Documents/cay/new-srtm-wcs.map',
                'SERVICE':  'WCS',
                'VERSION':  '1.0.0',
                'REQUEST':  'GetCoverage',
                'coverage': 'srtmgl1',
                'CRS':      'epsg:3857',
                'BBOX':      bbox,
                'WIDTH':     dimensions['x'],
                'HEIGHT':    dimensions['y'],
                'FORMAT':   'image/tiff' }
    else:
        bbox = "%s,%s,%s,%s"% (nwlon, selat, selon, nwlat) #-90,38,-89,39
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
        
        
def get_elevation(app_config, elevation_filename, nwlat, nwlon, selat, selon, retry = 0):
    if retry == 2:
        return None
    
    base_url, params = get_elevation_url_parts(app_config, nwlat, nwlon, selat, selon)
    status = get_elevation_image(elevation_filename, base_url, params)
    
    return  {'filename': status['file'],
             'nwlat': nwlat,
             'nwlon': nwlon,
             'selat': selat,
             'selon': selon,
             'status': status['status']}
             
def get_scaled_elevation(app_config, elevation_filename, nwlat, nwlon, selat, selon, dimensions, retry = 0):
    if retry == 2:
        return None
    
    base_url, params = get_elevation_url_parts(app_config, nwlat, nwlon, selat, selon, dimensions)
    status = get_elevation_image(elevation_filename, base_url, params)
    
    return  {'filename': status['file'],
             'nwlat': nwlat,
             'nwlon': nwlon,
             'selat': selat,
             'selon': selon,
             'status': status['status']}
             
def get_elevation_image(filename, base_url, params):
     ret = {'file':None, 'status':None}
     written = 0
     with closing(requests.get(base_url, params=params, stream=True)) as response:
     # Do things with the response here.
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
    
# main()
 