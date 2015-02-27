import requests
import re
import os.path
from contextlib import closing
import sys

# http://geobrain.laits.gmu.edu/cgi-bin/gbwcs-dem?service=wcs&version=1.0.0&request=getcoverage&coverage=SRTM_90m_Global&bbox=-90,38,-89,39&crs=epsg:4326&format=image/geotiff&store=true
# http://climb.local/cgi-bin/mapserv?map=/Library/WebServer/Documents/cay/new-srtm-wcs.map&SERVICE=WCS&VERSION=1.0.0&REQUEST=GetCoverage&coverage=srtmgl1&CRS=epsg:3857&BBOX=-13579530.723399062,5891090.039494356,-13528323.757634155,5943445.274026636&width=100&height=100&FORMAT=image/tiff
http://climb.local/cgi-bin/mapserv?map=/Library/WebServer/Documents/cay/new-srtm-wcs.map&SERVICE=WCS&VERSION=1.0.0&REQUEST=GetCoverage
&coverage=srtmgl1
&CRS=epsg:3857
&BBOX=-13579530.723399062,5891090.039494356,-13528323.757634155,5943445.274026636
&width=100
&height=100
&FORMAT=image/tiff

safari_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'DNT':'1'}
    
safari_headers = {}

def get_elevation_url():
    gburl = "http://geobrain.laits.gmu.edu/cgi-bin/gbwcs-dem"
    params = {'service':'wcs',
        'version':'1.0.0',
        'request':'getcoverage',
        'coverage':'SRTM_90m_Global',
        'bbox':'-90,38,-89.8,38.2',
        'crs':'epsg:4326',
        'format':'image/geotiff',
        'store':'true'}
        
    s = requests.Session()
    response = s.get(gburl, params = params, headers = safari_headers)
    print "===="
    print response.text
    print "===="
    reg = re.compile("Reference xlink:href=\"(\S+)\"")
    imgs = reg.findall(response.text)
    
    if imgs:
        return imgs[0]
    else:
        return None
        
def get_elevation_image(url):
    filename = os.path.split(url)[1]
    ret = ''
    with closing(requests.get(url, headers=safari_headers, stream=True)) as response:
    # Do things with the response here.
        print response.headers
        if response.status_code == 200:
            with open(filename, "wb") as save:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        save.write(chunk)
                        save.flush()
            ret = os.path.join(os.getcwd(), filename)
        else:
            ret = "error " + response.status_code
        
    return ret
    
def main():
    elevation_img_url = get_elevation_url()
    fn = "nope"
    if elevation_img_url:
        fn = get_elevation_image(elevation_img_url)
        
    print fn
    
def test():
    print get_elevation_image("http://monkey.org/~bill/geo/test.tif")
    
# main()
test()
 