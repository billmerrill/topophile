import requests

model_file = '../bam/test-data/mto.tif'
url = "http://127.0.0.1:8080/"
s = requests.Session()
kv = {'size': '200',
      'rez': '50'}      
      
files = {'elevation': open(model_file, 'rb')}
print "Posting ", model_file
r = s.post(url, params=kv, files=files)
print r.text
