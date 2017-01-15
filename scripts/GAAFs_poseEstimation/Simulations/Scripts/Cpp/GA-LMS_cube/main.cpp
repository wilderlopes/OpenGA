#define _USE_MATH_DEFINES
#include <boost/thread/thread.hpp>
#include <cmath>
#include <random>
#include <iostream>
#include <sstream>
#include <fstream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <Eigen/Eigen>
#include <iterator> // for ostream_iterator
#include <math.h>       /* log10 */
#include <stdio.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/visualization/point_cloud_color_handlers.h>
#include <algorithm>    // std::random_shuffle
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand

//#include "gnuplot-iostream.h"
#include "gaalet/include/gaalet.h"

using namespace std;
using namespace Eigen;

/*
boost::shared_ptr<pcl::visualization::PCLVisualizer> customColourVis (pcl::PointCloud<pcl::PointXYZ>::ConstPtr cloud, pcl::PointCloud<pcl::PointXYZ>::ConstPtr cloud_2, string name)
{
  // --------------------------------------------
  // -----Open 3D viewer and add point cloud-----
  // --------------------------------------------
  boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer (new pcl::visualization::PCLVisualizer (name));
  viewer->setBackgroundColor (0, 0, 0);
  pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ> red(cloud, 255, 0, 0);
  pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ> blue(cloud_2, 0, 0, 255);
  viewer->addPointCloud<pcl::PointXYZ> (cloud, red, "target");
  viewer->addPointCloud<pcl::PointXYZ> (cloud_2, blue, "source");
  viewer->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 3, "target");
  viewer->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 3, "source");
  viewer->addCoordinateSystem (1e-2);
  viewer->initCameraParameters ();
  return (viewer);
}
*/

int myrandom (int i) { return std::rand()%i;}

