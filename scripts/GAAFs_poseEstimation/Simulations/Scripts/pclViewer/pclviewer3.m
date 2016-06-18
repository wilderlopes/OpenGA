%PCLVIEWER3 View 2 point clouds using PCL
%
% PCLVIEWER2(P, Q, R) writes the point clouds P (MxN), Q (MxN), and R (MxN) to a temporary file and invokes
% the PCL point cloud viewer for fast display and visualization.  The
% columns of P, Q, and R represent the 3D points.
%
% If M=3 then the rows are x, y, z.
% If M=6 then the rows are x, y, z, R, G, B where R,G,B are in the range 0
% to 1.
%
% PCLVIEWER3(P, Q, ARGS) as above but the optional arguments ARGS are passed to the
% PCL viewer.  For example:
%
%         pclviewer(P, Q, '-ps 2 -ax 1' )
%
% Notes::
% - Only the "x y z" and "x y z rgb" field formats are currently supported.
% - The file is written in ascii format.
% - When viewing colored point clouds in pcl_viewer remember to toggle to 
%
% See also savepcd, lspcd, readpcd.
%
% Copyright (C) 2013, by Peter I. Corke
% Modified by Wilder B. Lopes to visualize 2 point clouds - 11.07.2014

% Syntax is: pcd_viewer <file_name 1..N>.pcd <options>
%   where options are:
%                      -bc r,g,b                = background color
%                      -fc r,g,b                = foreground color
%                      -ps X                    = point size (1..64)
%                      -opaque X                = rendered point cloud opacity (0..1)
%                      -ax n                    = enable on-screen display of XYZ axes and scale them to n
%                      -ax_pos X,Y,Z            = if axes are enabled, set their X,Y,Z position in space (default 0,0,0)
% 
%                      -cam (*)                 = use given camera settings as initial view
%  (*) [Clipping Range / Focal Point / Position / ViewUp / Distance / Window Size / Window Pos] or use a <filename.cam> that contains the same information.
% 
%                      -multiview 0/1           = enable/disable auto-multi viewport rendering (default disabled)
% 
% 
%                      -normals 0/X             = disable/enable the display of every Xth point's surface normal as lines (default disabled)
%                      -normals_scale X         = resize the normal unit vector size to X (default 0.02)
% 
%                      -pc 0/X                  = disable/enable the display of every Xth point's principal curvatures as lines (default disabled)
%                      -pc_scale X              = resize the principal curvatures vectors size to X (default 0.02)
% 
% 
% (Note: for multiple .pcd files, provide multiple -{fc,ps} parameters;
% they will be automatically assigned to the right file). Example:
% 
% pclviewer3(X, Y, T, '-fc 0,0,255 -fc 0,255,0 -fc 255,0,0'); - It plots point clouds X in blue, Y in green, and Y in red.


function pclviewer3(pc1, pc2, pc3, args)
    
     
    pointfile1 = [tempname '.pcd'];
    pointfile2 = [tempname '.pcd'];
    pointfile3 = [tempname '.pcd'];
    
    if nargin < 4
        args = '';
    end
    
    savepcd(pointfile1, pc1);
    savepcd(pointfile2, pc2);    
    savepcd(pointfile3, pc3);
    
    OS = getenv('OS'); % Gets the operational system 
    
    if strcmp(OS,'Windows_NT') % action if OS is Windows    
        viewer = 'pcd_viewer_release';
        system(sprintf('%s %s %s %s %s &', ...
            viewer, pointfile1, pointfile2, pointfile3, args));
    else % action if OS is Linux
        viewer = '/usr/bin/pcl_viewer';
        unix(sprintf('%s %s %s %s %s &', ...
            viewer, pointfile1, pointfile2, pointfile3, args));
    end
 
    pause(1)
    delete(pointfile1);
    delete(pointfile2);
    delete(pointfile3);
    