# OpenGA

Please visit www.openga.org

## About 
Open-source Geometric Algebra (OpenGA) is a hub for tools and algorithms devised in light of Geometric Algebra (GA) (also known as Clifford Algebra). GA encompasses many of the standard algebraic systems used for describing geometric transformations, e.g., linear/matrix algebra, complex algebra, quaternions etc. GA-based algorithms benefit from the intrinsic mathematical generality of GA. In the core of OpenGA algorithms reside open-source libraries/toolboxes like GABLE (Geometric AlgeBra Learning Environment) and GAALET (Geometric Algebra ALgorithms Expression Templates) by Florian Seybold (https://sourceforge.net/projects/gaalet/). OpenGA is for researchers, engineers, and developers willing to apply GA in their projects. 

## Applications
OpenGA currently provides two applications of GA-based algorithms. The first one is adaptive filtering (one of the building blocks of machine learning and artificial intelligence); the second is 3D registration/alignment of Point Clouds. Since GA is as a lingua franca, allowing to connect different mathematical languages, we believe there are many other applications out there waiting to be reformulated from a GA perspective. OpenGA may be the starting point to achieve that. 

## Collaboration
OpenGA started with researchers working on computer vision problems. However, the capabilities of GA may be useful in other applications. We welcome the help of researchers, engineers, and developers from other areas of knowledge to improve OpenGA codes. If you are willing to contribute to this project, please contact us. 

## Getting started 
There are two ways to get started with OpenGA. It is up to you to chose either one. However, we recommend to use the OpenGA Docker image, which contains all the necessary stuff to run the scripts. Moreover, the Docker option allows for running OpenGA in several operating systems (Linux, Windows, Mac OS).

[Jupyter Notebooks]

Simply download the files from GitHub (or clone the repository) and run the examples. There are examples for Python and MATLAB. Note that those are provided as Jupyter Notebooks, which should be previously installed in your computer (https://jupyter.readthedocs.io/en/latest/install.html).

Besides that, the following linux packages should also be installed:   
    libboost-system1.54-dev 
    python
    python-matplotlib

[Docker Image] --- Recommended

Python notebooks are great. However, as pointed out above, before running the tutorials one still needs to install the dependencies (libraries). Thus, to get a head-start on using OpenGA, a Docker image (based on Ubuntu 14.04 LTS) was created. A Docker image is a stripped-to-the-bare-bones linux image. Just install Docker in your machine (it is multiplatform, i.e., Linux, Windows, and Mac), download and run the OpenGA image (instructions here). As a result, it is going to create a container (which is similar to a virtual machine) inside your host system with all the necessary elements: tools, libraries, and source code.

IMPORTANT: at this moment, only the standard GAAFs are available with the Docker image. For the pose-estimation GAAFs, please go to the GitHub repository. 

By Wil Lopes - wil@openga.org
