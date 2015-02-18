from shapeways.client import Client

def new_shapeways_client():
    return Client(
        consumer_key="1694232fb1ee4d3441d0970934f994885409c9e2",
        consumer_secret="06e28ec74812adf61bb582e0ec218aede5fe3420",
        oauth_token = "a66163431a2215c48d2c4cb75fb348f19642df31",
        oauth_secret = "c3b86a32247cdd5777ec2bc181447adbf9fe945b"
    )
    # return Client(
    #     consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
    #     consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
    #     oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
    #     oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
    # )
        

def price_model(model_data):
    # client = Client(
    #     consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
    #     consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
    #     oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
    #     oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57",
    #     callback_url="http://localhost:3000/callback"
    # )        
    
    client = new_shapeways_client()

    # 6 - white strong and flexible
    # 26 - full color sandstone
    # 100 - full color plastic

    p = {'materials': [6],
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