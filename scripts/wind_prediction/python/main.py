# Start by importing the necessary Python modules:
import sys, string, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import log
from matplotlib.backends.backend_pdf import PdfPages
import common.constants as constants
from matplotlib.lines import Line2D

custom_lines = [Line2D([0], [0], color='magenta', linestyle='--', lw=1)]

# Line2D([0], [0], color='blue', lw=2),
#                 Line2D([0], [0], color='green', lw=2),
#                 Line2D([0], [0], color='black', lw=2),

# Simulation parameters
#====================================================
# The user is able to set the following AF parameters:
#
# Number of filter taps (system order): M
#
# Realizations: L
#
# Time iterations: N
#
# AF step size: mu
#
# Measurement Noise variance: sigma2v

M       = 6 # System order
L       = 1 # Realizations
N       = 1500 # Time iterations
mu      = 1e-9 # AF Step size
sigma2v = 1e-15 # Variance of measurement noise
sigma2q = 0 # Variance of random-walk noise
corr_input = 0 # Level of correlation between input's entries.
BINARY  = 'GA-LMS_rotors_linpred' # Note that you can call any of the following binaries:
		   # GA-LMS --> Complete subalgebra of R^3
		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
           # GA-LMS_rotors_linpred --> Even subalgebra of R (isomorphic to the real numbers)
#====================================================
pp = PdfPages('learningCurves' + BINARY + '.pdf') # multipage pdf to save figures

# The binary is called below using the previously set parameters. The GA-LMS runs and
# returns .txt files with the results: *_galms.out and *_theory.out, where * represents
# "MSE" or "EMSE". *_galms.out files store the ensemble-average learning curves (EMSE),
# while *_theory.out files store the theoretical steady-state value for MSE and EMSE.

# Calling binary
arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(mu) + " " + str(sigma2v) + " " + str(sigma2q) + " " + str(corr_input)
os.system("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments)

# Load files MSE_galms.out and MSE_theory.out to plot MSE learning curve and theoretical curve:

f1 = open('MSE_galms.out', 'r')
data_label1 = ['MSE_galms']
data1_list = []
for line in f1:
    data1_list.append(line.rstrip('\n'))

f2 = open('MSE_theory.out', 'r')
data_label2 = ['MSE_theory']
data2_list = []
for line in f2:
    for i in range(len(data1_list)):
        data2_list.append(line.rstrip('\n'))

data1 = [float(j) for j in data1_list] # Converts to float
data2 = [float(j) for j in data2_list] # Converts to float
data1_dB = [10*log(x,10) for x in data1]
data2_dB = [10*log(x,10) for x in data2]

plt.title('MSE curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
          mu, sigma2v, sigma2q, corr_input), fontsize=9)
plt.ylabel('MSE (dB)')
plt.xlabel('Iterations')
plt.plot(data1_dB, label = 'MSE_galms')
plt.plot(data2_dB, label = 'MSE_theory')
plt.legend()
#plt.savefig('MSE.png', bbox_inches='tight')
pp.savefig()
#plt.show()
plt.close()

# Load files EMSE_galms.out and EMSE_theory.out to plot EMSE learning curve and theoretical curve:

# f1 = open('EMSE_galms.out', 'r')
# data_label1 = ['EMSE_galms']
# data1_list = []
# for line in f1:
#     data1_list.append(line.rstrip('\n'))
#
# f2 = open('EMSE_theory.out', 'r')
# data_label2 = ['EMSE_theory']
# data2_list = []
# for line in f2:
#     for i in range(len(data1_list)):
#         data2_list.append(line.rstrip('\n'))
#
# data1 = [float(j) for j in data1_list] # Converts to float
# data2 = [float(j) for j in data2_list] # Converts to float
# data1_dB = [10*log(x,10) for x in data1]
# data2_dB = [10*log(x,10) for x in data2]
#
# plt.title('EMSE curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
#           mu, sigma2v, sigma2q, corr_input), fontsize=9)
# plt.ylabel('EMSE (dB)')
# plt.xlabel('Iterations')
# plt.plot(data1_dB, label = 'EMSE_galms', color = 'r')
# plt.plot(data2_dB, label = 'EMSE_theory', color = 'magenta')
# plt.legend()
# #plt.savefig('EMSE.png', bbox_inches='tight')
# pp.savefig()
# #plt.show()
#
# plt.close()



