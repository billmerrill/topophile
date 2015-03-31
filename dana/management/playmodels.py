from shapeways.client import Client
import datetime

# topophile labs 

PROD = 'prod'
DEV = 'dev'
MODEL = 'model'
ALT = 'alt'

keyring = {
    PROD : { MODEL : {
                'consumer_key':"ea29837886ad7e769872dd86e02e0bba50fcf02d",
                'consumer_secret':"7627ff80f3668369c02bb286fe31956d5b9d9dff",
                'oauth_secret': "700ff4c3291942bca5e5fd7c6195e073bd867444",
                'oauth_token': "d016feacb49497d9daddb778698969d542fb04fb"},
                
            ALT : {
                'consumer_key':"fa206ebf6c8e642d3ed0e4ee7be72e1ba4266f37",
                'consumer_secret':"06db7be844acc56473ac6ca8998cc2e50656e019",
                'oauth_secret': "8564c4f28aa7c73d0b9a32133a98e257762d9df4",
                'oauth_token': "b2c4268daaeff446328a0197ddbf722d8719ce02"
            }
    },
    DEV : { MODEL: {
            'consumer_key': "1694232fb1ee4d3441d0970934f994885409c9e2",
            'consumer_secret': "06e28ec74812adf61bb582e0ec218aede5fe3420",
            'oauth_token': "a66163431a2215c48d2c4cb75fb348f19642df31",
            'oauth_secret': "c3b86a32247cdd5777ec2bc181447adbf9fe945b"
    }}
}
keyring[DEV][ALT] = keyring[DEV][MODEL]


def get_client(env, key):
    return Client(**keyring[env][key])

def delete_old_models():
    client = Client(
        consumer_key="ea29837886ad7e769872dd86e02e0bba50fcf02d",
        consumer_secret="7627ff80f3668369c02bb286fe31956d5b9d9dff",
        oauth_token = "ee87280a80066e0e1920b7030c855a715c7d70f2",
        oauth_secret = "c4904cf2dbf2f34958a828f06208637175114a57")

    max_age_days = 7

    models = []
    page = 1
    while True:
        tmpm = client.get_models(page=page)
        page += 1
        if tmpm['models'] is None:
            break
        models.extend(tmpm['models'])


    old = 0
    skipped = 0

    today = datetime.datetime.now()
    for m in models:
        try:
            creation = datetime.datetime.strptime(m['title'], "Your New Model %Y-%m-%d %H:%M")
        except ValueError:
            skipped += 1
            continue
        diff = today - creation
        if diff.days > max_age_days:
            old += 1
            print "deleting ", m['modelId']
            client.delete_model(m['modelId'])
       
    print "Found %s models." % len(models)
    print "Deleted %s models, older than %s days."  % (old, max_age_days)
    print "Skipped %s malformed titles." % skipped
    

if __name__ == '__main__':
    pass
    
    # delete_old_models()
#client.delete_model(%s)" % add_result['modelId'])
