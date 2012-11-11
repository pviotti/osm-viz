#!/usr/bin/env python

import struct, math, sys, time
import shapefile
from check_point import is_point_in_poly    # Python module GCC compiled with Cython
import threading

SCALING = 10
MAX_LAT = 180 * SCALING
MAX_LON = 360 * SCALING
THREAD_SCALING = 9

INPUT_FILE = "reduced"
INPUT_FILE_DBF = "TM_WORLD_BORDERS-0.3.dbf"

global matrix     # MAX_LAT x  MAX_LON matrix
global shrec      # vector of polygons describing country boundaries

def load_matrix():
    fr = open(INPUT_FILE, 'r')
    matrix = [ [ 0 for i in range(MAX_LON) ] for i in range(MAX_LAT) ] # Matrix size: MAX_LAT rows x MAX_LON columns
    max_value = 0

    lines = fr.readlines()      
    for line in lines:
        val = line.split('\t')
        indexes = val[0]
        value = int(val[1])
        lat, lon = val[0].split("-")
        
        try:
            matrix[int(lat) - 1][int(lon) -1] = value 
        except:
            print "Error: ", lat, lon; sys.exit(1)
                
    fr.close()
    return matrix


def scale_points(points):
    new_points = []
    
    for p in points:
        x = int(round((p[1] + 90) * SCALING))      # 0-1800
        y = int(round((p[0] + 180) * SCALING)) # 0-3600
        new_points.append([x,y])
    
    return new_points 


def print_percentage(perc):
    sys.stdout.write("\r\x1b[K" + perc)
    sys.stdout.flush()
    
    
class Worker(threading.Thread):
    
    row_count = THREAD_SCALING
    wlock = threading.Lock()
    
    def __init__(self, starting_r):
        threading.Thread.__init__(self)
        self.starting_row = starting_r

    def run(self):
        global shrec
        global matrix
        Worker.wlock.acquire()
        print "Thread [", self.starting_row, " -  ", (self.starting_row + Worker.row_count), "] started"
        import time
        fn = 0
        Worker.wlock.release()
        for row in xrange(self.starting_row, self.starting_row + Worker.row_count):
            for column in xrange(MAX_LON):
                if matrix[row][column]:
                    done = 100 * float(((row-self.starting_row) * MAX_LON + column)) / (MAX_LON * Worker.row_count) + 0.001
                    pr = time.time()   
                    for sh in shrec:
                        if is_point_in_poly(row, column, sh.shape.points):
                            sh.osm_hit += matrix[row][column]
                            break
                    fn += time.time() - pr
                    remaining = fn * (100 - done) / done
                    print_percentage(" TH#=%d %.3f%% done, %.5f remaining [s]" % (self.starting_row,done, remaining))
        Worker.wlock.acquire()
        print "Thread [", self.starting_row, " -  ", self.starting_row + Worker.row_count, "] ended"
        Worker.wlock.release()
                            

def _debug_print(m,s):
    for row in xrange(s, s+100):
        for column in xrange(MAX_LON):
            if m[row][column]:
                print m[row][column], " ",
        print
    #sys.exit(0)


def create_countries():
    global matrix
    global shrec
    matrix = load_matrix()
    shrec = shapefile.Reader(INPUT_FILE_DBF).shapeRecords()
    
    for sh in shrec:
        sh.shape.points = scale_points(sh.shape.points)
        sh.osm_hit = 0

    workers = [Worker(count * THREAD_SCALING) for count in xrange(MAX_LAT / THREAD_SCALING)]    # 36 threads, scanning 50 rows each
    for w in workers: w.start()
    for w in workers: w.join()
    
    for sh in shrec:
        print sh.record[4], "-", sh.osm_hit

    # TEMP
    print "Saving objects with pickle..."                
    import pickle
    f = open("output.pkl", "wb")
    pickle.dump(shrec, f)
    f.close()


if __name__ == '__main__':
    create_countries()
