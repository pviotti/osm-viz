In this folder are some code attempts of computing a country based OSM GPS density.  

For each coordinate point having more than one GPS hits we check which country it belongs to using the borders shape file and than we compute some average figure about OpenStreeMap contribution per country.  

Since it is a computationally intensive task, we coded a multithreaded version meant to be executed with Jython and a C powered one featuring Cython.