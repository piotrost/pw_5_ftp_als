# ALS view 3.0
A small LAS data analysis python project by Piotr Ostaszewski (325697) matching FTP GI demands version 3.0.

# Scripts
1. class compare.py - Reads a LAS file, displays point count per class (based on ASPRS classification) and open3d visualisation of the whole point cloud. The same color palette used in both the chart and the visualization.

Command line arguments:
- path to LAS dataset

Dependencies:
- laspy[laszip]
- open3d
- numpy
- matplotlib

