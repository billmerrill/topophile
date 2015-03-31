from shapeways.client import Client

def new_shapeways_client(ring='model'):
    #topophilelabs
    return Client(
        consumer_key="1694232fb1ee4d3441d0970934f994885409c9e2",
        consumer_secret="06e28ec74812adf61bb582e0ec218aede5fe3420",
        oauth_token = "a66163431a2215c48d2c4cb75fb348f19642df31",
        oauth_secret = "c3b86a32247cdd5777ec2bc181447adbf9fe945b"
    )

# topophile modeler
modeler_client_values = {
    'consumer_key':"ea29837886ad7e769872dd86e02e0bba50fcf02d",
    'consumer_secret':"7627ff80f3668369c02bb286fe31956d5b9d9dff",
    'oauth_secret': "700ff4c3291942bca5e5fd7c6195e073bd867444",
    'oauth_token': "d016feacb49497d9daddb778698969d542fb04fb"}

# topophile assistant
modeler_assistant_client_values = {
    'consumer_key':"fa206ebf6c8e642d3ed0e4ee7be72e1ba4266f37",
    'consumer_secret':" 06db7be844acc56473ac6ca8998cc2e50656e019",
    'oauth_secret': "8564c4f28aa7c73d0b9a32133a98e257762d9df4",
    'oauth_token': "b2c4268daaeff446328a0197ddbf722d8719ce02"
}




def price_model(model_data):
    
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