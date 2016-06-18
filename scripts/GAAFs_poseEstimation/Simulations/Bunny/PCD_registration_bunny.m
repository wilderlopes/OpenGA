% PCD_registration.m - Script to register the Stanford bunny PCDs
% 
% Supplementary material for IEEE Signal Processing Letters submission:
% "Geometric-Algebra LMS Adaptive Filter and its Application to  
% Rotation Estimation", 
% Authors: Wilder Lopes (wilder@usp.br), Anas Al-Nuaimi
% (anas.alnuaimi@tum.de), Cassio Lopes (cassio@lps.usp.br)
%
% Matlab code by:
% Wilder Bezerra Lopes - Ph.D. Student 
% University of Sao Paulo (USP) / Technische Universitaet Muenchen (TUM)
% October 2015
% www.lps.usp.br/wilder
% wilderlopes@gmail.com

% The MIT License (MIT)
% 
% Copyright (c) 2015 onwards, by Wilder Lopes
% 
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
% 
% The above copyright notice and this permission notice shall be included in
% all copies or substantial portions of the Software.
% 
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
% THE SOFTWARE.

clear, clc

tic

%============= Type in the path for the extracted folder 'SPL_SupMat' =====
user_folder = '/home/wilder/Documents/Doctorate/gaaf_registration.git/SPL_SupMat';
%==========================================================================

useAllCorrespondences = 'clean';
get_data; % recover data from PCDs

correspondences = 'cleanedCorrs.txt ';
%correspondences = 'good_correspondences.txt '
correspondences_for_error = 'good_correspondences.txt ';
mu_values = 8;
mu_steep = mu_values/4; % It has to be 1/4 of the mu_values according to the steepest-descent update rule (Eq. (12) in the paper).

GA_LMS_Cpp = [user_folder,'/Simulations/Scripts/Cpp/GA-LMS_bunny/build/GA-LMS_bunny'];

realizations = 1;

for i=1:length(mu_values)

display(sprintf('Registration using GA-LMS (%g/%g) - | mu_steep = %g | mu_galms = %g |', i, length(mu_values), mu_steep, mu_values(i)));    

for l=1:realizations % Runs the sims for L realizations   
    display(sprintf('Realization %g/%g',l,realizations));

% Calling the GA-LMS binary (compiled from C++ code). The input (target PCD, source PCD, and \mu)
% has to be converted to string before passing it. The system function
% argument has to be a string. See the following answer for more
% information:
% http://www.mathworks.com/matlabcentral/answers/92537-how-do-i-pass-arguments-into-and-out-of-my-standalone-executable.
cmd = [GA_LMS_Cpp,' targetkps.pcd',' sourcekps.pcd ',correspondences,correspondences_for_error,num2str(mu_steep),' ',num2str(mu_values(i))];
system(cmd);

S_reg = loadpcd('sourcekps_reg.pcd');

import_CF;
%import_MSE_steep;
import_MSE;
import_rotor;

    if (l==1) % creates the variables of esemble average in the first realization
        mse = zeros(length(MSE),1);       
    end
    
% emsemble average
mse  = mse + MSE./realizations;

MSE = zeros(length(mse),1);

end

MSE = 10*log10(mse.^2);

%============================== SAVING ====================================
dataFolder = strsplit(pwd, '/'); % getting the folder name where the data is.
filename_to_save = strcat('simData','.mat'); % file name to save.
savefolder = fullfile(pwd,'Results_realizations',sprintf('L = %g',realizations),sprintf('mu = %g',mu_values(i)));
mkdir(savefolder);

save(fullfile(savefolder,filename_to_save));
copyfile('sourcekps_reg.pcd',savefolder);

%============================= PLOTTING ===================================
iterations = length(MSE);
dataSet = strcat(strjoin(strsplit(strcat(strjoin(dataFolder(end))),'_'))); % grabing the name of the data set

% Sizes for IEEE paper
fig_width = 6.5;
fig_height = 1.7;

line_width = 3;
font_size = 11;

