OpenStreetMap GPS point data visualization
==========================================

This repository hosts code and output of a visualization work about the density of GPS points from  the [OpenStreetMap bulk dataset](http://blog.osmfoundation.org/2012/04/01/bulk-gps-point-data/). After having created a gray scale bitmap of this, we superimposed it with the visualization of [world border dataset](http://thematicmapping.org/downloads/world_borders.php) and [NASA city light images](http://visibleearth.nasa.gov/view.php?id=55167) in order to compare the OSM contributions density with some data which hints about earth civilization.  

![OSM visualization](https://raw.github.com/pviotti/osm-viz/master/visualizations/output_withboundaries.png)


Technologies
------------
 * Python (Cython, Jython)
 * Amazon Elastic Map Reduce
 * Amazon Simple Storage Service


Authors
-------
[Luca Bonavita](http://www.mindrones.com/), [Marcello Pietri](http://weblab.ing.unimo.it/people/pietri/), [Roberto Piuca](http://www.linkedin.com/in/robertopiuca), [Paolo Viotti](https://github.com/pviotti/cv/raw/master/VIOTTI_Paolo-CV.pdf).
This was an exercise on visualizing big datasets we did at [Big Dive](http://www.bigdive.eu).


License
-------
GPL3. See COPYING for details.  
