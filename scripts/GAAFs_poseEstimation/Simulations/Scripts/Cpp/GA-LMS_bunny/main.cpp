/* GA-LMS_bunny_steep
   This code implements the GA-LMS for the Stanford Bunny set and the GA Steepest-Descent (rank m=K). The points for several
   learning curves are calculated and provided in different txt files by the end of the execution. They are:
	- MSE curve for the GA-LMS;
	- MSE curve for the GA steepest-descent algorithm;   
	- MSE curve for the Cost Function (Eq. (5) in the paper), using ONLY THE GOOD CORRESPONDENCES. This is done to
	assess the effect of the rotor (estimated at each iteration) only at the true correspondences. It makes no sense
	to account for the bad correspondences in this curve since their points could never be correctly registered, i.e., 
	they belong to different parts of the PCDs.   

   Three txt files are proided at the end

 */
#define _USE_MATH_DEFINES
#include <boost/thread/thread.hpp>
#include <cmath>
#include <iostream>
#include <sstream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <Eigen/Eigen>
#include <iterator> // for ostream_iterator
#include <math.h>       /* log10 */
#include <stdio.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/visualization/point_cloud_color_handlers.h>
#include <fstream>
#include <string>

#include "gnuplot-iostream.h"
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

    double error_galms, cost_function_mag;
    double error_steep_plot_mag, error_steep_plot;
    double cost_function = 0;
    double mu_steep = 0;
    double mu_galms = 0;
    double K;
    int iter_value;

    std::vector<double> CF_galms;
    std::vector<double> MSE_steep;
    std::vector<double> MSE_galms;
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

    // SELECTING CORRESPONDENCES ============================================================

    // clean correspondences
    int c=0;
    string line;
    ifstream myfile (argv[3]);

    if(myfile.fail()) // checks to see if file opended
   {
     cout << "error" << endl;
     return 1; // no point continuing if the file didn't open...
   }

    if (myfile.is_open())
    {
      while ( getline (myfile,line) )
      {
        c++;
      }
      //cout << c << '\n';
      myfile.close();
    }

    double col_1[c-1];// array that can hold 'c' numbers for 1st column
    double col_2[c-1];// array that can hold 'c' numbers for 2nd column
    double col_3[c-1];// array that can hold 'c' numbers for 3rd column

      int num = 0;
      myfile.open(argv[3]);// file containing numbers in 3 columns
      getline (myfile,line);

      for (num = 0; num < c-1; ++num) // reading file
          {

             myfile >> col_1[num]; // read first column number
             myfile >> col_2[num]; // read second column number
             myfile >> col_3[num]; // read third column number

             //std::cout << col_1[num] << " " << col_2[num] << " " << col_3[num] << std::endl;

             //++num; // go to the next number

           }
      myfile.close();

    pcl::PointCloud<pcl::PointXYZ>::Ptr Y_PCDPtr (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr X_PCDPtr (new pcl::PointCloud<pcl::PointXYZ>);

    int j = 0;
    for (j = 0; j < c-1; ++j)
    {
        pcl::PointXYZ basic_point_1;
        basic_point_1.x = targetPCDPtr->points[col_2[j]].x;
        basic_point_1.y = targetPCDPtr->points[col_2[j]].y;
        basic_point_1.z = targetPCDPtr->points[col_2[j]].z;
        Y_PCDPtr->points.push_back(basic_point_1);

        pcl::PointXYZ basic_point_2;
        basic_point_2.x = sourcePCDPtr->points[col_1[j]].x;
        basic_point_2.y = sourcePCDPtr->points[col_1[j]].y;
        basic_point_2.z = sourcePCDPtr->points[col_1[j]].z;
        X_PCDPtr->points.push_back(basic_point_2);

    }

    // Selecting only the good (true) correspondences. This is done to calculate the time evolution
    //of the cost function.
    int c_good=0;
    string line_good;
    ifstream myfile_good (argv[4]);

    if(myfile_good.fail()) // checks to see if file opended
   {
     cout << "error" << endl;
     return 1; // no point continuing if the file didn't open...
   }

    if (myfile_good.is_open())
    {
      while ( getline (myfile_good,line_good) )
      {
        c_good++;
      }
      //std::cout << "c_good = " << c_good << "\n";
      myfile_good.close();
    }

    double col_1_good[c_good-1];// array that can hold 'c' numbers for 1st column
    double col_2_good[c_good-1];// array that can hold 'c' numbers for 2nd column
    double col_3_good[c_good-1];// array that can hold 'c' numbers for 3rd column

      int num_good = 0;
      myfile_good.open(argv[4]);// file containing numbers in 3 columns
      getline (myfile_good,line_good);

      for (num_good = 0; num_good < (c_good-1); ++num_good) // reading file
          {

             myfile_good >> col_1_good[num_good]; // read first column number
             myfile_good >> col_2_good[num_good]; // read second column number
             myfile_good >> col_3_good[num_good]; // read third column number

             //std::cout << col_1[num] << " " << col_2[num] << " " << col_3[num] << std::endl;

             //++num; // go to the next number

           }
      myfile_good.close();

    pcl::PointCloud<pcl::PointXYZ>::Ptr Y_PCD_goodPtr (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr X_PCD_goodPtr (new pcl::PointCloud<pcl::PointXYZ>);

    int j_good = 0;
    for (j_good = 0; j_good < c_good-1; ++j_good)
    {
        pcl::PointXYZ basic_point_1;
        basic_point_1.x = targetPCDPtr->points[col_2_good[j_good]].x;
        basic_point_1.y = targetPCDPtr->points[col_2_good[j_good]].y;
        basic_point_1.z = targetPCDPtr->points[col_2_good[j_good]].z;
        Y_PCD_goodPtr->points.push_back(basic_point_1);

        pcl::PointXYZ basic_point_2;
        basic_point_2.x = sourcePCDPtr->points[col_1_good[j_good]].x;
        basic_point_2.y = sourcePCDPtr->points[col_1_good[j_good]].y;
        basic_point_2.z = sourcePCDPtr->points[col_1_good[j_good]].z;
        X_PCD_goodPtr->points.push_back(basic_point_2);

    }

    //=======================================================================================
    /*
    Code for scrambling the correspondences each time the binary is called by Matlab. Only
    the loops related to the cleaned correspondences are being scrambled. The ones related
    to the good correspondences stay untouched.
    */
    for (size_t i=1; i < Y_PCDPtr->points.size (); ++i) myvector.push_back(i);
    std::srand ( unsigned ( std::time(0) ) );
    std::random_shuffle ( myvector.begin(), myvector.end(), myrandom);

    // CENTROIDS ============================================================================
    em::mv<1, 2, 4>::type y_sum{0, 0, 0};
    em::mv<1, 2, 4>::type x_sum{0, 0, 0};
    em::mv<1, 2, 4>::type y_cent{0, 0, 0};
    em::mv<1, 2, 4>::type x_cent{0, 0, 0};
    em::mv<1, 2, 4>::type y_good_sum{0, 0, 0};
    em::mv<1, 2, 4>::type x_good_sum{0, 0, 0};
    em::mv<1, 2, 4>::type y_good_cent{0, 0, 0};
    em::mv<1, 2, 4>::type x_good_cent{0, 0, 0};

    // calculating centroids
    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;

        y_sum[0] += Y_PCDPtr->points[iter_value].x;
        y_sum[1] += Y_PCDPtr->points[iter_value].y;
        y_sum[2] += Y_PCDPtr->points[iter_value].z;
        //y_sum += Y_PCDPtr->points[i];
    }

    y_cent[0] = y_sum[0]/(Y_PCDPtr->points.size ());
    y_cent[1] = y_sum[1]/(Y_PCDPtr->points.size ());
    y_cent[2] = y_sum[2]/(Y_PCDPtr->points.size ());

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;

        x_sum[0] += X_PCDPtr->points[iter_value].x;
        x_sum[1] += X_PCDPtr->points[iter_value].y;
        x_sum[2] += X_PCDPtr->points[iter_value].z;
        //x_sum += X_PCDPtr->points[i];
    }

    x_cent[0] = x_sum[0]/(X_PCDPtr->points.size ());
    x_cent[1] = x_sum[1]/(X_PCDPtr->points.size ());
    x_cent[2] = x_sum[2]/(X_PCDPtr->points.size ());

    for (size_t i = 0; i < Y_PCD_goodPtr->points.size (); ++i)
    {
        y_good_sum[0] += Y_PCD_goodPtr->points[i].x;
        y_good_sum[1] += Y_PCD_goodPtr->points[i].y;
        y_good_sum[2] += Y_PCD_goodPtr->points[i].z;
        //y_sum += Y_PCDPtr->points[i];
    }

    y_good_cent[0] = y_good_sum[0]/(Y_PCD_goodPtr->points.size ());
    y_good_cent[1] = y_good_sum[1]/(Y_PCD_goodPtr->points.size ());
    y_good_cent[2] = y_good_sum[2]/(Y_PCD_goodPtr->points.size ());

    for (size_t i = 0; i < X_PCD_goodPtr->points.size (); ++i)
    {
        x_good_sum[0] += X_PCD_goodPtr->points[i].x;
        x_good_sum[1] += X_PCD_goodPtr->points[i].y;
        x_good_sum[2] += X_PCD_goodPtr->points[i].z;
        //x_sum += X_PCDPtr->points[i];
    }

    x_good_cent[0] = x_good_sum[0]/(X_PCD_goodPtr->points.size ());
    x_good_cent[1] = x_good_sum[1]/(X_PCD_goodPtr->points.size ());
    x_good_cent[2] = x_good_sum[2]/(X_PCD_goodPtr->points.size ());


    // Generating the new point clouds
    pcl::PointCloud<pcl::PointXYZ>::Ptr Y_PCDPtr_cent (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr X_PCDPtr_cent (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr Y_PCD_goodPtr_cent (new pcl::PointCloud<pcl::PointXYZ>);
    pcl::PointCloud<pcl::PointXYZ>::Ptr X_PCD_goodPtr_cent (new pcl::PointCloud<pcl::PointXYZ>);

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;

        pcl::PointXYZ basic_point_3;
        basic_point_3.x = Y_PCDPtr->points[iter_value].x - y_cent[0];
        basic_point_3.y = Y_PCDPtr->points[iter_value].y - y_cent[1];
        basic_point_3.z = Y_PCDPtr->points[iter_value].z - y_cent[2];
        Y_PCDPtr_cent->points.push_back(basic_point_3);

    }

    for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;

        pcl::PointXYZ basic_point_4;
        basic_point_4.x = X_PCDPtr->points[iter_value].x - x_cent[0];
        basic_point_4.y = X_PCDPtr->points[iter_value].y - x_cent[1];
        basic_point_4.z = X_PCDPtr->points[iter_value].z - x_cent[2];
        X_PCDPtr_cent->points.push_back(basic_point_4);
    }

    for (size_t i = 0; i < Y_PCD_goodPtr->points.size (); ++i)
    {
        pcl::PointXYZ basic_point_3;
        basic_point_3.x = Y_PCD_goodPtr->points[i].x - y_good_cent[0];
        basic_point_3.y = Y_PCD_goodPtr->points[i].y - y_good_cent[1];
        basic_point_3.z = Y_PCD_goodPtr->points[i].z - y_good_cent[2];
        Y_PCD_goodPtr_cent->points.push_back(basic_point_3);

    }

    for (size_t i = 0; i < X_PCD_goodPtr->points.size (); ++i)
    {
        pcl::PointXYZ basic_point_4;
        basic_point_4.x = X_PCD_goodPtr->points[i].x - x_good_cent[0];
        basic_point_4.y = X_PCD_goodPtr->points[i].y - x_good_cent[1];
        basic_point_4.z = X_PCD_goodPtr->points[i].z - x_good_cent[2];
        X_PCD_goodPtr_cent->points.push_back(basic_point_4);
    }



    //=======================================================================================

    std::stringstream str_mu_steep(argv[5]);
    str_mu_steep >> mu_steep;

    std::stringstream str_mu_galms(argv[6]);
    str_mu_galms >> mu_galms;


    // Initializing rotors in gaalet
    em::mv<0, 3, 5, 6>::type r_old{0.5, 0.5, -0.5, 0.5};
    em::mv<0, 3, 5, 6>::type r_new{0, 0, 0, 0};
    em::mv<0, 3, 5, 6>::type r_steep_old{0.5, 0.5, -0.5, 0.5};
    em::mv<0, 3, 5, 6>::type r_steep_new{0, 0, 0, 0};

    // Initializing auxiliary points in gaalet
    em::mv<1, 2, 4>::type y{0, 0, 0};   
    em::mv<1, 2, 4>::type x{0, 0, 0};    
    em::mv<1, 2, 4>::type x_reg{0, 0, 0};
    em::mv<1, 2, 4>::type y_CF{0, 0, 0};    
    em::mv<1, 2, 4>::type x_CF{0, 0, 0};
    em::mv<1, 2, 4>::type y_steep{0, 0, 0};
    em::mv<1, 2, 4>::type x_steep{0, 0, 0};

    em::mv<0,1,2,3,4,5,6,7>::type error_steep{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0,1,2,3,4,5,6,7>::type zero_multivector{0, 0, 0, 0, 0, 0, 0, 0};

    K = Y_PCDPtr->points.size (); //Number of points in the PCDs


//Begining of adaptation loop
for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;

        y[0] = Y_PCDPtr_cent->points[iter_value].x;
        y[1] = Y_PCDPtr_cent->points[iter_value].y;
        y[2] = Y_PCDPtr_cent->points[iter_value].z;

        x[0] = X_PCDPtr_cent->points[iter_value].x;
        x[1] = X_PCDPtr_cent->points[iter_value].y;
        x[2] = X_PCDPtr_cent->points[iter_value].z;

        //Adaptive Filters are found below
        for (size_t n = 0; n < Y_PCD_goodPtr_cent->points.size (); ++n) //To calculate the time evolution of the cost function
            {

                y_CF[0] = Y_PCD_goodPtr_cent->points[n].x;
                y_CF[1] = Y_PCD_goodPtr_cent->points[n].y;
                y_CF[2] = Y_PCD_goodPtr_cent->points[n].z;

                x_CF[0] = X_PCD_goodPtr_cent->points[n].x;
                x_CF[1] = X_PCD_goodPtr_cent->points[n].y;
                x_CF[2] = X_PCD_goodPtr_cent->points[n].z;

                cost_function_mag = (double) eval(magnitude(y_CF - r_old*x_CF*(~r_old)));
                cost_function += pow(cost_function_mag,2);

            }
        CF_galms.push_back(10*log10((1/K)*cost_function)); // appending to the cost function (CF) vector
        cost_function = 0;


        //Steepest-Descent ===============================================
        //Calculating the error for the steepest-descent algorithm (when the AF uses all the vailable K correspondence pairs)
        for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
            {
                iter_value = *it;

                y_steep[0] = Y_PCDPtr_cent->points[iter_value].x;
                y_steep[1] = Y_PCDPtr_cent->points[iter_value].y;
                y_steep[2] = Y_PCDPtr_cent->points[iter_value].z;

                x_steep[0] = X_PCDPtr_cent->points[iter_value].x;
                x_steep[1] = X_PCDPtr_cent->points[iter_value].y;
                x_steep[2] = X_PCDPtr_cent->points[iter_value].z;

                error_steep_plot_mag = (double) eval(magnitude(y_steep - (r_steep_old*x_steep*(~r_steep_old))));
                error_steep_plot += pow(error_steep_plot_mag,2);
                error_steep = error_steep + (y_steep^(r_steep_old*x_steep*(~r_steep_old))); //error to be used in the steepest-descent update rule
                //error_steep += pow(error_steep_mag,2);
            }
        //std::cout << "error_steep" << error_steep << std::endl;
        MSE_steep.push_back(10*log10((1/K)*error_steep_plot)); // appending to the steepest-descent error
        error_steep_plot = 0;

        r_steep_new = r_steep_old + mu_steep*(4/K)*error_steep*r_steep_old;
        r_steep_new = r_steep_new*(1/eval(magnitude(r_steep_new)));
        r_steep_new = eval(r_steep_new);

        r_steep_old = r_steep_new;

        error_steep = zero_multivector;

        //GA-LMS ===============================================
        error_galms = (double) eval(magnitude(y - r_old*x*(~r_old)));
        MSE_galms.push_back(error_galms); // .push_back shifts the previous content of the vector

        r_new = r_old + mu_galms*(y^(r_old*x*(~r_old)))*r_old;
        r_new = r_new*(1/eval(magnitude(r_new)));
        r_new = eval(r_new);

        r_old = r_new;
    }

