
# cython yourmod.pyx
# gcc -o check_point.so -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 check_point.c
# in the main python file: from check_point import is_point_in_poly


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
