import struct, math, sys

# cython yourmod.pyx
# gcc -o check_point.so -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 check_point.c
# in the main python file: from check_point import is_point_in_poly

SCALING = 10
MAX_LAT = 180 * SCALING
MAX_LON = 360 * SCALING

INPUT_FILE = "reduced"

def load_matrix():
	
	fr = open(INPUT_FILE, 'r')
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
				
	fr.close()
	
	return matrix
 
def is_point_in_poly(x,y,poly):

	# check if point is a vertex
	if (x,y) in poly: return True
	
	# check if point is on a boundary, 0 point specific case [OPTIMIZATION]
	if poly[0] == poly[1] and poly[0] == y and x > min(poly[0], poly[1]) and x < max(poly[0], poly[1]):
			return True
			
	n = len(poly)
	
	# check if point is on a boundary
	for i in range(1, n):
		p1 = poly[i-1]
		p2 = poly[i]
		if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
			return True
	  
	inside = False

	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y
		
	return inside

def scale_points(points):
	new_points = []
	
	for p in points:
		lat = int(round((p[1] + 90) * SCALING))	  # 0-1800
		lon = int(round((p[0] + 180) * SCALING))  # 0-3600
		new_points.append([lat,lon])
	
	return new_points 


def print_percentage(perc):
	sys.stdout.write("\r\x1b[K" + perc)
	sys.stdout.flush()
	
def work(shrec):
	matrix = load_matrix()

	for sh in shrec:
		sh.shape.points = scale_points(sh.shape.points)
		sh.osm_hit = 0

	import time
	fn = 0

	for row in range(MAX_LAT):
		for column in range(MAX_LON):
			if matrix[row][column]:
				done = 100 * float((row * MAX_LON + column)) / (MAX_LON * MAX_LAT)
				pr = time.time() 
			
				for sh in shrec:
					if is_point_in_poly(row, column, sh.shape.points):
						sh.osm_hit += matrix[row][column]
						break
						
				fn += time.time() - pr
				remaining = fn * (100 - done) / done
				print_percentage(" %.3f%% done, %.5f remaining [s]" % (done, remaining))

	import pickle
	f = open("output.pkl", "wb")
	pickle.dump(shrec, f)
	f.close()
