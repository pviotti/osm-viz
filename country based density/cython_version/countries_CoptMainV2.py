#!/usr/bin/env python

import struct, math, sys
import shapefile
from countries_CoptV2 import work

INPUT_FILE_DBF = "TM_WORLD_BORDERS-0.3.dbf"

def create_countries():
	attr = shapefile.Reader(INPUT_FILE_DBF)
	shrec = attr.shapeRecords()
	work(shrec)


if __name__ == '__main__':
	create_countries()
