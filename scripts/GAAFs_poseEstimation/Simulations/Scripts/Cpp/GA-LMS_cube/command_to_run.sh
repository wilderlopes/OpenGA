#!/bin/bash

cd build && ./GA-LMS /home/wilder/dev/OpenGA/scripts/GAAFs_poseEstimation/Simulations/Cube/Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0/targetkps.pcd /home/wilder/dev/OpenGA/scripts/GAAFs_poseEstimation/Simulations/Cube/Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0/sourcekps.pcd 2e-1 1e-7 && pcl_viewer /home/wilder/dev/OpenGA/scripts/GAAFs_poseEstimation/Simulations/Cube/Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0/targetkps.pcd /home/wilder/dev/OpenGA/scripts/GAAFs_poseEstimation/Simulations/Cube/Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0/sourcekps.pcd &

cd build && pcl_viewer /home/wilder/dev/OpenGA/scripts/GAAFs_poseEstimation/Simulations/Cube/Cube_PCDs_1728pts_0.5edge_X120Y90Z45_var_v0/targetkps.pcd sourcekps_reg.pcd & 
