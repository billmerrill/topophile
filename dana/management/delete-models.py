from shapeways.client import Client
import datetime

# topophile labs 

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
    delete_old_models()
#client.delete_model(%s)" % add_result['modelId'])
