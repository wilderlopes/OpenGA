README file

ALTERNATIVELY, THIS SUPPLEMENTARY MATERIAL IS ALSO AVAILABLE AT |====> www.lps.usp.br/wilder
 
Supplementary material for IEEE Signal Processing Letters submission: "Geometric-Algebra LMS Adaptive Filter and its Application to Rotation Estimation", 
Authors: Wilder Lopes (wilder@usp.br), Anas Al-Nuaimi
(anas.alnuaimi@tum.de), Cassio Lopes (cassio@lps.usp.br)

Matlab and C++ code by:
Wilder Bezerra Lopes - Ph.D. Student 
University of Sao Paulo (USP) / Technische Universitaet Muenchen (TUM)
October 2015
www.lps.usp.br/wilder
wilderlopes@gmail.com
 
==============================================================
The content provided by the authors (size 13MB) in this package is:
	- An .avi video showing the adaptation of the sets (cube and bunny).
	- MATLAB and C++ codes, and datasets to reproduce the curves shown in the paper.  

To reproduce the simulations, it is necessary a copy of MATLAB (The MathWorks Inc.). The tests were made using the Release 2013a. However, it should run on older versions as well (it may require some modifications in the code). 

The codes in this supplementary material are distributed with The MIT License (MIT) -- Please check the end of the document for details.
==============================================================

Directory structure:

SPL_SupMat|------|Simulations
          |             |------|Bunny
          |             |         |------PCD_registration_bunny.m
          |             |         | 
          |             |         |
          |             |         
          |             |------|Cube
          |             |         |------PCD_registration_cube.m
          |             |         |
          |             |         |
          |             |             
          |             |------|Scripts
          |                       |------|Cpp
          |                       |         |GA-LMS_bunny
	  |                       |         |        
          |                       |         |GA-LMS_cube
          |                       |         
          |                       |
          |                       |------|pclviewer
          |                       |            
          |   
          |------ video.avi
          |------ README.txt

==============================================================
VIDEO
==============================================================
The .avi video shows the alignment for both sets. It is a visual example of the iterative process to estimate the best rotor. Comments in subtitles provide details on the algorithm.     


==============================================================
SIMULATIONS 
==============================================================

Everything you need to simulate (except the MATLAB software, of course) is contained in the 'Simulations' folder. Inside each set folder (bunny and cube), you will find the respective main scripts: 'PCD_registration_bunny.m' and 'PCD_registration_cube.m'

In the 'Scripts' folder are stored all the function called by the main scripts. Also, a copy of the PCLVIEWER toolkit by Peter I. Corke is provided (http://www.mathworks.com/matlabcentral/fileexchange/40382-matlab-to-point-cloud-library), which is necessary to load and save Point Clouds format (.pcd). 

IMPORTANT: Add the folder 'SPL_SupMat' (and all its subfolders) to the path of MATLAB. Once MATLAB is open, navigate to the directory where you unpacked the folder. Then click with the right button on top of 'SPL_SupMat' and select the option 'Add to path - selected folders and subfolders'. Further instructions on how to do this can be found here (http://de.mathworks.com/help/matlab/ref/addpath.html). The simulations won't work if the folder and its contents are not added to the MATLAB path.


---> Cube set
	
We provide the following set of source and target PCDs:
	'Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0'	

First open the 'PCD_registration_cube.m' script. Remember to modify the path to SPL_SupMat folder (on the top of the code):

%============= Type in the path for the extracted folder 'SPL_SupMat' =====
user_folder = 'write_path_to_folder_here/SPL_SupMat';
%==========================================================================

Then navigate to the folder above ('Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0') and run the script from inside that folder. The code will run L=200 realizations (experiments) for each pair {sigma2v, mu}. The amount of realizations, the values for the step size (mu), and the measurement noise (sigma2v) can be redefined by the user at the top of the code. The default values are the ones used for the simulations in the paper.

By the end of the 1728 iterations, the learning curves, the misaligned PCDs, and the aligned PCDs are plotted and saved in their respective folders. You can check the results in the folder 'Results_realizations', created automatically. The figures are saved in .fig and .pdf formats, and the output variables in the file simData.mat. To visualize the figures, go inside its folder and type the following commands in Matlab Command Window:

openfig('Figure_MSE.fig','new','visible') % Opens the MSE figure 
openfig('Figure_EMSE.fig','new','visible') % Opens the EMSE figure 
openfig('Figure_misaligned_PCDs.fig','new','visible') % Opens the Misaligned_PCDs figure
openfig('Figure_aligned_PCDs.fig','new','visible') % Opens the Aligned_PCDs figure


---> Bunny set
	
Inside MATLAB, go to the 'Bunny' folder and run 'PCD_registration_bunny.m'. Remember to modify the path to SPL_SupMat folder (on the top of the code):

%============= Type in the path for the extracted folder 'SPL_SupMat' =====
user_folder = 'write_path_to_folder_here/SPL_SupMat';
%==========================================================================


You should see the message 'Bunny registration using GA-LMS' and the iterations start counting. When i=245, the simulation finishes and returns the plots, which are saved in the folder 'Results_realizations', created automatically. The figures are saved in .fig and .pdf formats, and the output variables in the file simData.mat. To visualize the figures, go inside its folder and type the following commands in Matlab Command Window:

openfig('Figure_MSE_and_CF.fig','new','visible') % Opens the MSE_and_CF figure
openfig('Figure_misaligned_PCDs.fig','new','visible') % Opens the Misaligned_PCDs figure
openfig('Figure_aligned_PCDs.fig','new','visible') % Opens the Aligned_PCDs figure

GOOD CORRESPONDENCES -> As pointed out in the paper, we use only the good correspondences, i.e. outlier-free correspondences, stored in the file 'good_correspondences.txt', to plot the cost function (CF) curve. This is done in order to obtain a CF learning curve free of outliers, what would naturally happen if the point matching in [31] was perfect. This way, we can see how the rotors provided by the GA-LMS align the true (good) correspondences.      

There are specialized tools to visualize point clouds available from the internet. One can load the provided PCDs in a software like the open source CloudCompare (http://www.danielgm.net/cc/) and apply the transformation T_galms to the sourceKps.pcd to align them. However, the MATLAB scatter plots suffice the purposes of this material.  

The value obtained for the SVD is also shown in the command window at the end of the simulation.   

 
==============================================================

The MIT License (MIT)
 
Copyright (c) 2015 onwards, by Wilder Lopes
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE. 


