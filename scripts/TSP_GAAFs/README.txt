Complementary material for submission to Transaction on Signal Processing:
"Geometric-Algebra Adaptive Filters", Lopes, W.B. and Lopes, C.G.

Code author: Wilder Lopes - wil@openga.org
www.openga.org
Feb 2018

===================================
INSTRUCTIONS TO RUN THE SIMULATIONS

To avoid having to install the dependencies by yourself, it is strongly
recommended to use the Docker image of OpenGA. This image is a like a Linux
virtual machine that contains all the binaries compiled from C++ codes, all the
Python/Matlab scripts, and all the dependencies.

To install Docker in your machine (Linux, Windows, or Mac), please follow the
instructions on OpenGA website: http://openga.org/getstarted.html

Once the OpenGA Docker image is running, navigate to "OpenGA/scripts/TSP_GAAFs".
There you should find this README.txt document and a folder called "python",
which contains the Python script to be run. Go inside it and execute (note that
to run the code for this submission you should use Python 3.0 or above. If your
Python version is already 3.0 or above, you probably only need to call 'python'
instead of 'python3' below):

$ python3 TSP_gaafs.py

This should run for a while (it could take up to 5 min).
At the end, the figures will be saved in a folder called "Figures".

If you have any trouble running the sims, or if you have suggestions to improve
OpenGA, please do not hesitate to contact me (Wilder Lopes) at wil@openga.org.
