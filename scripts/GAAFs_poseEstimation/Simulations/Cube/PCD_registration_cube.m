% PCD_registration.m - General script to register a Point Cloud.
% Cube set case
% 
% Supplementary material for IEEE Signal Processing Letters submission:
% "Geometric-Algebra LMS Adaptive Filter and its Application to Rotation
% Estimation.", 
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

tic;

%============= Type in the path for the extracted folder 'SPL_SupMat' =====
user_folder = 'write_path_to_folder_here/SPL_SupMat';
%==========================================================================

% Source and Target PCs XYZRGB
T = loadpcd('targetkps.pcd');
S = loadpcd('sourcekps.pcd');

% converting to double precising because operations in GA require that. 
T = double(T); 
S = double(S); 

Y_for_error = T;
X_for_error = S;

sigma2v_values = [1e-9 1e-5 1e-2 0];

mu_values = [0.06 0.2 0.3 1.2];

GA_LMS_Cpp = [user_folder,'/Simulations/Scripts/Cpp/GA-LMS_cube/build/GA-LMS_noCF']; %Note which binary is selected!!!

realizations = 200; % Amount of experiments/realizations;

for j=1:length(sigma2v_values)

for i=1:length(mu_values)
    display(sprintf('Registration using GA-LMS: sigma^2 = %g (%g/%g) | mu = %g (%g/%g)', sigma2v_values(j), j, length(sigma2v_values), mu_values(i), i, length(mu_values)));
 
for l=1:realizations % Runs the sims for L realizations   
    display(sprintf('Realization %g/%g',l,realizations));
   
% Calling the GA-LMS binary (compiled from C++ code). The input (target PCD, source PCD, and \mu)
% has to be converted to string before passing it. The system function
% argument has to be a string. See the following answer for more
% information:
% http://www.mathworks.com/matlabcentral/answers/92537-how-do-i-pass-arguments-into-and-out-of-my-standalone-executable.
cmd = [GA_LMS_Cpp,' targetkps.pcd',' sourcekps.pcd ',num2str(mu_values(i)),' ',num2str(sigma2v_values(j))];
system(cmd);

S_reg = loadpcd('sourcekps_reg.pcd');

% Importing results gernearted by the C++ code into Matlab 
import_MSE;
import_EMSE;
import_rotor;

    if (l==1) % creates the variables of esemble average in the first realization
        mse = zeros(length(MSE),1);
        emse = zeros(length(EMSE),1);        
    end
    
% emsemble average
mse  = mse + MSE./realizations;
emse = emse + EMSE./realizations;


MSE = zeros(length(mse),1);
EMSE = zeros(length(emse),1);

end

MSE = 10*log10(mse.^2);
EMSE = 10*log10(emse.^2);

%============================== SAVING ====================================
dataFolder = strsplit(pwd, '/'); % getting the folder name where the data is.
filename_to_save = strcat('simData','.mat'); % file name to save.
savefolder = fullfile(pwd,'Results_realizations',sprintf('L = %g',realizations),sprintf('sigma2v = %g',sigma2v_values(j)),sprintf('mu = %g',mu_values(i)));
mkdir(savefolder);

save(fullfile(savefolder,filename_to_save));
copyfile('sourcekps_reg.pcd',savefolder);
%============================= PLOTTING ===================================
iterations = length(MSE);
dataSet = strcat(strjoin(strsplit(strcat(strjoin(dataFolder(end))),'_'))); % grabing the name of the data set

% Sizes for IEEE paper
fig_width = 5;
fig_height = 2.3;

line_width = 3;

MSE_figure = figure('Name','MSE',...
                    'Units','inches',...
                    'Position',[0 0 fig_width fig_height],...
                    'PaperPositionMode','auto',...
                    'Visible','off'); 
title(sprintf('Adaptive Filter MSE - %s - mu = %g ',dataSet, mu_values(i)),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times'),
xlabel('Iterations','Interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), 
ylabel('AF - MSE (dB)','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), hold on
plot((0:iterations-1),MSE,'b-','LineWidth',1.5);
grid on;
% annotation('textarrow',[0.23,0.30],[0.40,0.63],...
% 'String','$\sigma^2_v = 10^{{}^{\_}7}$','FontSize',font_size,'FontName','Times','Interpreter','latex');
legend(sprintf('GA-LMS - sigma2v=%g, mu=%g, L=%g',sigma2v_values(j),mu_values(i),realizations)); legend boxoff;
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[fig_width, fig_height+0.1]);
set(gca,'FontUnits','points','FontWeight','normal','FontSize',10,'FontName','Times');
%savefig(fullfile(savefolder,'Figure_MSE.fig')) % For Matlab 2014a
saveas(MSE_figure,fullfile(savefolder,'Figure_MSE.fig'));
print('-dpdf','-r300',fullfile(savefolder,'Figure_MSE'))


EMSE_figure = figure('Name','EMSE',...
                    'Units','inches',...
                    'Position',[0 0 fig_width fig_height],...
                    'PaperPositionMode','auto',...
                    'Visible','off');
title(sprintf('Adaptive Filter EMSE - %s - mu = %g ',dataSet, mu_values(i)),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times'),
xlabel('Iterations','Interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), 
ylabel('AF - EMSE (dB)','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), hold on
plot((0:iterations-1),EMSE,'r-','LineWidth',1.5);
grid on;
legend(sprintf('GA-LMS - sigma2v=%g, mu=%g, L=%g',sigma2v_values(j),mu_values(i),realizations)); legend boxoff;
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[fig_width, fig_height+0.1]);
set(gca,'FontUnits','points','FontWeight','normal','FontSize',10,'FontName','Times');
%savefig(fullfile(savefolder,'Figure_EMSE.fig'))  % For Matlab 2014a
saveas(EMSE_figure,fullfile(savefolder,'Figure_EMSE.fig'));
print('-dpdf','-r300',fullfile(savefolder,'Figure_EMSE'))

misaligned_PCDs_fig = figure('Name','misaligned_PCDs',...
                             'PaperPositionMode','auto',...
                             'Visible','off'); 
title('Misaligned PCDs'),
xlabel('X','Interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), 
ylabel('Y','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'),
zlabel('Z','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), hold on;
scatter3(T(3,:),T(1,:),T(2,:),15,'xr');
scatter3(S(3,:),S(1,:),S(2,:),15,'xb');
saveas(misaligned_PCDs_fig,fullfile(savefolder,'Figure_misaligned_PCDs.fig'));
%print('-dpdf','-r300',fullfile(savefolder,'Misaligned_PCDs'))

aligned_PCDs_fig = figure('Name','aligned_PCDs',...
                          'PaperPositionMode','auto',...
                          'Visible','off'); 
title('Aligned PCDs'),
xlabel('X','Interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), 
ylabel('Y','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'),
zlabel('Z','interpreter','latex','FontUnits','points','FontSize',10,'FontName','Times'), hold on;
scatter3(T(3,:),T(1,:),T(2,:),15,'xr');
scatter3(S_reg(3,:),S_reg(1,:),S_reg(2,:),15,'xb');
saveas(aligned_PCDs_fig,fullfile(savefolder,'Figure_aligned_PCDs.fig'));
%print('-dpdf','-r300',fullfile(savefolder,'Aligned_PCDs'))

%pclviewer2(S_reg,T,'-fc 0,0,255 -fc 255,0,0');

close all;
delete('MSE.txt','EMSE.txt','rotor.txt','sourcekps_reg.pcd');

end

end

time_sec = toc;