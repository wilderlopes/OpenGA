# Script to call the GAAFs binaries.
#
# Author: Wilder Lopes - wil@openga.org
# www.openga.org
# Dec 2015
#
# The following Python 2.7 script calls the GA-LMS (standard) binary to perform a system identification task.
#
# In this example, the multivectors samples belong to the Geometric Algebra of $\mathbb{R}^3$.
# Thus, each regressor and weight vector entry has 8 coefficients, i.e., for each entry of
# the weight vector, 8 coefficients have to be estimated. This constrasts with the usal LMS
# which only estimates real/complex entries. For further information, please refer to the
# GA documentation at www.openga.org.
#
# At the end, the learning curves Mean-Square Error (MSE) and/or Excess Mean-Square Error (EMSE) are plotted.

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

M       = 5 # System order
L       = 100 # Realizations
N       = 3000 # Time iterations
mu      = 0.005 # AF Step size
sigma2v = 1e-3 # Variance of measurement noise
sigma2q = 0 # Variance of random-walk noise
corr_input = 0.95 # Level of correlation between input's entries.
BINARY  = 'GA-LMS' # Note that you can call any of the following binaries:
		   # GA-LMS --> Complete subalgebra of R^3
		   # GA-LMS_rotors --> Even subalgebra of R^3 (isomorphic to quaternions)
		   # GA-LMS_complex --> Even subalgebra of R^2 (isomorphic to complex numbers)
		   # GA-LMS_real --> Even subalgebra of R (isomorphic to the real numbers)
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

plt.title('EMSE curves - {}, mu={}, sigma2v={}, sigma2q={}, corr_input={}'.format(BINARY,
          mu, sigma2v, sigma2q, corr_input), fontsize=9)
plt.ylabel('EMSE (dB)')
plt.xlabel('Iterations')
plt.plot(data1_dB, label = 'EMSE_galms', color = 'r')
plt.plot(data2_dB, label = 'EMSE_theory', color = 'magenta')
plt.legend()
#plt.savefig('EMSE.png', bbox_inches='tight')
pp.savefig()
#plt.show()

plt.close()
pp.close()
