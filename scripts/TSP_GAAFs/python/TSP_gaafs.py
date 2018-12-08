# Complementary material for submission to Transaction on Signal Processing
#
# Author: Wilder Lopes - wil@openga.org
# www.openga.org
# Feb 2018
#
# The following Python 3.0 (or above) script calls the GA-LMS (standard) binary to perform a system identification task.
#
# In the examples below, the multivectors samples belong to the Geometric Algebra of $\mathbb{R}^3$.
# Thus, each regressor and weight vector entry has 8 coefficients, i.e., for each entry of
# the weight vector, 8 coefficients have to be estimated. This constrasts with the usal LMS
# which only estimates real/complex entries. For further information, please refer to the
# GA documentation at www.openga.org.
#
# At the end, Fig. 5 (Top, Middle, and Bottom) and Fig. 6 of the submission
# are generated and saved in the folder "Figures".
#
#
# The MIT License (MIT)
#
# Copyright (c) 2016 onwards, by Wilder Lopes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Start by importing the necessary Python modules:
import sys, string, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from math import log
from matplotlib.backends.backend_pdf import PdfPages

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

width  = 6 #3.487
height = width / 1.618
size_annotation = 10
size_annotation_zoom = 7
size_legend = 8
sizedot = 5
linewidth = 2

savefolder = './Figures/'
if not os.path.exists(savefolder):
    os.makedirs(savefolder)

# ###########################################
# ### Simulations to produce Fig. 5 (Top) ###
# ###########################################
# print('### Experiments for Fig 5 (Top) ###')
# pp = PdfPages(savefolder + '/TSP_GAAFs_Fig_5_Top.pdf') # multipage pdf to save figures
#
# M       = 10 # System order
# L       = 100 # Realizations
# N       = 1000 # Time iterations
# mu      = 0.01 # AF Step size
# sigma2v = [1e-2, 1e-3, 1e-5] # Variance of measurement noise
# sigma2q = 0 # Variance of random-walk noise
# corr_input = 0 # Level of correlation between input's entries.
# BINARY  = 'GA-LMS' # Note that you can call any of the following binaries:
# 		   # GA-LMS --> Complete subalgebra of R^3
# 		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
# 		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
# 		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
# #====================================================
#
# data_dic = {}
# for sig in sigma2v:
#     # The binary is called below using the previously set parameters. The GA-LMS runs and returns .txt files with the results: *_galms.out and *_theory.out, where * represents "MSE" or "EMSE". *_galms.out files store the ensemble-average learning curves (EMSE), while *_theory.out files store the theoretical steady-state value for MSE and EMSE.
#
#     # Calling binary
#     arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(mu)+ " " + str(sig) + " " + str(sigma2q) + " " + str(corr_input)
#     print('> Calling binary with the following parameters: \n {}'.format(arguments))
#     os.popen("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments).read()
#
#     # Load files EMSE_galms.out and EMSE_theory.out (generated by the binary) to plot
#     # EMSE learning curve and theoretical curve:
#     f1 = open('EMSE_galms.out', 'r')
#     data_label1 = ['EMSE_galms']
#     data1_list = []
#     for line in f1:
#         data1_list.append(line.rstrip('\n'))
#
#     f2 = open('EMSE_theory.out', 'r')
#     data_label2 = ['EMSE_theory']
#     data2_list = []
#     for line in f2:
#         for i in range(len(data1_list)):
#             data2_list.append(line.rstrip('\n'))
#
#     data1 = [float(j) for j in data1_list] # Converts to float
#     data2 = [float(j) for j in data2_list] # Converts to float
#     data1_dB = [10*log(x,10) for x in data1]
#     data2_dB = [10*log(x,10) for x in data2]
#
#     data_dic.update({'{}'.format(sig) : [data1_dB, data2_dB]})
#
# # Plot figures
# plt.title('EMSE curves - ' + BINARY + ' ' + r"$\mu={}, M={}$".format(mu, M))
# plt.ylabel('EMSE (dB)')
# plt.xlabel('Iterations')
# for key in data_dic.keys():
#     plt.plot(data_dic[key][1], label = r'$\sigma^2_v={}$ (theory)'.format(key), color = 'magenta', linestyle = '--')
#     plt.plot(data_dic[key][0], label = r'$\sigma^2_v={}$'.format(key), color = 'b')
#
# plt.legend(loc="best")
# #plt.savefig('EMSE.png', bbox_inches='tight')
# pp.savefig()
# #plt.show()
# plt.close()
# pp.close()



