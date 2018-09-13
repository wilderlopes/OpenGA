import os
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import common.constants as constants
from pandas.plotting import scatter_matrix

# Parser
# parser = argparse.ArgumentParser(
#     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#     description="Using GAAFs to predict wind",
#     epilog="OpenGA - www.openga.org")
#
# parser.add_argument('-inputfile', help='Job scheduler accounting file', nargs='+')
# parser.add_argument('-o', '--output',
#                     help='Output directory for the report',
#                     default='report')


df = pd.read_csv(constants.DATASETPATH + 'dataset_hourly.csv')
df[constants.DATETIME] = pd.to_datetime(df[constants.DATETIME])
df[constants.MAINDIRECTION] =  df.loc[:, constants.MAINDIRECTION].astype(str)
df[constants.MAINDIRECTIONDEG] = df.loc[:, constants.MAINDIRECTION].replace(constants.DIC_WIND_DIRECTION)
print(df.dtypes)
print(df.head())
# print(collections.Counter(df[constants.MAINDIRECTION]).most_common())

def plot_chart(samples):
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].set_title('Wind speed')
    axarr[0].scatter(df.index.values[:samples], df[constants.V_AVGSPEED][:samples])
    axarr[0].set_ylabel(constants.V_AVGSPEED)
    axarr[1].scatter(df.index.values[:samples], df[constants.V_AVGSPEED][:samples], color='r')
    axarr[1].set_ylabel(constants.U_AVGSPEED)
    # axarr.XAxis.set_ticklabels(df.index)
    plt.show()

# if __name__ == '__main__':

# plot_chart(1000)

# df.hist(column=[constants.V_AVGSPEED, constants.U_AVGSPEED])
# plt.show()

# Calculate scatter matrix
scatter_matrix(df[[constants.V_AVGSPEED, constants.U_AVGSPEED, constants.MAINDIRECTIONDEG]], alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.show()
