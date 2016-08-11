from shapeways.client import Client
from topoconf import PROD, DEV

MODEL = 'model'
ALT = 'alt'

keyring = {
    # model = Topophile Modeler
    # alt = Topophile Model Helper
    PROD: {
        MODEL: {
            'consumer_key':     "80a769f7e26672fd6e1489c256edcf5cc6187259",
            'consumer_secret':  "df85f5d585929f4ec48c9fb19a9b251ca79767f6",
            'oauth_token':      "97cc59d7c01cf0cc7ec328bec6641c1af8c7f19b",
            'oauth_secret':     "b867c8067b583c9aeb159d3fcf449b81d6a55227"},

        ALT: {
            'consumer_key':     "45af704eeb304045413c1c40838dba815e7dd000",
            'consumer_secret':  "2ddb324f36d88372cccea673966d6619be3ab4ad",
            'oauth_token':      "fa219dd901f47f78b7403b4008599fe708c3d9d8",
            'oauth_secret':     "8b7ef6b94a034f34be0c2e900f69b60bffee8c3e"
        }
    },
    DEV: {
        MODEL: {
            'consumer_key':     "eebd23897cf4eb1b47f6edadd186291a6acea654",
            'consumer_secret':  "7c0883ed2c8105b710ed07cf0b76dd63e95b81bc",
            'oauth_token':      "562ef407136345dd61dcd602de4a7d079319f425",
            'oauth_secret':     "dd4e2d8aaf28a6c9d55b00ccdc0b47761902f8b0"
        }
    }
}


keyring[DEV][ALT] = keyring[DEV][MODEL]


def new_shapeways_client(env=DEV, key=MODEL):
    return Client(**keyring[env][key])


def price_model(model_data, env=DEV, key=ALT):

    client = new_shapeways_client(env, key)

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
         'zBoundMax': model_data['z-size-mm'] / 1000}

    rez = {}
    try:
        r = client.get_price(p)
        for m in r['prices']:
            rez[m] = r['prices'][m]['price']
    except Exception as e:
        print "Pricing failure"
        print type(e)

    return rez
