# ALS view 3.0
A small LAS data analysis Python project by Piotr Ostaszewski (325697) matching FTP GI demands version 3.0. The project consists of three scripts.

# class compare.py
* Reads a LAS file, displays point count per class (based on ASPRS classification) and an open3d visualisation of the whole point cloud. The same color palette used in both the chart and the visualization.

* Command line arguments:
1. path to LAS file

* Dependencies:
1. laspy[laszip]
2. open3d
3. numpy
4. matplotlib

# density_calculator.py
* Reads a LAS file, calculates point density per 1 square or cubic meter and displays the data as a histogram. The algorithm is based on analyzing neighbourhood of every nth point (default n is 1000, can be overriden with --sample flag). 2D mode flattens the data (ommits height coordinate) and counts points within the radius of a 1 square meter circle. This is the default. 3D mode counts points within a radius of 1 cubic meter sphere. By default script analyzes whole point cloud, but it can take into account only ground class if flag --ground is given.

* Command line arguments:
1. Path to LAS file

* Flags (optional)
1. --analyze3D (perform 3D instead of 2D analysis)
2. --ground (analyze only points classified as ground)
3. --sample [integer] (override default every 1000th sample rate)

* Depenencies:
1. laspy[laszip]
2. scipy
3. numpy
4. matplotlib

# DEM_difference.py
* Reads two LAS files (newer and older measurements of the same area), makes DEM terrain models (only ground class) and DEM coverage models (ground, buildings and vegetation classes) for both. Then coverage difference raster is made (the height values of older coverage are subtracted from new coverage). The raster shows changes in land coverage.

* Command line arguments:
1. Path to LAS file with newer data
2. Path to LAS file with older data
3. Path to output difference raster (including '.tif')
4. DEM resolution (optional, in meters, defaults to 1.0)
5. Processing directory (folder to store DEM rasters other than the difference raster, defailts to '_processing' in current working directory)
Please note that these are positional arguments, so ommiting 4. and passing 5. is not supported.

* Dependencies:
1. laspy[laszip]
2. arcpy
3. numpy
