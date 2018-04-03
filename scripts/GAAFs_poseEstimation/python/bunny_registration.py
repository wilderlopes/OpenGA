import pcl
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


source_filename = '../../../data/bunny/sourcekps.pcd'
target_filename = '../../../data/bunny/targetkps.pcd'

def loadPCD(filename):
    """
    Load PCD file.

    Returns: panda dataframe with three columns, each one representing
    one coordinate (x, y, z). Each row is a sample.
    """

    pointCloud = pcl.load(filename)

    x = []
    y = []
    z = []
    for sample in pointCloud:
        x.append(sample[0])
        y.append(sample[1])
        z.append(sample[2])

    df_pointCloud = pd.DataFrame()
    df_pointCloud['x'] = x
    df_pointCloud['y'] = y
    df_pointCloud['z'] = z

    return df_pointCloud

# Load keypoint PCDs
sourceKps = loadPCD(source_filename)
targetKps = loadPCD(target_filename)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(sourceKps['x'], sourceKps['y'], sourceKps['z'], color='blue')
ax.scatter(targetKps['x'], targetKps['y'], targetKps['z'], color='red')
plt.show()
