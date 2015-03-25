import requests

model_file = '../bam/test-data/mto.tif'
#url = "http://127.0.0.1:8080/"
url = "http://billmerrill.webfactional.com/build"
      
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
          'selon':'-121.6701389',
          'zfactor':'2.2',
          'price': 'e',
	  'width': '100',
	  'height': '100',
	  'hollow': 1
          }      
    r = requests.get(url, params=kv)      
    print r.headers
    print r.status_code
    print r.text
    
def run_price_check():
    #test_model_name = "c0xbw8e1b50n-c22p78x48p8n"
    test_model_name = "c236t1htbh8p-c23d12n4b181-cube-100-200-1_5"
    test_url = url + "price"
    kv = {'model_id': test_model_name,
          }
    r = requests.get(test_url, params=kv)
    print test_url
    # print r.headers
    # print r.status_code
    print r.text
    
run_model_get()
#run_price_check()
