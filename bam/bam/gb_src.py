import requests
import re
import os.path
from contextlib import closing
import sys

    
safari_headers = {}

def get_elevation(nwlat, nwlon, selat, selon, retry = 0):
    if retry == 2:
        return None
    
    elevation_img_url = get_elevation_url(nwlat, nwlon, selat, selon)
    fn = "Error"
    if elevation_img_url:
        fn = get_elevation_image(elevation_img_url)
    
    if fn is None:
        retry = retry+1
        return get_elevation(nwlat, nwlon, selat, selon, retry=retry)        
        
    return fn

def get_elevation_url(nwlat, nwlon, selat, selon):
    # http://geobrain.laits.gmu.edu/cgi-bin/gbwcs-dem?service=wcs&version=1.0.0&request=getcoverage&coverage=SRTM_90m_Global&bbox=-90,38,-89,39&crs=epsg:4326&format=image/geotiff&store=true

    # gburl = "http://geobrain.laits.gmu.edu/cgi-bin/gbwcs-dem"
    bbox = "%s,%s,%s,%s"% (nwlon, selat, selon, nwlat) #-90,38,-89,39
    # bbox = "-90,38,-89,39"
    # params = {'service':'wcs',
    #     'version':'1.0.0',
    #     'request':'getcoverage',
    #     'coverage':'SRTM_90m_Global',
    #     'bbox': bbox,
    #     'crs':'epsg:4326',
    #     'format':'image/geotiff',
    #     'store':'true'}

    # hax, gb requires params to be in order
    gburl = "http://geobrain.laits.gmu.edu/cgi-bin/gbwcs-dem?service=wcs&version=1.0.0&request=getcoverage&coverage=SRTM_90m_Global&bbox=%s&crs=epsg:4326&format=image/geotiff&store=true" % bbox
        
    print '### URL ', gburl
        
    response = requests.get(gburl)
    print response
    reg = re.compile("Reference xlink:href=\"(\S+)\"")
    imgs = reg.findall(response.text)
    
    if imgs:
        return imgs[0]
    else:
        return None
        
def get_elevation_image(url):
    filename = os.path.split(url)[1]
    filename = os.path.join(os.getcwd(), 'app/elevation_cache', filename)
    ret = {'file':None, 'status':None}
    content_size = 0
    written = 0
    with closing(requests.get(url, headers=safari_headers, stream=True)) as response:
    # Do things with the response here.
        ret['status'] = response.status_code
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            with open(filename, "wb") as save:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        save.write(chunk)
                        save.flush()
                        written = written + len(chunk)
            ret['file'] = filename
    
    print ("Content-size: %s vs Written %s " % (content_size, written))
    
    if content_size != written:
        print "\n###############################"
        print ("Bad GB Elevation Image: content-size: %s vs received-size %s " % (content_size, written))
        print "###############################\n"
        ret['file'] = None
        
           
    return ret['file']
    
def main():
    print get_elevation('-90','38','-89.8','38.2')
    
 