# ##############################################
# ### Simulations to produce Fig. 5 (Middle) ###
# ##############################################
# print('### Experiments for Fig 5 (Middle) ###')
# pp = PdfPages(savefolder + 'TSP_GAAFs_Fig_5_Middle.pdf') # multipage pdf to save figures
#
# M       = 10 # System order
# L       = 100 # Realizations
# N       = 1000 # Time iterations
# mu      = [0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.0225] # AF Step size
# sigma2v = [1e-2, 1e-3, 1e-5] # Variance of measurement noise
# sigma2q = 0 # Variance of random-walk noise
# corr_input = 0.95 # Level of correlation between input's entries.
# BINARY  = 'GA-LMS' # Note that you can call any of the following binaries:
# 		   # GA-LMS --> Complete subalgebra of R^3
# 		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
# 		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
# 		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
# #====================================================
#
# # Number of points to average the EMSE:
# avgpoints = 200
#
# data_dic = {}
# for sig in sigma2v:
#     data1_dB = []
#     data2_dB = []
#     for step in mu:
#
#         # Calling binary
#         arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(step)+ " " + str(sig)  + " " + str(sigma2q) + " " + str(corr_input)
#         print('> Calling binary with the following parameters: \n {}'.format(arguments))
#         os.popen("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments).read()
#
#         # Load files EMSE_galms.out and EMSE_theory.out (generated by the binary) to plot
#         # EMSE learning curve and theoretical curve:
#         f1 = open('EMSE_galms.out', 'r')
#         data_label1 = ['EMSE_galms']
#         data1_list = []
#         for line in f1:
#             data1_list.append(line.rstrip('\n'))
#
#         f2 = open('EMSE_theory.out', 'r')
#         data_label2 = ['EMSE_theory']
#         data2_list = []
#         for line in f2:
#             for i in range(len(data1_list)):
#                 data2_list.append(line.rstrip('\n'))
#
#         data1 = [float(j) for j in data1_list] # Converts to float
#         data2 = [float(j) for j in data2_list] # Converts to float
#
#         data1_dB.append(10*log(np.mean(data1[-avgpoints:]),10))
#         try:
#             data2_dB.append(10*log(data2[0],10))
#         except:
#             data2_dB.append(np.nan)
#
#     data_dic.update({'{}'.format(sig) : [data1_dB, data2_dB]})
#
# # Plot figures
# plt.title('EMSE curves - ' + BINARY + ' ' + r"$M={}$".format(M))
# plt.ylabel('EMSE (dB)')
# plt.xlabel('Step size')
# for key in data_dic.keys():
#     plt.plot(mu, data_dic[key][1], label = r'$\sigma^2_v={}$ (theory)'.format(key), color = 'magenta', linestyle = '--', marker='o')
#     plt.plot(mu, data_dic[key][0], label = r'$\sigma^2_v={}$'.format(key), color = 'black', marker='x')
#
# plt.legend(loc="best")
# #plt.savefig('EMSE.png', bbox_inches='tight')
# pp.savefig()
# #plt.show()
# plt.close()
# pp.close()
#
#
# ##############################################
# ### Simulations to produce Fig. 5 (Bottom) ###
# ##############################################
# print('### Experiments for Fig 5 (Bottom) ###')
# pp = PdfPages(savefolder + 'TSP_GAAFs_Fig_5_Bottom.pdf') # multipage pdf to save figures
#
# M       = [x for x in range(24,25)] # System order
# L       = 100 # Realizations
# N       = 1000 # Time iterations
# mu      = 0.01 # AF Step size
# sigma2v = [1e-2, 1e-3, 1e-5] # Variance of measurement noise
# sigma2q = 0 # Variance of random-walk noise
# corr_input = 0.95 # Level of correlation between input's entries.
# BINARY  = 'GA-LMS' # Note that you can call any of the following binaries:
# 		   # GA-LMS --> Complete subalgebra of R^3
# 		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
# 		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
# 		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
# #====================================================
#
# # Number of points to average the EMSE:
# avgpoints = 200
#
# data_dic = {}
# for sig in sigma2v:
#     data1_dB = []
#     data2_dB = []
#     for order in M:
#
#         # Calling binary
#         arguments = " " + str(order) + " " + str(L) + " " + str(N) + " " + str(mu)+ " " + str(sig)  + " " + str(sigma2q) + " " + str(corr_input)
#         print('> Calling binary with the following parameters: \n {}'.format(arguments))
#         os.popen("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments).read()
#
#         # Load files EMSE_galms.out and EMSE_theory.out (generated by the binary) to plot
#         # EMSE learning curve and theoretical curve:
#         f1 = open('EMSE_galms.out', 'r')
#         data_label1 = ['EMSE_galms']
#         data1_list = []
#         for line in f1:
#             data1_list.append(line.rstrip('\n'))
#
#         f2 = open('EMSE_theory.out', 'r')
#         data_label2 = ['EMSE_theory']
#         data2_list = []
#         for line in f2:
#             for i in range(len(data1_list)):
#                 data2_list.append(line.rstrip('\n'))
#
#         data1 = [float(j) for j in data1_list] # Converts to float
#         data2 = [float(j) for j in data2_list] # Converts to float
#
#         data1_dB.append(10*log(np.mean(data1[-avgpoints:]),10))
#         try:
#             data2_dB.append(10*log(data2[0],10))
#         except:
#             data2_dB.append(np.nan)
#
#     data_dic.update({'{}'.format(sig) : [data1_dB, data2_dB]})
#
# # Plot figures
# plt.title('EMSE curves - ' + BINARY + ' ' + r"$\mu={}$".format(mu))
# plt.ylabel('EMSE (dB)')
# plt.xlabel('System Order M (Taps)')
# for key in data_dic.keys():
#     plt.plot(M, data_dic[key][1], label = r'$\sigma^2_v={}$ (theory)'.format(key), color = 'magenta', linestyle = '--', marker='o')
#     plt.plot(M, data_dic[key][0], label = r'$\sigma^2_v={}$'.format(key), color = 'black', marker='x')
#
# plt.legend(loc="best")
# #plt.savefig('EMSE.png', bbox_inches='tight')
# pp.savefig()
# #plt.show()
# plt.close()
# pp.close()


