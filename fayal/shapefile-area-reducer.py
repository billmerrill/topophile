# from pyshp https://code.google.com/p/pyshp/
import shapefile
import numpy as np

import sys
import json
import pprint
import geojson


TOP = False

def reduce_rects():
    input_filename = sys.argv[1]
    
    sf = shapefile.Reader(input_filename)
    shapes = sf.shapes()
    points = []
    bands = {}
    for s in shapes:
        r = [x.tolist() for x in s.points]
        bandkey = round(r[0][1])
        if bandkey in bands:
            bands[bandkey].append(r)
        else:
             bands[bandkey] = [r]
             
    # for b in bands:
    #     print "XX ", b, " - ", len(bands[b])
    #     if b == -31:
    #         for bb in bands[b]:
    #             print bb[0]
    # 
    output_rects = []
    blob_sizes = []
    blob_count = 0
    
    def _close(a,b):
        c = [.3, .3]
        return np.all(np.less(np.absolute(np.subtract(a,b)), c))

    def _sorter(x):
        return x[0][0]
        
    for band in bands:
        sband = sorted(bands[band], key=_sorter)
        l = len(sband)
        blob = None
        for x in range(0, l):
            curr = sband[x]
            if not blob:
                blob = curr
                if TOP:
                    print "NEW blob, ", blob
            
            else:
                if _close(blob[1], curr[0]):
                    blob[1] = curr[1]
                    blob[2] = curr[2]
                    is_neighbor = True
                    if TOP:
                        print "Matched Back, grow", blob
                else:
                    if TOP:
                        print "Ending blob, starting new"
                    output_rects.append(blob)
                    blob = curr
                    if TOP:
                        print "NEW blob, ", blob
        if blob:
            output_rects.append(blob)

    print "Ending with %s shapes." % len(output_rects) 
    return output_rects
    # with open('rectangles.json', 'wb') as of:
    #     json.dump(output_rects, of)
            

def write_geojson(rects):
    output_filename = sys.argv[2]

    features = []
    for i,r in enumerate(rects):
        # print round(r[0][0])
        # if round(r[0][0]) == -30.0:
        #     print "HEY ", r
        features.append(geojson.Feature(geometry=geojson.Polygon([r]), id=str(i)))
    
    collection = geojson.FeatureCollection(features=features)
    
    with open (output_filename, 'wb') as output:
        json.dump(collection, output)
    
    
        
    
def check():
    if len(sys.argv) != 3:
        print sys.argv
        print "Usage: %s input_shapefile.shp output_filename"
        return False
    return True 
    

if __name__ == '__main__':
    if check():
        rects = reduce_rects()
        write_geojson(rects)