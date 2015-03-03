# from pyshp https://code.google.com/p/pyshp/
import shapefile
import numpy as np

import sys
import json
import pprint


def close_enough(x, y, tol=1e-18, rel=1e-7):
    if tol is rel is None:
        raise TypeError('cannot specify both absolute and relative errors are None')
    tests = []
    if tol is not None: tests.append(tol)
    if rel is not None: tests.append(rel*abs(x))
    # assert tests
    return abs(x - y) <= max(tests)

TOP = True

def run():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
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
            #  print bandkey
        
    # for bk in bands:
    #     print bk, len(bands[bk])
    #     



    # sorted_points = sorted(points, key=sorter, reverse=False)    
    
    # print "Starting with %s shapes." % len(sorted_points)    
    
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
                    print "NEW blob, ", blob

    print "Ending with %s shapes." % len(output_rects) 
    with open('rectangles.json', 'wb') as of:
        json.dump(output_rects, of)
            
        
    
def check():
    if len(sys.argv) != 3:
        print sys.argv
        print "Usage: %s input_shapefile.shp output_filename"
        return False
    return True 
    

if __name__ == '__main__':
    if check():
        run()