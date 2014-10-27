import requests
import re
import os.path
from contextlib import closing
import sys

safari_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'DNT':'1'}
    
safari_headers = {}

def get_elevation(nwlat, nwlon, selat, selon):
    elevation_img_url = get_elevation_url(nwlat, nwlon, selat, selon)
    fn = "Error"
    if elevation_img_url:
        fn = get_elevation_image(elevation_img_url)

    return fn

def get_elevation_url(nwlat, nwlon, selat, selon):
    gburl = "http://geobrain.laits.gmu.edu/cgi-bin/gbwcs-dem"
    bbox = "%s,%s,%s,%s"% (nwlat, nwlon, selat, selon) #'-90,38,-89.8,38.2',
    params = {'service':'wcs',
        'version':'1.0.0',
        'request':'getcoverage',
        'coverage':'SRTM_90m_Global',
        'bbox': bbox',
        'crs':'epsg:4326',
        'format':'image/geotiff',
        'store':'true'}
        
    response = requests.get(gburl, params = params, headers = safari_headers)
    # print "===="
    # print response.text
    # print "===="
    reg = re.compile("Reference xlink:href=\"(\S+)\"")
    imgs = reg.findall(response.text)
    
    if imgs:
        return imgs[0]
    else:
        return None
        
def get_elevation_image(url):
    filename = os.path.split(url)[1]
    ret = {'file':None, 'status':None}
    content_size = 0
    with closing(requests.get(url, headers=safari_headers, stream=True)) as response:
    # Do things with the response here.
        ret['status'] = response.status_code
        content_size = response.headers['content-length']
        if response.status_code == 200:
            with open(filename, "wb") as save:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk: # filter out keep-alive new chunks
                        save.write(chunk)
                        save.flush()
            ret['file'] = os.path.join(os.getcwd(), filename)
           
    return ret['file']
    
def main():
    print get_elevation('-90','38','-89.8','38.2')
    
main()
 