import re
import json


def get_model_metadata(model_dir, tpid):
    bogies = re.findall(r'[^A-Za-z0-9_\-\\]', tpid)
    if len(bogies) > 0:
        return None

    with open("%s/%s.json" % (model_dir, tpid), 'rb') as mjf:
        model_data = json.load(mjf)

    return model_data


def write_model_metadata(dest, data):
    jf = open(dest, 'wb')
    json.dump(data, jf)
    jf.close()
