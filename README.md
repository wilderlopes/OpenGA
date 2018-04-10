# OpenGA

Please visit www.openga.org

## About
Open-source Geometric Algebra (OpenGA) is a hub for tools and algorithms devised in light of Geometric Algebra (GA) (also known as Clifford Algebra). GA encompasses many of the standard algebraic systems used for describing geometric transformations, e.g., linear/matrix algebra, complex algebra, quaternions etc. GA-based algorithms benefit from the intrinsic mathematical generality of GA. In the core of OpenGA algorithms reside open-source libraries/toolboxes like GABLE (Geometric AlgeBra Learning Environment) and GAALET (Geometric Algebra ALgorithms Expression Templates) by Florian Seybold (https://sourceforge.net/projects/gaalet/). OpenGA is for researchers, engineers, and developers willing to apply GA in their projects.

## Applications
OpenGA currently provides two applications of GA-based algorithms. The first one is adaptive filtering (one of the building blocks of machine learning and artificial intelligence); the second is 3D registration/alignment of Point Clouds. Since GA is as a lingua franca, allowing to connect different mathematical languages, we believe there are many other applications out there waiting to be reformulated from a GA perspective. OpenGA may be the starting point to achieve that.

In this repository you can find the source codes and scripts (matlab and python)
for the Geometric-Algebra Adaptive Filters (GAAFs).

Here is a map of the directory structure:
<pre>
openga-----|
           src -------------> Here you can find the C++ source codes for the GAAFs and
                              compiled binaries.
           include ---------> A series of header files necessary for the compilation
                              of the GAAFs. The GAALET C++ (http://gaalet.sourceforge.net/)
                              library, created by Florian Seybold, is stored here.
           scripts ---------> Matlab and Python scripts to call the binaries and run simulations.
           tutorials -------> Some tutorials written in jupyter nootebook. They are useful
                              to learn step-by-step how to call the binaries and understand
                              the GAAFs behavior.
</pre>
All the codes and scripts are heavily commented in order to make it easier for the user to understand.
However, if you get in trouble, please send us an email: info@openga.org

## Collaboration
OpenGA started with researchers working on computer vision problems. However, the capabilities of GA may be useful in other applications. We welcome the help of researchers, engineers, and developers from other areas of knowledge to improve OpenGA codes. If you are willing to contribute to this project, please contact us.
There are two ways to get started with OpenGA. It is up to you to chose either one. However, we recommend to use the OpenGA Docker image, which contains all the necessary stuff to run the scripts. Moreover, the Docker option allows for running OpenGA in several operating systems (Linux, Windows, Mac OS).

## How to Run it

###[Jupyter Notebooks]

Simply download the files from GitHub (or clone the repository) and run the examples. There are examples for Python and MATLAB. Note that those are provided as Jupyter Notebooks, which should be previously installed in your computer (https://jupyter.readthedocs.io/en/latest/install.html).

Besides that, the following linux packages should also be installed:   
<pre>
    libboost-system1.54-dev

    python-matplotlib

    libplc --> http://pointclouds.org/downloads/linux.html
</pre>

###[Docker Image] --- Recommended

Python notebooks are great. However, as pointed out above, before running the tutorials one still needs to install the dependencies (libraries). Thus, to get a head-start on using OpenGA, a Docker image (based on Ubuntu 14.04 LTS) was created. A Docker image is a stripped-to-the-bare-bones linux image. Just install Docker in your machine (it is multiplatform, i.e., Linux, Windows, and Mac), download and run the OpenGA image (instructions here). As a result, it is going to create a container (which is similar to a virtual machine) inside your host system with all the necessary elements: tools, libraries, and source code.

IMPORTANT: at this moment, only the standard GAAFs are able to be run with the Docker image. The pose-estimation GAAFs are included in the
<a href="https://github.com/wilderlopes/OpenGA/tree/master/scripts/GAAFs_poseEstimation">
GitHub</a> repository files.   

Step-by-step to use the OpenGA image:
                  <br>
                  1 - <a target="_blank" href="https://github.com/wilderlopes/OpenGA">Download the GitHub files</a>
                  containing all the source codes and scripts, or clone the respository:
                  <pre>$ git clone https://github.com/wilderlopes/OpenGA.git</pre>
                  <br>
                  2 - Install Docker.
                  The procedure varies by operating system. Go <a target="_blank" href="https://docs.docker.com/linux/">
                  here for Linux</a> and <a target="_blank" href="https://www.docker.com/products/docker-toolbox">here for Windows
                  or Mac OS</a>.
                  <br>
                  3 - It is time to download the OpenGA Docker image. There are three ways of doing it:
                  Method A: Pull it from Docker Hub (<b>easiest and recommended</b>):
                      <pre>$ docker pull wilderlopes/openga</pre>

                  Method B: Download the OpenGA Docker image <a target="_blank" href="files/openga.tar">from here</a> (2.4 GB .tar file). After
                  the download, you can load it into your docker like so
                  <pre>$ docker load < openga.tar</pre>

                  Method C: Alternatively, you can build the image in your host system using the Dockerfile provided with the GitHub repository. See how to do it <a target="_blank" href="https://docs.docker.com/engine/reference/commandline/build/">here</a>
                  <br>
                  4 - Whatever is the alternative chosen above, you should now have the OpenGA Docker image available. To check it, run the following command (Linux users):
                  <pre>$ docker images</pre>
                  You should expect an output similar to
                  <pre>REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
wilderlopes/openga   latest              beb957393d05        About an hour ago   2.45GB</pre>
                  <br>
                  5 - It is time to run the image. Go inside the folder you downloaded (cloned) from the GitHub
                  <pre>$ cd openga</pre>
                  You will find the file "start.sh". Run it like
                  <pre>$ ./start.sh </pre>
                  This file runs the Docker image, creating a container. You will find yourself
                  inside the container, in the directory '/home/openga' (notice that the prompt changes, showing
                  the container ID -- it will be a different one for you). A welcome message is printed:
                  <pre>root@2095a07347a0:/home/openga# Welcome to OpenGA! Please have a look on the README file or access www.openga.org.</pre>
                  <br>
                  6 - Let's run a simulation to check if everything works as expected. Navigate to the python scripts directory:
                  <pre>root@2095a07347a0:/home/openga# cd scripts/GAAFs_standard/python/</pre>
                  There you find the python script 'gaafs.py', which you can run as
                  <pre>root@2095a07347a0:/home/openga/scripts/GAAFs_standard/python# python gaafs.py</pre>
                  It will run 100 realizations, each with 1000 iterations, of the GA-LMS (standard) in a
                  system identification task. The estimated and optimal multivectors are printed on the
                  terminal, and MSE and EMSE learning curves are saved in the file 'learningCurvesGA-LMS.pdf'
                  inside the working path. At the moment, the only way to change the coefficients of the plant to be identified (optimal weights)
                  is modifying the <a target="_blank" href="https://github.com/wilderlopes/OpenGA/tree/master/src/GAAFs_standard">
                  source codes</a> and rebuilding the binaries.
                  <br>
                  You can open the file 'learningCurvesGA-LMS.pdf' from your host computer (the container does not have a pdf reader). Go to
                  <pre>$ cd OpenGA/scripts/GAAFs_standard/python </pre>
                  There you will find the same 'learningCurvesGA-LMS.pdf' which you can open with
                  your pdf reader.

For more details, please visit openga.org.


By Wil Lopes - wil@openga.org
