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
                              of the GAAFs. The GAALET C++ (https://sourceforge.net/projects/gaalet/)
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
To get started with OpenGA, visit the website: https://openga.org/getstarted.html

Please let us know if you need help running the algorithms: info@openga.org

By Wil Lopes - wil@openga.org