############################################################################
### Simulations to produce Fig. 5 (Top) Correlated Input and Random Walk ###
############################################################################
print('### Experiments for Fig 5 (Top) Correlated and Random Walk ###')
pp = PdfPages(savefolder + '/TSP_GAAFs_Fig_5_Top_correlated_randomwalk.pdf') # multipage pdf to save figures

M       = 10 # System order
L       = 100 # Realizations
N       = 5000 # Time iterations
mu      = 0.01 # AF Step size
sigma2v = [1e-2, 1e-3, 1e-5] # Variance of measurement noise
sigma2q = 0 # Variance of random-walk noise
corr_input = 0.98 # Level of correlation between input's entries.
BINARY  = 'GA-LMS' # Note that you can call any of the following binaries:
		   # GA-LMS --> Complete subalgebra of R^3
		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
#====================================================

data_dic = {}
for sig in sigma2v:
    # The binary is called below using the previously set parameters. The GA-LMS runs and returns .txt files with the results: *_galms.out and *_theory.out, where * represents "MSE" or "EMSE". *_galms.out files store the ensemble-average learning curves (EMSE), while *_theory.out files store the theoretical steady-state value for MSE and EMSE.

    # Calling binary
    arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(mu)+ " " + str(sig) + " " + str(sigma2q) + " " + str(corr_input)
    print('> Calling binary with the following parameters: \n {}'.format(arguments))
    os.popen("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments).read()

    # Load files EMSE_galms.out and EMSE_theory.out (generated by the binary) to plot
    # EMSE learning curve and theoretical curve:
    f1 = open('EMSE_galms.out', 'r')
    data_label1 = ['EMSE_galms']
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))

    f2 = open('EMSE_theory.out', 'r')
    data_label2 = ['EMSE_theory']
    data2_list = []
    for line in f2:
        for i in range(len(data1_list)):
            data2_list.append(line.rstrip('\n'))

    data1 = [float(j) for j in data1_list] # Converts to float
    data2 = [float(j) for j in data2_list] # Converts to float
    data1_dB = [10*log(x,10) for x in data1]
    data2_dB = [10*log(x,10) for x in data2]

    data_dic.update({'{}'.format(sig) : [data1_dB, data2_dB]})

