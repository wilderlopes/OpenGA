function Y = applyrotor(r,X)
% Apply a geometric-algebra rotor to a point cloud in order to rotate it.  

N = size(X,2); % number of vectors in the input Point Cloud (PC)
Y = zeros(3,N); % output PC

for j=1:N
    x = X(1,j)*e1 + X(2,j)*e2 + X(3,j)*e3; % selecting a vector and converting to GA.
    y = r*x/r; % rotates the vector x
        if y==0
            coeff = [0 0 0 0 0 0 0 0];
        else
            coeff = coefficients(y); % gets the coefficients of the rotated vector
        end
    Y(:,j) = coeff(2:4)'; % stores the rotated vectors in the output PC  
end

