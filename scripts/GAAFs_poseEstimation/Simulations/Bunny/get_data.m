% get_data.m - Script to load the PCDs and its parameters
% Cube set case.
% 
% Supplementary material for IEEE Signal Processing Letters submission:
% "Geometric-Algebra LMS Adaptive Filter and its Application to Rotation Estimation", 
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
% Copyright (c) 2015 Wilder Lopes
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


% Source and Target PCs XYZRGB
sourceKps = loadpcd('sourcekps.pcd');
targetKps = loadpcd('targetkps.pcd');

sourceKps = double(sourceKps); % converting to double precising because operations in GA require that. 
targetKps = double(targetKps);

%Getting correspondence indexes and distances
[query_all, match_all, distances_all] = importfile_PCL('all_correspondences.txt');
[query_good, match_good, distances_good] = importfile_PCL('good_correspondences.txt');
[query_clean, match_clean, distances_clean] = importfile_PCL('cleanedCorrs.txt');

%Reshaping the PCs
sourceKps = sourceKps(1:3,:); % The source point cloud XYZ
targetKps = targetKps(1:3,:); % The source point cloud XYZ 

X_all = zeros(3,size(query_all,1));
Y_all = zeros(3,size(match_all,1));

X_good = zeros(3,size(query_good,1));
Y_good = zeros(3,size(match_good,1));

X_clean = zeros(3,size(query_clean,1));
Y_clean = zeros(3,size(match_clean,1));

for iter=1:length(query_all)
    X_all(:,iter) = sourceKps(1:3, query_all(iter)+1);  
    Y_all(:,iter) = targetKps(1:3, match_all(iter)+1);
end

for iter=1:length(query_good)
    X_good(:,iter) = sourceKps(1:3, query_good(iter)+1);  
    Y_good(:,iter) = targetKps(1:3, match_good(iter)+1);
end

for iter=1:length(query_clean)
    X_clean(:,iter) = sourceKps(1:3, query_clean(iter)+1);  
    Y_clean(:,iter) = targetKps(1:3, match_clean(iter)+1);
end

if strcmp(useAllCorrespondences,'all')    
    T = Y_all; % target keypoints cloud (all correspondences)
    S = X_all; % source keypoints cloud (all correspondences)
    distances = distances_all; % distances between correspondent keypoints
elseif strcmp(useAllCorrespondences,'good')
    T = Y_good; % target keypoints cloud (good correspondences)
    S = X_good; % source keypoints cloud (good correspondences)
    distances = distances_good; % distances between correspondent keypoints
elseif strcmp(useAllCorrespondences,'clean')
    T = Y_clean; % target keypoints cloud (clean correspondences)
    S = X_clean; % source keypoints cloud (clean correspondences)
    distances = distances_clean; % distances between correspondent keypoints
end

%As pointed out in the paper, we use the good correspondences to calculate 
%the cost function (5). The Y_for_error and X_for_error store those PCDs.
Y_for_error = Y_good;
X_for_error = X_good;
