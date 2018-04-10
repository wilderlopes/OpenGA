import pcl
import pickle
import pandas as pd
import sys, string, os
import numpy as np
# import matplotlib.pyplot as plt
from math import log
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.backends.backend_pdf import PdfPages

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

if __name__ == '__main__':

    # savefolder = './Figures/'
    # if not os.path.exists(savefolder):
    #     os.makedirs(savefolder)

    # pp = PdfPages(savefolder + '/bunny.pdf') # multipage pdf to save figures

    BINARY = 'GA-LMS_bunny'
    source_filename = '../../../data/bunny/sourcekps.pcd'
    target_filename = '../../../data/bunny/targetkps.pcd'
    correspondences = '../../../data/bunny/cleanedCorrs.txt'
    correspondences_for_error = '../../../data/bunny/good_correspondences.txt'

    mu_values = 8;
    mu_steep = mu_values/4; # It has to be 1/4 of the mu_values according to the steepest-descent update rule (Eq. (12) in the paper).

    # Load keypoint PCDs
    sourceKps = loadPCD(source_filename)
    targetKps = loadPCD(target_filename)

    # Call binary to perform registration
    arguments = " " + str(target_filename) + " " + str(source_filename) + " " + str(correspondences) + " " + str(correspondences_for_error) + " " + str(mu_steep) + " " + str(mu_values)
    print('> Calling binary with the following parameters: \n {}'.format(arguments))
    os.popen('../Simulations/Scripts/Cpp/' + BINARY + "/build/" + BINARY + arguments).read()

    # Load registered PCD
    sourceKps_reg = loadPCD('sourcekps_reg.pcd')

    # Save PCDs in pickle file
    pickle.dump(sourceKps, open("sourceKps.p", "wb"))
    pickle.dump(targetKps, open("targetKps.p", "wb"))
    pickle.dump(sourceKps_reg, open("sourceKps_reg.p", "wb"))

    # Plot
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(sourceKps['x'], sourceKps['y'], sourceKps['z'], color='blue')
    # ax.scatter(targetKps['x'], targetKps['y'], targetKps['z'], color='red')
    # ax.scatter(S_reg['x'], S_reg['y'], S_reg['z'], color='green')
    # # plt.show()
    # pp.savefig()
    # #plt.show()
    # plt.close()
    # pp.close()