# Plot figures
# colors = ['blue', 'green', 'black']
cmap = plt.cm.RdYlBu
colors = []
for i in np.linspace(0.8, 1, 3):
    colors.append(cmap(i))
y_annotation = [-5, -28, -36]
x_start = 0
x_end = N
y_start = -50
y_end = 40
fig, [ax1, ax2] = plt.subplots(2, 1, sharex=True)
# plt.title('EMSE curves - ' + BINARY + ' ' + r"$\mu={}, M={}$".format(mu, M))
ax1.set_ylabel('EMSE (dB)')
# ax1.set_xlabel('Iterations')
data_dic_keys = data_dic.keys()
dic_sigma2v = dict(zip(data_dic_keys, [r'$\sigma^2_v=10^{-2}$', r'$\sigma^2_v=10^{-3}$', r'$\sigma^2_v=10^{-5}$']))
for i in range(len(data_dic_keys)):
    key = data_dic_keys[i]
    # ax1.plot(data_dic[key][1], label = r'$\sigma^2_v={}$ (theory)'.format(key), color = 'magenta', linestyle = '--')
    ax1.plot(data_dic[key][0], label = "{}".format(dic_sigma2v[key]), color = colors[i], linewidth=linewidth)
    # ax1.annotate("{}".format(dic_sigma2v[key]), xy=(2600, y_annotation[i]), size=size_annotation)
ax1.annotate("b = {}".format(corr_input), xy=(500, 29), size=size_annotation)
ax1.annotate(r"$\sigma^2_q = {}$".format(sigma2q), xy=(500, 13), size=size_annotation)
ax1.annotate("{:.2f} dB".format(data_dic[key][0][-1]), xy=(4990, data_dic[key][0][-1]), xytext=(3200, data_dic[key][0][-1] + 10), arrowprops=dict(facecolor='red', color='red', width=1, headwidth=4, shrink=0.05), size=size_annotation)
ax1.legend(loc="upper right", prop={'size': size_legend})
ax1.set_xlim([x_start, x_end])
ax1.set_ylim([y_start, y_end])


sigma2q = 4e-6 # Variance of random-walk noise
corr_input = 0.98 # Level of correlation between input's entries.
BINARY  = 'GA-LMS' # Note that you can call any of the following binaries:
		   # GA-LMS --> Complete subalgebra of R^3
		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
#====================================================

data_dic = {}
for sig in sigma2v:
    # The binary is called below using the previously set parameters. The GA-LMS runs and returns .txt files with the results: *_galms.out and *_theory.out, where * represents "MSE" or "EMSE". *_galms.out files store the ensemble-average learning curves (EMSE), while *_theory.out files store the theoretical steady-state value for MSE and EMSE.

    # Calling binary
    arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(mu)+ " " + str(sig) + " " + str(sigma2q) + " " + str(corr_input)
    print('> Calling binary with the following parameters: \n {}'.format(arguments))
    os.popen("../../../src/GAAFs_standard/" + BINARY + "/build/" + BINARY + arguments).read()

    # Load files EMSE_galms.out and EMSE_theory.out (generated by the binary) to plot
    # EMSE learning curve and theoretical curve:
    f1 = open('EMSE_galms.out', 'r')
    data_label1 = ['EMSE_galms']
    data1_list = []
    for line in f1:
        data1_list.append(line.rstrip('\n'))

    f2 = open('EMSE_theory.out', 'r')
    data_label2 = ['EMSE_theory']
    data2_list = []
    for line in f2:
        for i in range(len(data1_list)):
            data2_list.append(line.rstrip('\n'))

    data1 = [float(j) for j in data1_list] # Converts to float
    data2 = [float(j) for j in data2_list] # Converts to float
    data1_dB = [10*log(x,10) for x in data1]
    data2_dB = [10*log(x,10) for x in data2]

    data_dic.update({'{}'.format(sig) : [data1_dB, data2_dB]})


ax2.set_ylabel('EMSE (dB)')
ax2.set_xlabel('Iterations')
data_dic_keys = data_dic.keys()
dic_sigma2v = dict(zip(data_dic_keys, [r'$\sigma^2_v=10^{-2}$', r'$\sigma^2_v=10^{-3}$', r'$\sigma^2_v=10^{-5}$']))
for i in range(len(data_dic_keys)):
    key = data_dic_keys[i]
    # ax2.plot(data_dic[key][1], label = r'$\sigma^2_v={}$ (theory)'.format(key), color = 'magenta', linestyle = '--')
    ax2.plot(data_dic[key][0], label = "{}".format(dic_sigma2v[key]), color = colors[i], linewidth=linewidth)
    # ax2.annotate("{}".format(dic_sigma2v[key]), xy=(2600, y_annotation[i]), size=size_annotation)
