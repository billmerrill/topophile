# from pyshp https://code.google.com/p/pyshp/
import shapefile
import numpy as np

import sys


def close_enough(x, y, tol=1e-18, rel=1e-7):
    if tol is rel is None:
        raise TypeError('cannot specify both absolute and relative errors are None')
    tests = []
    if tol is not None: tests.append(tol)
    if rel is not None: tests.append(rel*abs(x))
    # assert tests
    return abs(x - y) <= max(tests)

def run():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    sf = shapefile.Reader(input_filename)
    shapes = sf.shapes()
    print "Starting with %s shapes." % len(shapes)    
    
    output_rects = []
    blob = None
    blob_sizes = []
    blob_count = 0
   
    def _close(a,b):
        c = [.3, .3]
        return np.all(np.less(np.absolute(np.subtract(a,b)), c))
        
    itr = range(len(shapes))
    itr2 = range(len(shapes))
      
    for i in itr:
        if not blob:
            blob = shapes[i].points
        
        else:
            found_neighbor = False
            for j in itr2:
                # print '\n-----\n'
                # print i,j, blob, 
                # print '\n===\n'
                # print shapes[j].points
                if _close(blob[1], shapes[j].points[0]):
                    # print blob[1], shapes[j].points
                    if i != j:
                        blob[1] = shapes[j].points[1]
                        blob[2] = shapes[j].points[2]
                        found_neighbor = True
                        break
                elif _close(blob[0], shapes[j].points[1]):
                    # print 'second check:', i, j, blob[0], shapes[j].points
                    if i != j:
                        blob[0] = shapes[j].points[0]
                        blob[3] = shapes[j].points[3]
                        found_neighbor = True
                        break
                        
            if not found_neighbor:
                output_rects.append(blob)
                blob = None
                print 'nope'
            else:
                print 'yep'
                
 
    
    # for i,s in enumerate(shapes):
    #     if not blob:
    #         blob = s.points
    #         
    #     else:
    #         # match, grow blob
    #         # if np.allclose(blob[1], s.points[0], atol=1):
    #         found_neighbor = False
    #         for x in range (i, len(shapes)):
    #         
    #             if _close(blob[1], shapes[x].points[0]):
    #                 blob[1] = shapes[x].points[1]
    #                 blob[2] = shapes[x].points[2]
    #                 found_neighbor = True
    #                 blob_count += 1
    #                 break
    #                 
    #         if not found_neighbor:
    #             # print 'new blob', shapes[x].points
    #             blob_sizes.append(blob_count)
    #             output_rects.append(blob);
    #             # print "%s\t%s" % (blob_count, blob)
    #             blob_count = 1
    #             blob = None
    #   
    np.sort(output_rects)
    for r in output_rects:
        print '%s: %s' % ((r[0][0] - r[1][0]) , r)
     
    print "Ending with %s shapes." % len(output_rects) 
    # print blob_sizes
            
        
    
def check():
    if len(sys.argv) != 3:
        print sys.argv
        print "Usage: %s input_shapefile.shp output_filename"
        return False
    return True 
    

if __name__ == '__main__':
    if check():
        run()