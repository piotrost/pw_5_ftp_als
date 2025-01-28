# Author: Piotr Ostaszewski (325697)

import laspy
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.spatial import cKDTree
import argparse

def density_chart(las_path, D, only_ground, sample_rate):
    # read
    las_dataset = laspy.read(las_path)
    if only_ground:
        las_dataset.points = las_dataset.points[las_dataset.classification == 2]    # filter if necessary
    header = las_dataset.header

    # translation vector
    min = header.min
    max = header.max
    vec = (min + max) / 2

    # 2D
    if D == 2:
        # original coords
        i = las_dataset.x
        j = las_dataset.y

        # xy
        coords = np.vstack((i, j)).T
        coords = coords - vec[:2]

        query_radius = np.sqrt(1/np.pi) # from circle field formula for 1 m^2 field
    
    # 3D
    elif D == 3:
        # original coords
        i = las_dataset.x
        j = las_dataset.y
        k = las_dataset.z

        # xyz
        coords = np.vstack((i, j, k)).T
        coords = coords - vec

        query_radius = (3/(4*np.pi))**(1/3) # from sphere volume formula for 1 m^3 volume

    # calculate density
    kdtree = cKDTree(coords)
    neighbour_groups = kdtree.query_ball_point(
        coords[::sample_rate], r=query_radius, workers = -1
    )
    densities = [len(neighbours) for neighbours in neighbour_groups]

    # Create a histogram of the densities
    plt.figure(figsize=(10, 6))
    plt.hist(densities, bins=20, edgecolor='black')
    plt.xlabel(f'Density, points per 1 m^{D}')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Point Densities (Every {sample_rate}th Point)')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("path", type=str, help="Path to las file")
        parser.add_argument("--analyze3D", action="store_true", help="Analyze 3D density")
        parser.add_argument("--ground", action="store_true", help="Analyze only ground class points")
        parser.add_argument("--sample", type=str, help="Sampling rate for filtering point cloud")
        args = parser.parse_args()

        # analyze 2D or 3D density
        if args.analyze3D:
            D = 3
        else:
            D = 2

        # analyze whole point cloud or just ground points
        if args.ground:
            only_ground = True
        else:
            only_ground = False
        
        # sample rate for filtering point cloud
        if args.sample is None:
            sample_rate = 1000
        else:
            sample_rate = int(args.sample)
    except:
        pass

    try:
        density_chart(args.path, D, only_ground, sample_rate)
    except Exception as e:
        print("Please provide all necessary command line arguments. Flags are optionl.")
        print("\nUsage: python density_claculator.py <path_to_your_las_file> --analyze3D --ground --sample <sampling_rate_integer>")
        print(f"\nError: {e}")
        sys.exit(1)
