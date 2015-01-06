import json
import time
import base64
import pprint
from os import system

from shapeways.client import Client

client = Client(
    consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
    consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
    oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
    oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
    callback_url="http://localhost:3000/callback"
)

'''
client = Client(
    consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
    consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
    callback_url="http://localhost:3000/callback"
)
'''

p =  {
        'xBoundMin':  0.0,
        'xBoundMax':  0.05932,
        'yBoundMin':  0.0,
        'yBoundMax':  0.05932,
        'zBoundMin':  0.0,
        'zBoundMax':  0.01534
        }
        
p =  {
        'xBoundMin':  0.0,
        'xBoundMax':  0.2,
        'yBoundMin':  0.0,
        'yBoundMax':  0.15,
        'zBoundMin':  0.0,
        'zBoundMax':  0.15
        }

p =  {
        'xBoundMin':  0.0,
        'xBoundMax':  0.65,
        'yBoundMin':  0.0,
        'yBoundMax':  0.35,
        'zBoundMin':  0.0,
        'zBoundMax':  0.55
        }
p =  {
        'xBoundMin':  0.0,
        'xBoundMax':  0.010,
        'yBoundMin':  0.0,
        'yBoundMax':  0.010,
        'zBoundMin':  0.0,
        'zBoundMax':  0.010
        }
       
        
x = (p['xBoundMax'] - p['xBoundMin'])
y = (p['yBoundMax'] - p['yBoundMin'])
z = (p['zBoundMax'] - p['zBoundMin'])

p['volume'] = x*y*z
p['area'] = 2*x*y + 2*x*z + 2*y*z


pricetest = { 'xBoundMin': 0.0,
              'xBoundMax': .3000, 
              'yBoundMin': 0.0,
              'yBoundMax': .19245108570111924,
              'zBoundMin': 0.0,
              'zBoundMax': .045144946952235827,
              'volume': 1040075.0398049863 / 1000000000,
              'area': 141600.1233810283 / 1000000,
              'materials': [6] }  
pprint.pprint (client.get_price(pricetest))
exit()
              
              
            #   '', "filename": "/Users/bill/qrl/topophile/topophile/bam/bam/app/model_cache/c29mcwxp20bp-c29t1g8181bn.stl", "area-mm2": 141600.1233810283, "z-size-mm": 45.144946952235827, "volume-mm3": 1040075.0398049863}

# 6 - white strong and flexible
# 26 - full color sandstone
# 100 - full color plastic

p['materials'] = [6]        


'''
        1. ``file`` - str (the file data)
        2. ``fileName`` - str
        3. ``hasRightsToModel`` - bool
        4. ``acceptTermsAndConditions`` - bool

        Optional Parameters:

        1. ``uploadScale`` - float
        2. ``title`` - str
        3. ``description`` - str
        4. ``isPublic`` - bool
        5. ``isForSale`` - bool
        6. ``isDownloadable`` - bool
        7. ``tags`` - list
        8. ``materials`` - dict
        9. ``defaultMaterialId`` - int
        10. ``categories`` - list
'''

def make_mat_dict():
    '''
    {
      "<materialId>":{
        "id":"<materialId>",
        "type":"object",
        "description":"Material Object",
        "properties":{
          "markup":{
            "type":"float",
            "description":"Markup amount"
          },
          "isActive":{
            "type":"boolean",
            "description":"Is this material active"
          }
        }
      }
    }
    '''

    mats = {
            "6": 
                { "id": 6,
			'type': 'object',
			'description': 'material object',
			'properties': {
				'markup': {
					'type': 'float',
					'description': 123.45},
				'isActive': {
					'type': 'boolean',
					'description': 1 }
			}
          }
		}

			
    return mats


p = {'fileName': 'topo-%s.stl' % int(time.time()),
	'hasRightsToModel': 1,
	'acceptTermsAndConditions': 1,
    'isClaimable': 1,
	# 'uploadScale': .001,
	# 'title': 'api testing model =]',
	# 'description': '[Mon Dec 22 12:41:39 2014].525589 msDrawRasterLayerGDAL(): src=706,489,524,122, dst=0,0,524,122 [Mon Dec 22 12:41:39 2014].525593 msDrawRasterLayerGDAL(): source raster PL (705.932,488.601) for dst PL (0,0).',
	# 'isPublic': 1,
	# 'isForSale': 1,
	# 'isDownloadable': 0,
	# 'tags': 'mountains, hashtags',
	'materials': make_mat_dict(),
	# 'default_material_id': 6
	}
    
def make_public(p):
    p['isPublic'] = 1
    p['isClaimable'] = 0

def make_claimable(p):
    p['isPublic'] = 0
    p['isClaimable'] = 1
    
    
    
with open('test.stl', 'rb') as f:
	p['file'] = base64.b64encode(f.read())
    
make_public(p)
# make_claimable(p)
p['isForSale'] = 1

pprint.pprint(p)
print('\n\n-----------\n\n')
add_result = client.add_model(p)

pprint.pprint(add_result)

print
print
print(add_result['modelId'])


print("Claim URL http://www.shapeways.com/model/%s/?key=%s " % (add_result['modelId'], add_result['claimKey']))

time.sleep(5)


# go_url = "http://www.shapeways.com/model/%s/?key=%s" % (add_result['modelId'], add_result['claimKey'])
go_url = add_result['urls']['publicProductUrl']
print go_url
cmd ='open -a "google chrome" "%s"' % str(go_url)
system(cmd)

# pprint.pprint (client.get_materials())
#pprint.pprint(p)
#pprint.pprint (client.get_price(p))
#p['volume'] = p['volume']/100.0
#pprint.pprint (client.get_price(p))

print("client.delete_model(%s)" % add_result['modelId'])
