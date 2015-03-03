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

TOP = False

def run():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    sf = shapefile.Reader(input_filename)
    shapes = sf.shapes()
    points = []
    for s in shapes:
        
        points.append([x.tolist() for x in s.points])

    def sorter(x):
        return x[0][1], x[0][0]

    sorted_points = sorted(points, key=sorter, reverse=False)    
    
    print "Starting with %s shapes." % len(sorted_points)    
    
    output_rects = []
    blob = None
    blob_sizes = []
    blob_count = 0
   
    def _close(a,b):
        c = [.3, .3]
        return np.all(np.less(np.absolute(np.subtract(a,b)), c))
       
       
    # for i,p in enumerate(sorted_points):
    #     if not blob:
    #         print "Start Blob: ", p
    #         blob = p
    for i in range(0, len(sorted_points)):
        if not blob:
            if TOP:
                print "Start Blob: ", sorted_points[i]
            blob = sorted_points[i]
            
        else:
            is_neighbor = False
            cury = blob[0][1]
            
            for j in range(0, len(sorted_points)):
                print i,j
                if sorted_points[j][0][1] != cury:
                    if TOP:
                        print "Mismatch 0y", sorted_points[j][0] , cury
                    continue
                else: 
                    if TOP:
                        print "continuing"
                    else: 
                        pass
                
                if _close(blob[1], sorted_points[j][0]):
                    if TOP:
                        print "CLOOOSE"
                    if i != j:
                        blob[1] = sorted_points[j][1]
                        blob[2] = sorted_points[j][2]
                        is_neighbor = True
                        if TOP:
                            print "Matched Back, grow", blob
                        break
                        
                elif _close(blob[0], sorted_points[j][1]):
                    if TOP:
                        print "CLOOOSE"
                    if i != j:
                        blob[0] = sorted_points[j][0]
                        blob[3] = sorted_points[j][3]
                        is_neighbor = True
                        if TOP:
                            print "Matched Front, grow", blob
                        break
                        
            if not is_neighbor:
                output_rects.append(blob)
                if TOP:
                    print "End Blob", blob
                blob = None

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