ax2.annotate("b = {}".format(corr_input), xy=(500, 29), size=size_annotation)
ax2.annotate("{}".format(r'$\sigma^2_q = 4x10^{-6}$'), xy=(500, 13), size=size_annotation)
ax2.annotate("{:.2f} dB".format(data_dic[key][0][-1]), xy=(4990, data_dic[key][0][-1]), xytext=(3200, -35), arrowprops=dict(facecolor='red', color='red', width=1, headwidth=4, shrink=0.05), size=size_annotation)
# plt.legend(loc="best")
ax2.set_xlim([x_start, x_end])
ax2.set_ylim([y_start, y_end])
fig.set_size_inches(width, height)
#plt.savefig('EMSE.png', bbox_inches='tight')
pp.savefig()
#plt.show()
plt.close()
pp.close()





# ##############################################
# ###      Simulations to produce Fig. 6     ###
# ##############################################
# print('### Experiments for Fig 6 ###')
# pp = PdfPages(savefolder + 'TSP_GAAFs_Fig_6.pdf') # multipage pdf to save figures
#
# M       = 10 # System order
# L       = 100 # Realizations
# N       = 2000 # Time iterations
# mu      = 0.005 # AF Step size
# sigma2v = 1e-3 # Variance of measurement noise
# sigma2q = 0 # Variance of random-walk noise
# corr_input = 0.95 # Level of correlation between input's entries.
# BINARY  = ['GA-LMS_rotors', 'GA-LMS_complex', 'GA-LMS_real']
# 		   # GA-LMS --> Complete subalgebra of R^3
# 		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
# 		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
# 		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
# #====================================================
#
# # Number of points to average the EMSE:
# avgpoints = 200
#
# color_dic = {'GA-LMS_rotors' : 'blue',
#              'GA-LMS_complex' : 'green',
#              'GA-LMS_real' : 'black'}
# data_dic = {}
# for binary in BINARY:
#     data1_dB = []
#     data2_dB = []
#
#     # Calling binary
#     arguments = " " + str(M) + " " + str(L) + " " + str(N) + " " + str(mu)+ " " + str(sigma2v)  + " " + str(sigma2q) + " " + str(corr_input)
#     print('> Calling binary with the following parameters: \n {}'.format(arguments))
#     os.popen("../../../src/GAAFs_standard/" + binary + "/build/" + binary + arguments).read()
#
#     # Load files EMSE_galms.out and EMSE_theory.out (generated by the binary) to plot
#     # EMSE learning curve and theoretical curve:
#     f1 = open('EMSE_galms.out', 'r')
#     data_label1 = ['EMSE_galms']
#     data1_list = []
#     for line in f1:
#         data1_list.append(line.rstrip('\n'))
#
#     f2 = open('EMSE_theory.out', 'r')
#     data_label2 = ['EMSE_theory']
#     data2_list = []
#     for line in f2:
#         for i in range(len(data1_list)):
#             data2_list.append(line.rstrip('\n'))
#
#     data1 = [float(j) for j in data1_list] # Converts to float
#     data2 = [float(j) for j in data2_list] # Converts to float
#     data1_dB = [10*log(x,10) for x in data1]
#     data2_dB = [10*log(x,10) for x in data2]
#
#     data_dic.update({'{}'.format(binary) : [data1_dB, data2_dB]})
#
#
# # Plot figures
# plt.title('EMSE curves - ' + r"$M={}, \mu={}, \sigma^2_v={}$".format(M, mu, sigma2v))
# plt.ylabel('EMSE (dB)')
# plt.xlabel('Iterations')
# for key in data_dic.keys():
#     plt.plot(data_dic[key][0], label = '{}'.format(key), color = color_dic[key])
#     plt.plot(data_dic[key][1], label = '{} (theory)'.format(key), color = 'magenta', linestyle = '--')
#
# plt.legend(loc="best")
# #plt.savefig('EMSE.png', bbox_inches='tight')
# pp.savefig()
# #plt.show()
# plt.close()
# pp.close()
