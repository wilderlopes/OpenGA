import os
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages

savefolder = './Figures/'
if not os.path.exists(savefolder):
    os.makedirs(savefolder)

sourceKps = pickle.load(open("sourceKps.p", "rb"))
targetKps = pickle.load(open("targetKps.p", "rb"))
sourceKps_reg = pickle.load(open("sourceKps_reg.p", "rb"))

# Plot
pp = PdfPages(savefolder + 'before_bunny.pdf') # multipage pdf to save figures
fig_before = plt.figure()
ax = fig_before.add_subplot(111, projection='3d')
ax.set_title('Before registration')
ax.scatter(sourceKps['x'], sourceKps['y'], sourceKps['z'], color='blue', label='source')
ax.scatter(targetKps['x'], targetKps['y'], targetKps['z'], color='red', label='target')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
pp.savefig()
pp.close()

pp = PdfPages(savefolder + 'after_bunny.pdf') # multipage pdf to save figures
fig_after = plt.figure()
ax = fig_after.add_subplot(111, projection='3d')
ax.set_title('After registration')
ax.scatter(targetKps['x'], targetKps['y'], targetKps['z'], color='red', label='target')
ax.scatter(sourceKps_reg['x'], sourceKps_reg['y'], sourceKps_reg['z'], color='green', label='source_reg')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
pp.savefig()
pp.close()

# plt.show()
