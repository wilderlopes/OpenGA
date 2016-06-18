% Calculating the SVD error - Bunny case
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

% The following matrix was calculated using the Jacobi SVD algorithm, 
% as implemented in EIGEN (http://eigen.tuxfamily.org/dox/classEigen_1_1JacobiSVD.html), 
% a C++ template library for linear algebra, which is used by the
% Point Cloud Library (http://pointclouds.org/).
%
% GOOD CORRESPONDENCES -> As pointed out in the paper (Section V.B), we 
% use only the good correspondences, i.e. outlier-free correspondences, 
% stored in the file 'good_correspondences.txt', to plot the cost function 
% (CF) curve. This is done in order to obtain a CF learning curve free of outliers,
% what would naturally happen if the point matching in [1] was perfect. 
% This way, we can see how the rotors provided by the GA-LMS align the 
% true (good) correspondences. 
Transf_SVD =[ 0.844653 -0.00109573    0.535313  -0.0519838
 0.00289789    0.999993 -0.00252524 0.000959478
  -0.535307  0.00368419     0.84465  -0.0131625
          0           0           0           1];     

S_1_svd = [X_for_error; ones(1,size(X_for_error,2))];
S_reg_svd = Transf_SVD*S_1_svd;
S_reg_svd = S_reg_svd(1:3,:);
ErrorMat_SVD = Y_for_error-S_reg_svd;
mse_SVD = trace(ErrorMat_SVD'*ErrorMat_SVD)/size(T,2);
mse_SVD_dB = 10*log10(mse_SVD);
display(sprintf('MSE of Jacobi SVD = %g dB',mse_SVD_dB));   
