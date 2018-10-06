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

M       = 4 # System order
L       = 1 # Realizations
N       = 1200 # Time iterations
mu      = 0.8e-9 # AF Step size
sigma2v = 0 # Variance of measurement noise
sigma2q = 0 # Variance of random-walk noise
corr_input = 0 # Level of correlation between input's entries.
BINARY  = 'GA-LMS_linpred' # Note that you can call any of the following binaries:
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

# Comparison d versus y
width  = 12 #3.487
height = width / 1.9 #1.618
size_annotation = 9
size_annotation_zoom = 7
size_legend = 9
sizedot = 5
linewidth = 2
start_plot = 3 # sample where plotting should start (useful to discard the first
# samples where the AF is reaching the signal to be tracked).
x_start = 0
x_end = N #1000
plot_LMSs = True

# Call regular LMS to estimate each data column
mu_list = [1e-9, 1e-8, 0.5e-8, 3e-8, 1e-6, 1e-6, 1e-6, 1.6e-6]
LMS_curves_to_plot = range(8)
for col_number in LMS_curves_to_plot:
    BINARY  = 'GA-LMS_real_linpred' # Note that you can call any of the following binaries:
    arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(mu_list[col_number]) + " " + str(sigma2v) + " " + str(sigma2q) + " " + str(corr_input)
    os.system("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments  + " " + str(col_number))

# Load files MSE_galms.out and MSE_theory.out to plot MSE learning curve and theoretical curve:
f1 = open('MSE_galms.out', 'r')
data_label1 = ['MSE_galms']
data1_list = []
for line in f1:
    data1_list.append(line.rstrip('\n'))

# f2 = open('MSE_theory.out', 'r')
# data_label2 = ['MSE_theory']
# data2_list = []
# for line in f2:
#     for i in range(len(data1_list)):
#         data2_list.append(line.rstrip('\n'))

data1 = [float(j) for j in data1_list] # Converts to float
# data2 = [float(j) for j in data2_list] # Converts to float
data1_dB = [10*log(x,10) for x in data1]
# data2_dB = [10*log(x,10) for x in data2]

plt.title('MSE curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
          mu, sigma2v, sigma2q, corr_input), fontsize=9)
plt.ylabel('MSE (dB)')
plt.xlabel('Iterations')
cmap = plt.cm.autumn
colors = []
for i in np.linspace(0, 1, 8):
    colors.append(cmap(i))

if plot_LMSs:
    for col_number in LMS_curves_to_plot:
        f3 = open('MSE_galms_real_{}.out'.format(col_number), 'r')
        # data_label3 = ['MSE_galms_real']
        data3_list = []
        for line in f3:
            data3_list.append(line.rstrip('\n'))
        data3 = [float(j) for j in data3_list] # Converts to float
        data3_dB = [10*log(x,10) for x in data3]
        plt.plot(data3_dB, label = 'MSE_LMS_{}'.format(col_number), linestyle='--', color=colors[col_number], linewidth=linewidth)

# plt.plot(data2_dB, label = 'MSE_theory')
plt.plot(data1_dB, label = 'MSE_galms', color='green')
plt.legend()
#plt.savefig('MSE.png', bbox_inches='tight')
pp.savefig()
# plt.show()
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



df = pd.read_csv('/home/openga/data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS_complete.csv')

from matplotlib.lines import Line2D
cmap = plt.cm.RdYlBu
colors = []
for i in np.linspace(0.8, 1, 8):
    # colors.append(cmap(i))
    colors.append((0, 0.8, 0.9))
    # colors.append((0, 0.9, 0.1))
# colors = ['orange', 'blue', 'green', 'black', ]
blades = [0, 1, 2, 4, 3, 5, 6, 7]
cols = constants.COLS_FOR_SIM_COMPLETE
dic = dict(zip(blades, cols))

