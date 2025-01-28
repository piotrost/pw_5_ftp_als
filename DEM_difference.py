# Author: Piotr Ostaszewski (325697)

import arcpy
import laspy
import sys
import os
import numpy as np

def subtract_DEMs(cloud1, cloud2, output, DEM_resolution, processing_dir):
    # processing directory
    if not os.path.exists(processing_dir):
        os.makedirs(processing_dir)

    # las generated for further processing
    clouds_list = [] # [terrain1, coverage1, terrain2, coverage2]

    # rasters generated for further processing
    raster_list = [] # [terrain1, coverage1, terrain2, coverage2]

    # generate filtered point clouds
    for i, cl in enumerate([cloud1, cloud2]):
        # read dataset and get name
        las = laspy.read(cl)
        cl_name = os.path.basename(cl).split('.')[0]      

        # paths for terrain
        terrain_cloud_path = os.path.join(processing_dir, cl_name + f'_terrain_{i+1}.las')
        clouds_list.append(terrain_cloud_path)
        terrain_raster_path = os.path.join(processing_dir, cl_name + f'_terrain_{i+1}.tif')
        raster_list.append(terrain_raster_path)
        
        # filter and write terrain
        terrain_cloud = laspy.LasData(las.header)
        terrain_cloud.points = las.points[las.classification == 2]
        terrain_cloud.write(terrain_cloud_path)
        
        # paths for coverage
        coverage_cloud_path = os.path.join(processing_dir, cl_name + f'_coverage_{i+1}.las')
        clouds_list.append(coverage_cloud_path)
        coverage_raster_path = os.path.join(processing_dir, cl_name + f'_coverage_{i+1}.tif')
        raster_list.append(coverage_raster_path)
        
        # filter and write coverage
        coverage_cloud = laspy.LasData(las.header)
        coverage_cloud.points = las.points[np.isin(las.classification, [2, 3, 4, 5, 6])]
        coverage_cloud.write(coverage_cloud_path)
    
    # generate DEMs
    for i in range(0, 4):
        las_dataset = arcpy.CreateLasDataset_management(
            clouds_list[i]
        )

        arcpy.LasDatasetToRaster_conversion(
            las_dataset,
            raster_list[i],
            value_field="ELEVATION",
            sampling_type="CELLSIZE",
            sampling_value=DEM_resolution,
        )
    
    # subtract coverages
    coverages_difference = arcpy.Raster(raster_list[1]) - arcpy.Raster(raster_list[3])
    
    if not os.path.isabs(output):
        output = os.path.join(os.getcwd(), output)
    
    coverages_difference.save(output)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Please provide all necessary command line arguments. DEM_resolution (defaults to 1.0 m) and processing_dir (defaults to '_processing') are optional.")
        print("\nUsage: python DEM_difference.py <path_to_newer_las_file> <path_to_older_las_file> <output_raster.tif> <output_DEMs_resolution> <processing_dir>")
        sys.exit(1)

    # output raster resolution
    if len(sys.argv) >= 5:
        DEM_resolution = float(sys.argv[4])
    else:
        DEM_resolution = 1.0
    
    # processing directory
    if len(sys.argv) >= 6:
        processing_dir = os.path(sys.argv[5])
    else:
        processing_dir = os.path.join('_processing')

    # run
    subtract_DEMs(
        cloud1=sys.argv[1],
        cloud2=sys.argv[2],
        output=sys.argv[3],
        DEM_resolution=DEM_resolution,
        processing_dir=processing_dir
    )