#!/usr/bin/env python
# Script to create the bitmap from the map reduce dump file 

import struct, math, sys

SCALING = 10
MAX_LAT = 180 * SCALING
MAX_LON = 360 * SCALING
PDIV = 10000000 / SCALING

INPUT_FILE = "reduced"
OUTPUT_FILE = "output.bmp"


def load_matrix():
    
    with open(INPUT_FILE, 'r') as fr:
        matrix = [ [ 0 for i in range(MAX_LON) ] for i in range(MAX_LAT) ] # Matrix size: MAX_LAT rows x MAX_LON columns
        max_value = 0

        print "File scanning..."
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
             
            if value > max_value: 
                max_value = value
    
	print "Normalize values in 0-255..."
    for lat in range(len(matrix)):
        for lon in range(len(matrix[0])):
            matrix[lat][lon] = int(round( 255 * math.log( matrix[lat][lon] + 1) / math.log( max_value + 1) ) )
	
    return matrix


def bmp_write(d,the_bytes):
    """ Function to write a bmp file.  It takes a dictionary (d) of
        header values and the pixel data (bytes) and writes them
        to a file.  This function is called at the bottom of the code. """
    mn1 = struct.pack('<B',d['mn1'])
    mn2 = struct.pack('<B',d['mn2'])
    filesize = struct.pack('<L',d['filesize'])
    undef1 = struct.pack('<H',d['undef1'])
    undef2 = struct.pack('<H',d['undef2'])
    offset = struct.pack('<L',d['offset'])
    headerlength = struct.pack('<L',d['headerlength'])
    width = struct.pack('<L',d['width'])
    height = struct.pack('<L',d['height'])
    colorplanes = struct.pack('<H',d['colorplanes'])
    colordepth = struct.pack('<H',d['colordepth'])
    compression = struct.pack('<L',d['compression'])
    imagesize = struct.pack('<L',d['imagesize'])
    res_hor = struct.pack('<L',d['res_hor'])
    res_vert = struct.pack('<L',d['res_vert'])
    palette = struct.pack('<L',d['palette'])
    importantcolors = struct.pack('<L',d['importantcolors'])

    outfile = open(OUTPUT_FILE,'wb')
    # write the header + the_bytes
    outfile.write(mn1+mn2+filesize+undef1+undef2+offset+headerlength+width+height+\
                  colorplanes+colordepth+compression+imagesize+res_hor+res_vert+\
                  palette+importantcolors+the_bytes)
    outfile.close()

  
def main():
    
    print "Image size: %dx%d pixel" % (MAX_LAT, MAX_LON)

    # Here is a minimal dictionary with header values.
    # Of importance is the offset, headerlength, width, height and colordepth.
    # Edit the width and height to your liking.
    d = {
        'mn1':66,
        'mn2':77,
        'filesize':0,
        'undef1':0,
        'undef2':0,
        'offset':54,
        'headerlength':40,
        'width':MAX_LON,
        'height':MAX_LAT,
        'colorplanes':0,
        'colordepth':24,
        'compression':0,
        'imagesize':0,
        'res_hor':0,
        'res_vert':0,
        'palette':0,
        'importantcolors':0
        }
        
    print "Loading matrix..."
    maxtrix = load_matrix()

    # Build the byte array.  This code takes the height and width values from the dictionary above and
    # generates the pixels row by row.  The row_mod and padding stuff is necessary to ensure that the byte count for each
    # row is divisible by 4.  This is part of the specification.
    the_bytes = ''
    for row in range(d['height']-1,-1,-1): # (BMPs are L to R from the bottom L row)
        for column in range(d['width']):
            b = maxtrix[-row][column]
            g = maxtrix[-row][column]
            r = maxtrix[-row][column]
            pixel = struct.pack('<BBB',b,g,r)
            the_bytes = the_bytes + pixel
        row_mod = (d['width']*d['colordepth']/8) % 4
        if row_mod == 0:
            padding = 0
        else:
            padding = (4 - row_mod)
        padbytes = ''
        for i in range(padding):
            x = struct.pack('<B',0)
            padbytes = padbytes + x
        the_bytes = the_bytes + padbytes
        
    # call the bmp_write function with the dictionary of header values 
    # and the bytes created above.
    bmp_write(d,the_bytes)
    

if __name__ == '__main__':
    main()