fig, [ax1, ax2, ax3, ax4] = plt.subplots(4, 1, sharex=True)
ax1.set_ylabel('mbar')
for i in [0]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    range_plot = range(start_plot, len(data1))

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float

    ax1.scatter(range_plot, df[dic[blades[i]]].values[start_plot:len(data1)], label = 'actual_{}'.format(dic[blades[i]]), color=colors[i], s=sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax1.plot(range_plot, data1[start_plot:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax1.plot(range_plot, data2[start_plot:], label = 'predicted_LMS_{}'.format(dic[blades[i]]), linestyle='--', color='black', linewidth=linewidth)
ax1.set_xlim([x_start, x_end])
ax1.legend(custom_lines, ['Predicted'], loc=2, prop={'size': size_legend})
ax1.annotate('Dynamic_Pressure {{{}}}'.format(r"$1$"), xy=(763, 14340), size=size_annotation)

ax2.set_ylabel('m/s')
# ax2.set_xlabel('Iterations')
for i in range(1, 4):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    range_plot = range(start_plot, len(data1))

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float

    ax2.scatter(range_plot, df[dic[blades[i]]].values[start_plot:len(data1)], label = 'actual_{}_{}'.format(dic[blades[i]], blades[i]), color=colors[i], s=sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax2.plot(range_plot, data1[start_plot:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax2.plot(range_plot, data2[start_plot:], label = 'predicted_LMS_{}'.format(dic[blades[i]]), linestyle='--', color='black', linewidth=linewidth)
ax2.set_xlim([x_start, x_end])
# ax2.legend()
ax2.annotate('NorthSouth_Wind {{{}}}'.format(r"$\gamma_{2}$"), xy=(20, 1500), size=size_annotation)
ax2.annotate('EastWest_Wind {{{}}}'.format(r"$\gamma_{1}$"), xy=(20, 980), size=size_annotation)
ax2.annotate('Vertical_Wind {{{}}}'.format(r"$\gamma_{3}$"), xy=(20, 300), size=size_annotation)

ax3.set_ylabel('deg')
# ax3.set_xlabel('Iterations')
for i in range(4, 7):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    range_plot = range(start_plot, len(data1))

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float

    ax3.scatter(range_plot, df[dic[blades[i]]].values[start_plot:len(data1)], label = 'actual_{}_{}'.format(dic[blades[i]], blades[i]), color=colors[i], s=sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax3.plot(range_plot, data1[start_plot:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax3.plot(range_plot, data2[start_plot:], label = 'predicted_LMS_{}'.format(dic[blades[i]]), linestyle='--', color='black', linewidth=linewidth)
ax3.set_xlim([x_start, x_end])
# ax3.legend()
ax3.annotate('Roll {{{}}}'.format(r"$\gamma_{12}$"), xy=(40, 160), size=size_annotation)
ax3.annotate('Pitch {{{}}}'.format(r"$\gamma_{31}$"), xy=(40, 345), size=size_annotation)
ax3.annotate('Yaw {{{}}}'.format(r"$\gamma_{23}$"), xy=(40, -70), size=size_annotation)

ax4.set_ylabel('deg')
ax4.set_xlabel('Iterations')
for i in [7]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    range_plot = range(start_plot, len(data1))

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float

    ax4.scatter(range_plot, df[dic[blades[i]]].values[start_plot:len(data1)], label = 'actual_{}'.format(dic[blades[i]]), color=colors[i], s=sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax4.plot(range_plot, data1[start_plot:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax4.plot(range_plot, data2[start_plot:], label = 'predicted_LMS_{}'.format(dic[blades[i]]), linestyle='--', color='black', linewidth=linewidth)
ax4.set_xlim([x_start, x_end])
# ax4.legend(custom_lines, ['Predicted'], loc=2, prop={'size': size_legend})
ax4.annotate('Angle_Of_Attack {{{}}}'.format(r"$\gamma_{123}$"), xy=(760, 40), size=size_annotation)
fig.set_size_inches(0.65*width, height)
pp.savefig()
plt.close()

# Zoomed-in figures
zoom_range_start = 0 #300
zoom_range_end = 100 #450
fig, [ax1, ax2] = plt.subplots(2, 1)
ax1.set_ylabel('deg')
# ax1.set_xlabel('Iterations')
for i in range(4, 7):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float
    data2 = data2[zoom_range_start:zoom_range_end]

    ax1.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=0.5*sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax1.plot(range(zoom_range_start, zoom_range_end), data1, label = 'GA-LMS', linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax1.plot(range(zoom_range_start, zoom_range_end), data2, label = 'LMS', linestyle='--', color='black', linewidth=linewidth)
ax1.legend(custom_lines, ['predicted'], loc=(0.6, 0.75))
ax1.annotate('Roll {{{}}}'.format(r"$\gamma_{12}$"), xy=(300, 200), size=size_annotation)
ax1.annotate('Pitch {{{}}}'.format(r"$\gamma_{31}$"), xy=(300, 70), size=size_annotation)
ax1.annotate('Yaw {{{}}}'.format(r"$\gamma_{23}$"), xy=(300, -110), size=size_annotation)
# ax1.legend(prop={'size': size_legend})

ax2.set_ylabel('deg')
ax2.set_xlabel('Iterations')
for i in [7]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float
    data2 = data2[zoom_range_start:zoom_range_end]

    ax2.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=1.3*sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linestyle=None, marker='.')
    ax2.plot(range(zoom_range_start, zoom_range_end), data1, label = 'GA-LMS', linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax2.plot(range(zoom_range_start, zoom_range_end), data2, label = 'LMS', linestyle='--', color='black', linewidth=linewidth)
ax2.annotate('Angle_Of_Attack {{{}}}'.format(r"$\gamma_{123}$"), xy=(375, 69), size=size_annotation)
ax2.legend(prop={'size': size_legend}, loc='lower left')
# ax2.legend(custom_lines, ['predicted'], loc='upper right')
# fig.set_size_inches(width, 0.7*height)
# fig.set_size_inches(0.95*height*height/width, height)
fig.set_size_inches(0.35*width, height)
plt.tight_layout()
# plt.subplots_adjust(wspace=0.4)
pp.savefig()
plt.close()

# Zoomed-in figures 2
zoom_range_start = 300
zoom_range_end = 450
fig, [ax1, ax2] = plt.subplots(2, 1)
ax1.set_ylabel('deg')
# ax1.set_xlabel('Iterations')
for i in range(4, 7):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float
    data2 = data2[zoom_range_start:zoom_range_end]

    ax1.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=0.5*sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax1.plot(range(zoom_range_start, zoom_range_end), data1, label = 'GA-LMS', linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax1.plot(range(zoom_range_start, zoom_range_end), data2, label = 'LMS', linestyle='--', color='black', linewidth=linewidth)
ax1.legend(custom_lines, ['predicted'], loc=(0.6, 0.75))
ax1.annotate('Roll {{{}}}'.format(r"$\gamma_{12}$"), xy=(300, 200), size=size_annotation)
ax1.annotate('Pitch {{{}}}'.format(r"$\gamma_{31}$"), xy=(300, 70), size=size_annotation)
ax1.annotate('Yaw {{{}}}'.format(r"$\gamma_{23}$"), xy=(300, -110), size=size_annotation)
# ax1.legend(prop={'size': size_legend})

ax2.set_ylabel('deg')
ax2.set_xlabel('Iterations')
for i in [7]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float
    data2 = data2[zoom_range_start:zoom_range_end]

    ax2.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=1.3*sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linestyle=None, marker='.')
    ax2.plot(range(zoom_range_start, zoom_range_end), data1, label = 'GA-LMS', linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax2.plot(range(zoom_range_start, zoom_range_end), data2, label = 'LMS', linestyle='--', color='black', linewidth=linewidth)
ax2.annotate('Angle_Of_Attack {{{}}}'.format(r"$\gamma_{123}$"), xy=(375, 69), size=size_annotation)
ax2.legend(prop={'size': size_legend}, loc='lower left')
# ax2.legend(custom_lines, ['predicted'], loc='upper right')
# fig.set_size_inches(width, 0.7*height)
# fig.set_size_inches(0.95*height*height/width, height)
fig.set_size_inches(0.35*width, height)
plt.tight_layout()
# plt.subplots_adjust(wspace=0.4)
pp.savefig()
plt.close()

# Zoomed-in figures 3
zoom_range_start = 1000
zoom_range_end = 1200
fig, [ax1, ax2] = plt.subplots(2, 1)
ax1.set_ylabel('deg')
# ax1.set_xlabel('Iterations')
for i in range(4, 7):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float
    data2 = data2[zoom_range_start:zoom_range_end]

    ax1.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=0.5*sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    ax1.plot(range(zoom_range_start, zoom_range_end), data1, label = 'GA-LMS', linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax1.plot(range(zoom_range_start, zoom_range_end), data2, label = 'LMS', linestyle='--', color='black', linewidth=linewidth)
ax1.legend(custom_lines, ['predicted'], loc=(0.6, 0.75))
ax1.annotate('Roll {{{}}}'.format(r"$\gamma_{12}$"), xy=(300, 200), size=size_annotation)
ax1.annotate('Pitch {{{}}}'.format(r"$\gamma_{31}$"), xy=(300, 70), size=size_annotation)
ax1.annotate('Yaw {{{}}}'.format(r"$\gamma_{23}$"), xy=(300, -110), size=size_annotation)
# ax1.legend(prop={'size': size_legend})

ax2.set_ylabel('deg')
ax2.set_xlabel('Iterations')
for i in [7]:
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    data1 = data1[zoom_range_start:zoom_range_end]

    f2 = open('y_galms_real_{}.out'.format(blades[i]), 'r')
    data2_list = []
    for line in f2:
        data2_list.append(line.rstrip('\n'))
    data2 = [float(j) for j in data2_list] # Converts to float
    data2 = data2[zoom_range_start:zoom_range_end]

    ax2.scatter(range(zoom_range_start, zoom_range_end), df[dic[blades[i]]].values[zoom_range_start:zoom_range_end], label = 'Actual'.format(dic[blades[i]]), color=colors[i], s=1.3*sizedot)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linestyle=None, marker='.')
    ax2.plot(range(zoom_range_start, zoom_range_end), data1, label = 'GA-LMS', linestyle='--', color='magenta', linewidth=linewidth)
    if plot_LMSs:
        ax2.plot(range(zoom_range_start, zoom_range_end), data2, label = 'LMS', linestyle='--', color='black', linewidth=linewidth)
ax2.annotate('Angle_Of_Attack {{{}}}'.format(r"$\gamma_{123}$"), xy=(375, 69), size=size_annotation)
ax2.legend(prop={'size': size_legend}, loc='lower left')
# ax2.legend(custom_lines, ['predicted'], loc='upper right')
# fig.set_size_inches(width, 0.7*height)
# fig.set_size_inches(0.95*height*height/width, height)
fig.set_size_inches(0.35*width, height)
plt.tight_layout()
# plt.subplots_adjust(wspace=0.4)
pp.savefig()
plt.close()

pp.close()
