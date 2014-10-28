import requests

model_file = '../bam/test-data/mto.tif'
url = "http://127.0.0.1:8080/"
      
def run_post():
    s = requests.Session()
    kv = {'size': '200',
          'rez': '50'}      
    files = {'elevation': open(model_file, 'rb')}
    print "Posting ", model_file
    r = s.post(url, params=kv, files=files)
    print r.text


def run_model_get():
    kv = {'size': '200',
          'rez': '50',
          'nwlat':'46.9290278',
          'nwlon':'-121.8229167',
          'selat':'46.7762500',
          'selon':'-121.6701389'
          }      
    r = requests.get(url, params=kv)      
    print r.status_code
    print r.text
    
run_model_get()