# Comparison d versus y
width  = 6 #3.487
height = width / 1.618
size_annotation = 6
size_legend = 6

df = pd.read_csv('/home/openga/data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS.csv')
colors = ['orange', 'blue', 'green', 'black']
blades = [0, 3, 5, 6]
cols = constants.COLS_FOR_SIM
dic = dict(zip(blades, cols))
start_plot = 3 # sample where plotting should start (useful to discard the first
# samples where the AF is reaching the signal to be tracked).

fig, [ax1, ax2] = plt.subplots(2, 1, sharex=True)
# plt.figure(figsize=(13.69,8.27))
# plt.figure(figsize=(6, 3.5))
# plt.title('y curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
#           mu, sigma2v, sigma2q, corr_input), fontsize=9)
# plt.ylabel('mbar')
# plt.xlabel('Iterations')
ax1.set_ylabel('mbar')
# ax1.set_xlabel('Iterations')
for i in range(1):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    # data_label1 = ['y_galms_{}'.format(blades[i])]
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    range_plot = range(len(data1)-start_plot)
    ax1.scatter(range_plot, df[dic[blades[i]]].values[start_plot:len(data1)], label = 'actual_{}'.format(dic[blades[i]]), color=colors[i], s=1)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax1.plot(range_plot, data1[start_plot:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=1.5)
ax1.legend(custom_lines, ['predicted'], loc=2, prop={'size': size_legend})
ax1.annotate('Dynamic_Pressure', xy=(1000, 14400), size=size_annotation)

ax2.set_ylabel('m/s')
ax2.set_xlabel('Iterations')
for i in range(1, len(blades)):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    # data_label1 = ['y_galms_{}'.format(blades[i])]
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    range_plot = range(len(data1)-start_plot)
    ax2.scatter(range_plot, df[dic[blades[i]]].values[start_plot:len(data1)], label = 'actual_{}'.format(dic[blades[i]]), color=colors[i], s=1)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax2.plot(range_plot, data1[start_plot:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=1.5)
ax2.annotate('NorthSouth_Wind', xy=(50, 1600), size=size_annotation)
ax2.annotate('EastWest_Wind', xy=(50, 1000), size=size_annotation)
ax2.annotate('Vertical_Wind', xy=(50, 300), size=size_annotation)
fig.set_size_inches(width, height)
pp.savefig()
plt.close()

# Zoomed in figures
zoom_range_start = 1200
zoom_range_end = 1500
fig, [ax1, ax2] = plt.subplots(1, 2)
ax1.set_ylabel('mbar')
ax1.set_xlabel('Iterations')
for i in [0]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    # data_label1 = ['y_galms_{}'.format(blades[i])]
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]
    ax1.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=1)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax1.plot(range(zoom_range_start, zoom_range_end), data1, label = 'Predicted', linestyle='--', color='magenta', linewidth=1.5)
ax1.annotate('Dynamic_Pressure', xy=(1350, 14970), size=size_annotation)
ax1.legend(prop={'size': size_legend})
# ax1.legend(custom_lines, ['predicted'], loc='lower left')

ax2.set_ylabel('m/s')
ax2.set_xlabel('Iterations')
for i in [3]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    # data_label1 = ['y_galms_{}'.format(blades[i])]
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]
    ax2.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=1)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linestyle=None, marker='.')
    ax2.plot(range(zoom_range_start, zoom_range_end), data1, label = 'Predicted', linestyle='--', color='magenta', linewidth=1.5)
ax2.annotate('Vertical_Wind', xy=(1200, 115), size=size_annotation)
ax2.legend(prop={'size': size_legend})
# ax3.annotate('NorthSouth_Wind', xy=(50, 1600))
# ax3.annotate('EastWest_Wind', xy=(50, 1000))
# ax3.annotate('Vertical_Wind', xy=(50, 300))
fig.set_size_inches(width, 0.7*height)
plt.tight_layout()
pp.savefig()
plt.close()
pp.close()
