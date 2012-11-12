#!/usr/bin/env python
# Script for processing with map reduce the Open Street Map datasets.
# Counts the number of GPS hits in a discretized and scaled coordinates space.

# Example of input row: -778591613,1666898345   [as described here: http://blog.osmfoundation.org/2012/04/01/bulk-gps-point-data/ ]
# Example of output row: 1000-2579	282         [<latitude>-<longitude> \t <density value>]

import sys

SCALING = 10                # scaling factor, to decrease map resolution
MAX_LAT = 180 * SCALING
MAX_LON = 360 * SCALING
PDIV = 10000000 / SCALING

def mapper():
    
    for line in sys.stdin:
        
        line = line.strip()
        if len(line) < 6:               continue
        if len(line.split(',')) != 2:   continue
        
        coords = line.split(',')
        try:
            lat = int((90*SCALING) + round(float(coords[0])/PDIV))      # 0-1800
            lon = int((180*SCALING) + round(float(coords[1])/PDIV))	    # 0-3600
        except:
            continue

        if (lat <= MAX_LAT) and (lon <= MAX_LON):
            sys.stdout.write('LongValueSum:%s\t%d\n' % (str(lat) + "-" + str(lon), 1))
            

if __name__ == '__main__':
    mapper()
