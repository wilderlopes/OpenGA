% gaafs.m - General script to call the GAAFs 
% 
% Matlab code by:
% Wilder Bezerra Lopes - Ph.D. Student 
% University of Sao Paulo (USP)
% February 2016
% www.openga.org
% www.lps.usp.br/wilder
% wil@openga.org

% The MIT License (MIT)
% 
% Copyright (c) 2016 onwards, by Wilder Lopes
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

close all
clear, clc

tic;

%============= Type in the path for the extracted folder ==================
user_folder = '../../../GAAFs_source/GAAFs_standard';
%==========================================================================

GA_LMS_Cpp = [user_folder,'/GA-LMS/build/GA-LMS']; %Note which binary is selected!!!

% Simulation parameters
M            = [1:10 15:5:45 46:50]; % System order (number of taps)
N            = 3000; % Time iterations
L            = 100; % Amount of experiments/realizations;
mu           = 0.005; % AF Step size
sigma2v      = [0 1e-9 1e-6 1e-5 1e-4 1e-3 1e-2]; % Variance of measurement noise

MSE_steadyState  = zeros(length(M),1); % To accumulate the average steady-state MSE
EMSE_steadyState = zeros(length(M),1); % To accumulate the average steady-state EMSE
MSE_steadyState_theory  = zeros(length(M),1); % To accumulate the theoretical steady-state MSE
EMSE_steadyState_theory = zeros(length(M),1); % To accumulate the theoretical steady-state EMSE
MSE_minus_theory  = zeros(length(M),1); % To accumulate the average steady-state 
                                        % MSE minus EMSE theory
EMSE_minus_theory  = zeros(length(M),1); % To accumulate the average steady-state 
                                         % EMSE minus EMSE theory

for j=1:length(sigma2v)

    M_counter = 0;
    
for order=M
    
    M_counter = M_counter + 1; % Counting how many different M orders are
                               % being used.
    if order > 40 % If number of taps is higher than 40, increase the 
                  % the number of iterations so the steady-state level can
                  % be calculated by averaging the last 200 points.
        N = 6000;
    end


for i=1:length(mu)
    display(sprintf('Running GA-LMS: sigma^2 = %g (%g/%g) | mu = %g (%g/%g)',...
        sigma2v(j), j, length(sigma2v), mu(i), i, length(mu)));
 
% for l=1:L % Runs the sims for L realizations   
%     display(sprintf('Realization %g/%g',l,L));
   
% Calling the GA-LMS binary (compiled from C++ code). The system function
% argument has to be a string. See the following answer for more
% information:
% http://www.mathworks.com/matlabcentral/answers/92537-how-do-i-pass-arguments-into-and-out-of-my-standalone-executable.
cmd = [GA_LMS_Cpp,' ',num2str(order),' ',num2str(L),' ',num2str(N),' ', ...
    num2str(mu(i)),' ',num2str(sigma2v(j))];

system(cmd); % executes the binary

% Importing results gernearted by the C++ code into Matlab 
import_MSE;
import_EMSE;
import_MSE_theory;
import_EMSE_theory;
import_W; % Imports final multivector W (weight vector)

%     if (l==1) % creates the variables of esemble average in the first realization
%         mse = zeros(length(MSE),1);
%         emse = zeros(length(EMSE),1);        
%     end
    
% % emsemble average
% mse  = mse + MSE./realizations;
% emse = emse + EMSE./realizations;


% MSE = zeros(length(mse),1);
% EMSE = zeros(length(emse),1);

% end

mean_MSE  = mean(MSE((N-200):N));
mean_EMSE = mean(EMSE((N-200):N));

MSE_steadyState(M_counter,:)= 10*log10(mean_MSE); % Averaging the MSE last 200 points
EMSE_steadyState(M_counter,:)= 10*log10(mean_EMSE); % Averaging the EMSE last 200 points
MSE_steadyState_theory(M_counter,:)= 10*log10(MSE_theory); % Steady-state theory for each M
EMSE_steadyState_theory(M_counter,:)= 10*log10(EMSE_theory); % Steady-state theory for each M
MSE_minus_theory(M_counter,:)= 10*log10(mean_MSE - MSE_theory); % Steady-state MSE minus MSE bound
EMSE_minus_theory(M_counter,:)= 10*log10(mean_EMSE - EMSE_theory); % Steady-state EMSE minus EMSE bound
%EMSE_minus_noise(M_counter,:)= 10*log10(mean(EMSE((N-200):N)) - sigma2v); % Average minus noise

MSE              = 10*log10(MSE);
EMSE             = 10*log10(EMSE);
MSE_theory_line  = 10*log10(MSE_theory*ones(N,1));
EMSE_theory_line = 10*log10(EMSE_theory*ones(N,1));

%============================== SAVING ====================================
dataFolder = strsplit(pwd, '/'); % getting the folder name where the data is.
filename_to_save = strcat('simData','.mat'); % file name to save.
savefolder = fullfile(pwd,'Results',sprintf('sigma2v = %g',sigma2v(j)), ...
            sprintf('M=%g',order), sprintf('N=%g',N),sprintf('L=%g',L), ...
            sprintf('mu = %g',mu(i)));
    
mkdir(savefolder);

save(fullfile(savefolder,filename_to_save));
%copyfile('sourcekps_reg.pcd',savefolder);
%============================= PLOTTING ===================================
iterations = length(MSE);
dataSet = strcat(strjoin(strsplit(strcat(strjoin(dataFolder(end))),'_'))); % grabing the name of the data set

% fig_width = 5;
% fig_height = 2.3;

% Sizes for IEEE paper
fig_width = 10;
fig_height = 3.6;

line_width = 3;

