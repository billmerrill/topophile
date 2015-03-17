import re
import json

def get_model_metadata(model_dir, tpid):
    bogies = re.findall(r'[^A-Za-z0-9_\-\\]',tpid)
    if len(bogies) > 0:
        return None

    with open("%s/%s.json" % (model_dir, tpid), 'rb') as mjf:
        model_data = json.load(mjf)
        
    return model_data


def write_model_metadata(m):
    data_filename = m['filename'].replace('stl', 'json')
    jf = open(data_filename, 'wb')
    json.dump(m,jf)
    jf.close()