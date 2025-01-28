# Author: Piotr Ostaszewski (325697)

import laspy
import numpy as np
import open3d
import matplotlib.pyplot as plt
import sys

custom_colors = {
    0: [1, 1, 1],
    1: [0.2, 0.2, 0.2],
    2: [0.6, 0.3, 0.1],
    3: [0.5, 0.9, 0.5],
    4: [0.2, 0.7, 0.2],
    5: [0.1, 0.5, 0.1],
    6: [0.6, 0.15, 0.15],
    7: [0.9, 0.8, 0.2],
    8: [0.9, 0.5, 0.1],
    9: [0.2, 0.4, 0.8],
    10: [0.6, 0.2, 0.6],
    11: [1, 1, 1],
    12: [0.9, 0.5, 0.1]

}

# https://www.asprs.org/wp-content/uploads/2010/12/LAS_Specification.pdf
names_ASPRS = {
    0: "Created, never classified",
    1: "Unclassified",
    2: "Ground",
    3: "Low vegetation",
    4: "Medium vegetation",
    5: "High vegetation",
    6: "Building",
    7: "Low point (noise)",
    8: "Reserved",
    9: "Water",
    10: "Rail",
    11: "Road surface",
    12: "Reserved"
}

def class_chart_and_visualization(las_path):
    # read
    las_dataset = laspy.read(las_path)
    header = las_dataset.header

    # translation vector
    min = header.min
    max = header.max
    vec = (min + max) / 2

    # original coords
    i = las_dataset.x
    j = las_dataset.y
    k = las_dataset.z

    # xyz
    xyz = np.vstack((i, j, k)).T
    xyz = xyz - vec

    # colors
    colors = np.zeros((len(las_dataset), 3))

    # class point count
    point_count = []

    for aclass in names_ASPRS.keys():
        class_filtered = np.zeros(len(las_dataset), dtype=bool)
        class_filtered |= (las_dataset["classification"] == aclass)
        
        # point count
        point_count.append(np.sum(class_filtered))

        # color
        colors[class_filtered] = custom_colors[aclass]

    # plot
    fig, ax = plt.subplots()
    ax.bar(names_ASPRS.values(), point_count, color=[custom_colors[i] for i in names_ASPRS.keys()])
    plt.xticks(rotation=90)
    plt.xlabel('Class')
    plt.ylabel('Point count')
    plt.title('Point count by ASPRS classification')
    plt.tight_layout()
    plt.grid()
    plt.show()

    # load into open3d
    point_cloud = open3d.geometry.PointCloud()
    point_cloud.points = open3d.utility.Vector3dVector(xyz)
    point_cloud.colors = open3d.utility.Vector3dVector(colors)

    # visualization
    open3d.visualization.draw_geometries([point_cloud])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide path to your LAS file as command line argument.")
        print("\nUsage: python class_compare.py <path_to_your_LAS_file>")
        sys.exit(1)

    class_chart_and_visualization(sys.argv[1])