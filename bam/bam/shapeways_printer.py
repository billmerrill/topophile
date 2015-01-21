from shapeways.client import Client

def price_model(model_data):
    client = Client(
        consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
        consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
        oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
        oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
        callback_url="http://localhost:3000/callback"
    )        

    # 6 - white strong and flexible
    # 26 - full color sandstone
    # 100 - full color plastic

    p = {'materials': [6, 26, 100],
       'volume': model_data['volume-mm3'] / 1000000000, 
       'area': model_data['area-mm2'] / 1000000,
       'xBoundMin': 0.0,
       'xBoundMax': model_data['x-size-mm'] / 1000,
       'yBoundMin': 0.0,
       'yBoundMax': model_data['y-size-mm'] / 1000,
       'zBoundMin': 0.0,
       'zBoundMax':model_data['z-size-mm'] / 1000 }
      
    rez = {}
    try:
        r = client.get_price(p)
        for m in r['prices']:
            rez[m] = r['prices'][m]['price']
    except Exception as e:
        print "Pricing failure"
        print type(e)
        
    return rez 