MSE_figure = figure('Name','MSE',...
                    'Units','inches',...
                    'Position',[0 0 fig_width fig_height],...
                    'PaperPositionMode','auto',...
                    'Visible','off'); 
title(sprintf('GA-LMS - M=%g, N=%g, L=%g, mu=%g, sigma2v=%g',order,N,L,mu(i),sigma2v(j)),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times'),
xlabel('Iterations','Interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), 
ylabel('MSE (dB)','interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), hold on
plot((0:iterations-1),MSE,'b-','LineWidth',1.5);
plot((0:iterations-1),MSE_theory_line,'magenta--','LineWidth',3);
grid on;
% annotation('textarrow',[0.23,0.30],[0.40,0.63],...
% 'String','$\sigma^2_v = 10^{{}^{\_}7}$','FontSize',font_size,'FontName','Times','Interpreter','latex');
legend('MSE','MSE bound'); legend boxoff;
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[fig_width, fig_height+0.1]);
set(gca,'FontUnits','points','FontWeight','normal','FontSize',14,'FontName','Times');
%savefig(fullfile(savefolder,'Figure_MSE.fig')) % For Matlab 2014a
saveas(MSE_figure,fullfile(savefolder,'Figure_MSE.fig'));
legend 'off';
title '';
print('-dpdf','-r300',fullfile(savefolder,'Figure_MSE'))


EMSE_figure = figure('Name','EMSE',...
                    'Units','inches',...
                    'Position',[0 0 fig_width fig_height],...
                    'PaperPositionMode','auto',...
                    'Visible','off');
title(sprintf('GA-LMS - M=%g, N=%g, L=%g, mu=%g, sigma2v=%g',order,N,L,mu(i),sigma2v(j)),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times','Interpreter','latex'),
xlabel('Iterations','Interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), 
ylabel('EMSE (dB)','interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), hold on
plot((0:iterations-1),EMSE,'r-','LineWidth',1.5);
plot((0:iterations-1),EMSE_theory_line,'magenta--','LineWidth',3);
grid on;
legend('EMSE','EMSE bound'); legend boxoff;
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[fig_width, fig_height+0.1]);
set(gca,'FontUnits','points','FontWeight','normal','FontSize',14,'FontName','Times');
%savefig(fullfile(savefolder,'Figure_EMSE.fig'))  % For Matlab 2014a
saveas(EMSE_figure,fullfile(savefolder,'Figure_EMSE.fig'));
legend 'off';
title '';
print('-dpdf','-r300',fullfile(savefolder,'Figure_EMSE'))


%close all;

end

end

MSE_and_EMSE_figure = figure('Name','EMSE_and_MSE',...
                    'Units','inches',...
                    'Position',[0 0 fig_width fig_height],...
                    'PaperPositionMode','auto',...
                    'Visible','off');
title(sprintf('GAAF - Multivector Entry - Average Steady-State Error - mu = %g, sigma2v = %g', mu(i), sigma2v(j)),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times','Interpreter','latex'),
xlabel('System Order (Taps)','Interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), 
ylabel('Error (dB)','interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), hold on
plot(M,MSE_steadyState,'b--o','LineWidth',3,'MarkerSize',10);
plot(M,EMSE_steadyState,'r--o','LineWidth',3,'MarkerSize',10);
plot(M,MSE_steadyState_theory,'green-*','LineWidth',2,'MarkerSize',10);
plot(M,EMSE_steadyState_theory,'magenta-*','LineWidth',2,'MarkerSize',10);
grid on;
legend('MSE','EMSE','MSE theory','EMSE theory','Location','east'); legend boxoff;
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[fig_width, fig_height+0.1]);
set(gca,'FontUnits','points','FontWeight','normal','FontSize',14,'FontName','Times');
%savefig(fullfile(savefolder,'Figure_MSE_and_EMSE.fig'))  % For Matlab 2014a
saveas(MSE_and_EMSE_figure,fullfile(savefolder,'Figure_MSE_and_EMSE.fig'));
print('-dpdf','-r300',fullfile(savefolder,'Figure_MSE_and_EMSE'))
title ''
xlim([0 40])
print('-dpdf','-r300',fullfile(savefolder,'Figure_MSE_and_EMSE_GALMS_mv'))

sims_minus_theory_figure = figure('Name','sims_minus_theory',...
                    'Units','inches',...
                    'Position',[0 0 fig_width fig_height],...
                    'PaperPositionMode','auto',...
                    'Visible','off');
title(sprintf('GAAF - Multivector Entry - Sims minus theory - mu = %g, sigma2v = %g', mu(i), sigma2v(j)),...
    'FontUnits','points','FontWeight','normal','FontSize',12,'FontName','Times','Interpreter','latex'),
xlabel('System Order (Taps)','Interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), 
ylabel('Error (dB)','interpreter','latex','FontUnits','points','FontSize',18,'FontName','Times'), hold on
plot(M,MSE_minus_theory,'b--o','LineWidth',1.5,'MarkerSize',10);
plot(M,EMSE_minus_theory,'r--o','LineWidth',1.5,'MarkerSize',10);
grid on;
legend('MSE minus MSEtheory','EMSE minus EMSEtheory'); legend boxoff;
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[fig_width, fig_height+0.1]);
set(gca,'FontUnits','points','FontWeight','normal','FontSize',14,'FontName','Times');
%savefig(fullfile(savefolder,'Figure_MSE_and_EMSE.fig'))  % For Matlab 2014a
saveas(sims_minus_theory_figure ,fullfile(savefolder,'Figure_Sims_minus_Theory.fig'));
print('-dpdf','-r300',fullfile(savefolder,'Figure_Sims_minus_Theory'))

end

time_sec = toc;
