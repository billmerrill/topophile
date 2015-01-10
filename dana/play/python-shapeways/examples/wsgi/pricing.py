import json
import pprint
import sys
from shapeways.client import Client

def make_price_message(attrs):
    '''
    {"x-size-mm": 100.0, 
    "y-size-mm": 33.038729405978835, 
    "filename": "/Users/bill/qrl/topophile/topophile/bam/bam/app/model_cache/c236s72vpbrv-c236rt70010n.stl", 
    "area-mm2": 13989.16517522048, 
    "z-size-mm": 41.09875455038955, 
    "volume-mm3": 94449.621147067635}
    '''
    pmsg = { 'xBoundMin': 0.0,
                  'xBoundMax': attrs['x-size-mm'] / 1000, 
                  'yBoundMin': 0.0,
                  'yBoundMax': attrs['y-size-mm'] / 1000,
                  'zBoundMin': 0.0,
                  'zBoundMax': attrs['y-size-mm'] / 1000,
                  'volume': attrs['volume-mm3'] / 1000000000,
                  'area': attrs['area-mm2'] / 1000000,
                  'materials': [6] }  
                  
    return pmsg
    

                  
def get_pricing(model_attrs):
    
    client = Client(
        consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
        consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
        oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
        oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
        callback_url="http://localhost:3000/callback"
    )
   
    pmsg = make_price_message(json.loads(model_attrs))
    price = client.get_price(pmsg)
    pprint.pprint(price)
    

def read_input():    
    msg = ""
    for line in sys.stdin:
        msg += line
        
    return msg
    
if __name__ == '__main__':
    msg = read_input()
    get_pricing(msg)