% GOOD CORRESPONDENCES -> As pointed out in the paper (Section V.B), we 
% use only the good correspondences, i.e. outlier-free correspondences, 
% stored in the file 'good_correspondences.txt', to plot the cost function 
% (CF) curve. This is done in order to obtain a CF learning curve free of outliers,
% what would naturally happen if the point matching in [1] was perfect. 
% This way, we can see how the rotors provided by the GA-LMS align the 
% true (good) correspondences. 

MSE_and_CF_fig = figure('Name','CostFunction-MSE',...
                   'Units','inches',...
                   'Position',[0 0 fig_width fig_height],... 
                   'PaperPositionMode','auto'); 
title(sprintf('Cost Function MSE - %s',dataSet),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times'),
xlabel('Iterations','Interpreter','latex','FontUnits','points','FontSize',font_size,'FontName','Times'), 
ylabel('MSE (dB)','interpreter','latex','FontUnits','points','FontSize',font_size,'FontName','Times'), hold on
plot((0:iterations-1),MSE,'b-','LineWidth',1.5);
plot((0:iterations-1),CF,'g-','LineWidth',3);
%plot((0:iterations-1),MSE_steep,'r-','LineWidth',3);
grid on;
annotation('textarrow',[0.23,0.30],[0.40,0.63],...
           'String','(5)','FontSize',font_size,'FontName','Times');
annotation('textarrow',[0.67,0.7],[0.8,0.62],...
           'String','AF MSE','FontSize',font_size,'FontName','Times');
set(gcf,'PaperPositionMode','Manual',...
        'PaperUnits','Inches','PaperSize',[fig_width-0.5, fig_height+0.1],...
        'PaperPosition',[-0.3 0.05 fig_width, fig_height]); % Necessary because the issue with long Ylabel (it shifts the printed pdf to the right,
                                                                     % creating blank space).
set(gca,'FontUnits','points','FontWeight','normal','FontSize',font_size,'FontName','Times','XLim',[0 250],'XTick',0:50:250,'YLim',[-60 -10],'YTick',-60:20:-20);
%savefig(fullfile(savefolder,'Figure_CostFunction_and_AF_MSE_bunny.fig'))
saveas(MSE_and_CF_fig,fullfile(savefolder,'Figure_MSE_and_CF.fig'));
title(''); % Turn off title to print the PDF
print('-dpdf','-r300',fullfile(savefolder,'Figure_MSE_and_CF'))

% Calculating MSE_SVD
MSE_SVD;

% Plotting the misaligned PCDs
misaligned_PCDs_fig = figure; 
title('Misaligned PCDs'), 
xlabel('X','Interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), 
ylabel('Y','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'),
zlabel('Z','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), hold on;
scatter3(targetKps(3,:),targetKps(1,:),targetKps(2,:),15,'xr');
scatter3(sourceKps(3,:),sourceKps(1,:),sourceKps(2,:),15,'xb');
%savefig(fullfile(savefolder,'Misaligned_PCDs.fig'))
saveas(misaligned_PCDs_fig,fullfile(savefolder,'Figure_misaligned_PCDs.fig'));
print('-dpdf','-r300',fullfile(savefolder,'Figure_misaligned_PCDs'))

% Plotting the aligned PCDs
%sourceKps_new = (applyrotor(r_galms,sourceKps) - repmat(tr_galms,1,size(sourceKps,2)));
aligned_PCDs_fig = figure;
title('Aligned PCDs'), 
xlabel('X','Interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), 
ylabel('Y','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'),
zlabel('Z','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), hold on;
scatter3(targetKps(3,:),targetKps(1,:),targetKps(2,:),15,'xr');
scatter3(S_reg(3,:),S_reg(1,:),S_reg(2,:),15,'xb');
%savefig(fullfile(savefolder,'Aligned_PCDs.fig')) % For Matlab 2014a
saveas(aligned_PCDs_fig,fullfile(savefolder,'Figure_aligned_PCDs.fig'));
print('-dpdf','-r300',fullfile(savefolder,'Figure_aligned_PCDs'))


close all;
delete('MSE.txt','CF.txt','rotor.txt','sourcekps_reg.pcd','MSE_steep.txt','rotor_steep.txt');

end

time_sec = toc;