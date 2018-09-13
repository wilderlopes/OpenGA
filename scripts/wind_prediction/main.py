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

savefolder = './Figures/'
if not os.path.exists(savefolder):
    os.makedirs(savefolder)