pcl::PointCloud<pcl::PointXYZ>::Ptr reg_sourcePCDPtr (new pcl::PointCloud<pcl::PointXYZ>);

//Registering Source PCD
for (std::vector<int>::iterator it=myvector.begin(); it!=myvector.end(); ++it)
    {
        iter_value = *it;

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
    std::cout << "Number_of_Points: " << Y_PCDPtr->points.size () << std::endl;
    std::cout << "Estimated_rotor_galms: " << r_new << std::endl;
    std::cout << "Estimated_rotor_steep: " << r_steep_new << std::endl;

    pcl::io::savePCDFileBinary("sourcekps_reg.pcd", *reg_sourcePCDPtr); //saving registered source PCD

    std::ofstream output_rotor_steep("./rotor_steep.txt"); //saving rotor_steep
    output_rotor_steep << r_steep_new;

    std::ofstream output_rotor("./rotor.txt"); //saving rotor
    output_rotor << r_new;

    std::ofstream output_CF("./CF.txt"); //saving CF vector
    std::ostream_iterator<double> output_iterator_CF(output_CF, "\n");
    std::copy(CF_galms.begin(), CF_galms.end(), output_iterator_CF);

    std::ofstream output_MSE_steep("./MSE_steep.txt"); //saving MSE_steep vector
    std::ostream_iterator<double> output_iterator_MSE_steep(output_MSE_steep, "\n");
    std::copy(MSE_steep.begin(), MSE_steep.end(), output_iterator_MSE_steep);

    std::ofstream output_MSE("./MSE.txt"); //saving MSE vector
    std::ostream_iterator<double> output_iterator_MSE(output_MSE, "\n");
    std::copy(MSE_galms.begin(), MSE_galms.end(), output_iterator_MSE);




    // PLOTTING ==============================================================================
/*
    //gp << "set xrange [-2:2]\nset yrange [-2:2]\n";
    // '-' means read from stdin.  The send1d() function sends data to gnuplot's stdin.
    gp << "set title 'Mean-Squared Error'\n";
    gp << "set xlabel 'Iterations'\n";
    gp << "set ylabel 'MSE (dB)'\n";
    gp << "set grid xtics\n";
    gp << "set grid ytics\n";
    gp << "set grid mxtics\n";
    gp << "set grid mytics\n";
    gp << "plot '-' title 'GA-LMS' with lines\n";
    gp.send1d(MSE_galms);

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