int main(int argc, char* argv[])
{

    //Gnuplot gp;

    double error_galms, emse;
    //double cost_function_mag, cost_function_mag_emse;
    //double cost_function = 0;
    //double cost_function_emse = 0;
    double mu_galms = 0;
    double noiseVar; //noise variance
    int iter_value;
    //double K;



    //---Random noise generator
    std::stringstream str_noiseVar(argv[4]);
    str_noiseVar >> noiseVar; //noise variance

    std::default_random_engine generator;
    std::normal_distribution<double> distribution(0,sqrt(noiseVar)); //zero-mean and variance (std deviation) defined by input
    //---

    //std::vector<double> CF_galms;
    //std::vector<double> CF_galms_emse;
    std::vector<double> MSE_galms;
    std::vector<double> EMSE_galms;
    //std::vector<double> MSD_galms;
    std::vector<int> myvector;

    typedef gaalet::algebra<gaalet::signature<3,0> > em;

    // LOADING POINT CLOUDS ================================================================
    pcl::PointCloud<pcl::PointXYZ>::Ptr targetPCDPtr (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr sourcePCDPtr (new pcl::PointCloud<pcl::PointXYZ>);

    if (pcl::io::loadPCDFile<pcl::PointXYZ> (argv[1], *targetPCDPtr) == -1) //* load target PCD
    {
      PCL_ERROR ("Couldn't read target PCD \n");
      return (-1);
    }

    if (pcl::io::loadPCDFile<pcl::PointXYZ> (argv[2], *sourcePCDPtr) == -1) //* load source PCD
    {
      PCL_ERROR ("Couldn't read source PCD \n");
      return (-1);
    }

    //=======================================================================================


    //Code for scrambling the correspondences each time the binary is called by Matlab
    for (size_t i=1; i < targetPCDPtr->points.size (); ++i) myvector.push_back(i);
    std::srand ( unsigned ( std::time(0) ) );
    std::random_shuffle ( myvector.begin(), myvector.end(), myrandom);

    //std::cout << "myvector " << myvector[0] << std::endl;


    // CENTROIDS ============================================================================

    em::mv<1, 2, 4>::type y_sum{0, 0, 0};
    em::mv<1, 2, 4>::type x_sum{0, 0, 0};
    em::mv<1, 2, 4>::type y_cent{0, 0, 0};
    em::mv<1, 2, 4>::type x_cent{0, 0, 0};


    // calculating centroids
    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        //std::cout << "iter_value " << iter_value << std::endl;
        y_sum[0] += targetPCDPtr->points[iter_value].x;
        y_sum[1] += targetPCDPtr->points[iter_value].y;
        y_sum[2] += targetPCDPtr->points[iter_value].z;
    }

    y_cent[0] = y_sum[0]/(targetPCDPtr->points.size ());
    y_cent[1] = y_sum[1]/(targetPCDPtr->points.size ());
    y_cent[2] = y_sum[2]/(targetPCDPtr->points.size ());

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        x_sum[0] += sourcePCDPtr->points[iter_value].x;
        x_sum[1] += sourcePCDPtr->points[iter_value].y;
        x_sum[2] += sourcePCDPtr->points[iter_value].z;
    }

    x_cent[0] = x_sum[0]/(sourcePCDPtr->points.size ());
    x_cent[1] = x_sum[1]/(sourcePCDPtr->points.size ());
    x_cent[2] = x_sum[2]/(sourcePCDPtr->points.size ());


    // Generating the new point clouds (subtracting centroids and adding noise)
    pcl::PointCloud<pcl::PointXYZ>::Ptr D_PCDPtr (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr Y_PCDPtr (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr X_PCDPtr (new pcl::PointCloud<pcl::PointXYZ>);

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        pcl::PointXYZ basic_point_1;
        basic_point_1.x = targetPCDPtr->points[iter_value].x - y_cent[0] + (double) distribution(generator); //adding gaussian noise;
        basic_point_1.y = targetPCDPtr->points[iter_value].y - y_cent[1] + (double) distribution(generator); //adding gaussian noise;
        basic_point_1.z = targetPCDPtr->points[iter_value].z - y_cent[2] + (double) distribution(generator); //adding gaussian noise;
        D_PCDPtr->points.push_back(basic_point_1);

    }

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        pcl::PointXYZ basic_point_1;
        basic_point_1.x = targetPCDPtr->points[iter_value].x - y_cent[0];
        basic_point_1.y = targetPCDPtr->points[iter_value].y - y_cent[1];
        basic_point_1.z = targetPCDPtr->points[iter_value].z - y_cent[2];
        Y_PCDPtr->points.push_back(basic_point_1);

    }

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        pcl::PointXYZ basic_point_2;
        basic_point_2.x = sourcePCDPtr->points[iter_value].x - x_cent[0];
        basic_point_2.y = sourcePCDPtr->points[iter_value].y - x_cent[1];
        basic_point_2.z = sourcePCDPtr->points[iter_value].z - x_cent[2];
        X_PCDPtr->points.push_back(basic_point_2);
    }


    //=======================================================================================

    std::stringstream str_mu_galms(argv[3]);
    str_mu_galms >> mu_galms;


    // Initializing rotor in gaalet
    em::mv<0, 3, 5, 6>::type r_old{0.5, 0.5, -0.5, 0.5};
    // Initializing rotor in gaalet
    em::mv<0, 3, 5, 6>::type r_new{0, 0, 0, 0};
    // Initializing rotor in gaalet
    //em::mv<0, 3, 5, 6>::type r_exp{0, 0, 0, 0};
    // Initializing target point in gaalet
    em::mv<1, 2, 4>::type d{0, 0, 0};
    // Initializing target point in gaalet
    em::mv<1, 2, 4>::type y{0, 0, 0};
    // Initializing source point in gaalet
    em::mv<1, 2, 4>::type x{0, 0, 0};
    // Initializing registered source point in gaalet
    em::mv<1, 2, 4>::type x_reg{0, 0, 0};
    // Initializing target point in gaalet
    //em::mv<1, 2, 4>::type d_CF{0, 0, 0};
    // Initializing target point in gaalet
    //em::mv<1, 2, 4>::type y_CF{0, 0, 0};
    // Initializing source point in gaalet
    //em::mv<1, 2, 4>::type x_CF{0, 0, 0};


    //K = Y_PCDPtr->points.size (); //Number of points in the PCDs

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        d[0] = D_PCDPtr->points[iter_value].x;
        d[1] = D_PCDPtr->points[iter_value].y;
        d[2] = D_PCDPtr->points[iter_value].z;

        y[0] = Y_PCDPtr->points[iter_value].x;
        y[1] = Y_PCDPtr->points[iter_value].y;
        y[2] = Y_PCDPtr->points[iter_value].z;

        x[0] = X_PCDPtr->points[iter_value].x;
        x[1] = X_PCDPtr->points[iter_value].y;
        x[2] = X_PCDPtr->points[iter_value].z;

        //GA-LMS
        /*
        for (size_t n = 0; n < Y_PCDPtr->points.size (); ++n) //To calculate the time evolution of the cost function
            {

                d_CF[0] = D_PCDPtr->points[n].x;
                d_CF[1] = D_PCDPtr->points[n].y;
                d_CF[2] = D_PCDPtr->points[n].z;

                y_CF[0] = Y_PCDPtr->points[n].x;
                y_CF[1] = Y_PCDPtr->points[n].y;
                y_CF[2] = Y_PCDPtr->points[n].z;

                x_CF[0] = X_PCDPtr->points[n].x;
                x_CF[1] = X_PCDPtr->points[n].y;
                x_CF[2] = X_PCDPtr->points[n].z;

                cost_function_mag = (double) eval(magnitude(d_CF - r_old*x_CF*(~r_old)));
                cost_function += pow(cost_function_mag,2);

                cost_function_mag_emse = (double) eval(magnitude(y_CF - r_old*x_CF*(~r_old)));
                cost_function_emse += pow(cost_function_mag_emse,2);

            }
        CF_galms.push_back(10*log10((1/K)*cost_function)); // appending to the cost function (CF) vector
        cost_function = 0;
        CF_galms_emse.push_back(10*log10((1/K)*cost_function_emse)); // appending to the cost function (CF) vector
        cost_function_emse = 0;
        */

        error_galms = (double) eval(magnitude(d - r_old*x*(~r_old)));
        MSE_galms.push_back(error_galms); // .push_back shifts the previous content of the vector
        emse = (double) eval(magnitude(y - r_old*x*(~r_old)));
        EMSE_galms.push_back(emse); // .push_back shifts the previous content of the vector

        r_new = r_old + mu_galms*(d^(r_old*x*(~r_old)))*r_old;
        r_new = r_new*(1/eval(magnitude(r_new))); // normalizing rotor
        r_new = eval(r_new);

        r_old = r_new;

    }

    //auto r_exp = gaalet::exponential(-0.5*r_new);

