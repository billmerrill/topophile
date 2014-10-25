import requests

url = "http://127.0.0.1:8080/"
s = requests.Session()
kv = {'size': '200',
      'rez': '50'}      
      
files = {'elevation': open('../bam/test-data/mto.tif', 'rb')}

print files['elevation']

r = s.post(url, params=kv, files=files)
print r.text
