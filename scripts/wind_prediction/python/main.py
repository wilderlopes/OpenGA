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

custom_lines = [Line2D([0], [0], color='magenta', linestyle='--', lw=2)]

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

df = pd.read_csv('/home/openga/data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS.csv')
colors = ['orange', 'blue', 'green', 'black']
blades = [0, 3, 5, 6]
# blades = []
cols = constants.COLS_FOR_SIM
dic = dict(zip(blades, cols))

# plt.figure(figsize=(13.69,8.27))
plt.figure(figsize=(6, 3.5))
# plt.figure()
# plt.title('y curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
#           mu, sigma2v, sigma2q, corr_input), fontsize=9)
plt.ylabel('mbar')
plt.xlabel('Iterations')
for i in range(1):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    # data_label1 = ['y_galms_{}'.format(blades[i])]
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    plt.scatter(range(len(data1)), df[dic[blades[i]]].values[:len(data1)], label = 'actual_{}'.format(dic[blades[i]]), color=colors[i], s=3)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linewidth=3)
    plt.plot(data1[3:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=1.5)
plt.legend(loc='upper left')
# plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#            ncol=2, mode="expand", borderaxespad=0.)
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#plt.savefig('EMSE.png', bbox_inches='tight')
pp.savefig()
plt.close()


plt.figure(figsize=(6, 4.0))
# plt.figure()
# plt.title('y curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
#           mu, sigma2v, sigma2q, corr_input), fontsize=9)
plt.ylabel('m/s')
plt.xlabel('Iterations')
for i in range(1, len(blades)):
    f1 = open('y_galms_{}.out'.format(blades[i]), 'r')
    # data_label1 = ['y_galms_{}'.format(blades[i])]
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))
    data1 = [float(j) for j in data1_list] # Converts to float
    plt.scatter(range(len(data1)), df[dic[blades[i]]].values[:len(data1)], label = 'actual_{}'.format(dic[blades[i]]), color=colors[i], s=3)
    # plt.plot(df[dic[blades[i]]].values[:len(data1)], label = 'y_galms_{}_{}'.format(blades[i], dic[blades[i]]), color=colors[i], linestyle=None, marker='.')
    plt.plot(data1[3:], label = 'predicted_{}'.format(dic[blades[i]]), linestyle='--', color='magenta', linewidth=1.5)

plt.annotate('V', xy=(50, 1400))
plt.annotate('U', xy=(50, 900))
plt.annotate('W', xy=(50, 300))
plt.legend(custom_lines, ['predicted'], loc=2)
# plt.legend(custom_lines, ['actual_{}'.format(col) for col in cols[1:]] + ['pred'], loc=(0.6, 0.3))
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# plt.legend(custom_lines, ['actual_{}'.format(col) for col in cols[1:]], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#            ncol=2, mode="expand", borderaxespad=0.)
#plt.savefig('EMSE.png', bbox_inches='tight')
pp.savefig()
plt.close()
pp.close()