pcl::PointCloud<pcl::PointXYZ>::Ptr reg_sourcePCDPtr (new pcl::PointCloud<pcl::PointXYZ>);

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;
        //iter_value = myvector[i];
        x[0] = sourcePCDPtr->points[iter_value].x;
        x[1] = sourcePCDPtr->points[iter_value].y;
        x[2] = sourcePCDPtr->points[iter_value].z;

        x_reg = r_new*x*(~r_new) - (r_new*x_cent*(~r_new) - y_cent);

        pcl::PointXYZ basic_point;
        basic_point.x = x_reg[0];
        basic_point.y = x_reg[1];
        basic_point.z = x_reg[2];
        reg_sourcePCDPtr->points.push_back(basic_point);

    }

    // SAVING ================================================================================
    //std::cout << "Number_of_Points: " << Y_PCDPtr->points.size () << std::endl;
    //std::cout << "Estimated_rotor: " << r_new << std::endl;
    //std::cout << "Estimated_rotor_exp(-0.5*rotor): " << r_exp << std::endl;

    //std::string pcd_file_to_save = "sourcekps_reg.pcd";
    pcl::io::savePCDFileBinary("sourcekps_reg.pcd", *reg_sourcePCDPtr); //saving registered source PCD

    std::ofstream output_rotor("./rotor.txt"); //saving rotor vector
    output_rotor << r_new;

    /*
    std::ofstream output_CF("./CF.txt"); //saving CF vector
    std::ostream_iterator<double> output_iterator_CF(output_CF, "\n");
    std::copy(CF_galms.begin(), CF_galms.end(), output_iterator_CF);

    std::ofstream output_CF_emse("./CF_EMSE.txt"); //saving CF_emse vector
    std::ostream_iterator<double> output_iterator_CF_emse(output_CF_emse, "\n");
    std::copy(CF_galms_emse.begin(), CF_galms_emse.end(), output_iterator_CF_emse);
    */

    std::ofstream output_MSE("./MSE.txt"); //saving MSE vector
    std::ostream_iterator<double> output_iterator_MSE(output_MSE, "\n");
    std::copy(MSE_galms.begin(), MSE_galms.end(), output_iterator_MSE);

    std::ofstream output_EMSE("./EMSE.txt"); //saving EMSE vector
    std::ostream_iterator<double> output_iterator_EMSE(output_EMSE, "\n");
    std::copy(EMSE_galms.begin(), EMSE_galms.end(), output_iterator_EMSE);


    // PLOTTING ==============================================================================


/*
    //GNU Plot
    //'-' means read from stdin.  The send1d() function sends data to gnuplot's stdin.
    gp << "set title 'Mean-Squared Error'\n";
    gp << "set xlabel 'Iterations'\n";
    gp << "set ylabel 'MSE (dB)'\n";
    gp << "set grid xtics\n";
    gp << "set grid ytics\n";
    gp << "set grid mxtics\n";
    gp << "set grid mytics\n";
    gp << "plot '-' title 'GA-LMS' with lines\n";
    gp.send1d(MSE_galms);
*/

/*
    // Visualizer routine
     boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer_before;
     viewer_before = customColourVis(targetPCDPtr,sourcePCDPtr,"Before Alignment");
     boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer_after;
     viewer_after = customColourVis(targetPCDPtr,reg_sourcePCDPtr,"After Alignment");

     while (!viewer_before->wasStopped ())
       {
         viewer_before->spinOnce (100);
         viewer_after->spinOnce (100);
         boost::this_thread::sleep (boost::posix_time::microseconds (100000));
       }
*/
}
