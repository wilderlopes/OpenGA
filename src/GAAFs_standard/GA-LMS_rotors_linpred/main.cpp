// Linear predictor GA-LMS_rotor

#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <sstream>
#include <iterator> // for ostream_iterator
#include <math.h>       /* log10 */
#include <stdio.h>

#include "gnuplot-iostream.h"
#include "gaalet/include/gaalet.h"
#include "array_operators.h"

using namespace std;

//TODO: substitute the numbers '4' by the size of the multivector.

int main(int argc, char* argv[])
{

    double error_galms, emse_galms, msd_galms;
    double MSE_theory = 0, EMSE_theory = 0;
    double mu_galms = 5e-3;
    double realizations = 10;
    double iterations = 1000;
    double var_v = 0;
    double var_q = 0; // random walk variance
    double corr_input = 0.95; // level of correlation between input entries
    int M = 4; //number of taps
    int n_rows = 10000;
    int n_cols = 4;
    double data[n_rows][n_cols];

    std::stringstream str_M(argv[1]);
    str_M >> M;

    std::stringstream str_realizations(argv[2]);
    str_realizations >> realizations;

    std::stringstream str_iterations(argv[3]);
    str_iterations >> iterations;

    std::stringstream str_mu_galms(argv[4]);
    str_mu_galms >> mu_galms;

    std::stringstream str_var_v(argv[5]);
    str_var_v >> var_v;

    std::stringstream str_var_q(argv[6]);
    str_var_q >> var_q;

    std::stringstream str_corr_input(argv[7]);
    str_corr_input >> corr_input;

    // Loading data
    // std::ifstream file("/home/wilder/dev/OpenGA/data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS.csv");
    std::ifstream file("/home/openga/data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS.csv");

    for(int row = -1; row < n_rows; ++row)
    {
      std::string line;
      std::getline(file, line);

      if (row >= 0)
      {
        // if ( !file.good() )
        //     break;

        std::stringstream iss(line);

        for (int col = -1; col < n_cols; ++col)
        {
            std::string val;
            std::getline(iss, val, ',');
            if (col >= 0)
            {
              // Hat to comment out lines below otherwise conversion of negative
              // strings doesn't happen.
              // if ( !iss.good() )
              //     break;
              std::stringstream convertor(val);
              convertor >> data[row][col];
            }
        }
      }
    }

    // Print data
    std::cout << "data array = \n" << std::endl;
    for (int i = 0; i < n_rows; ++i)
    {
        for (int j = 0; j < n_cols; ++j)
        {
            std::cout << data[i][j] << ' ';
        }
        std::cout << std::endl;
    }




    // Initializing multivectors in gaalet
    mvType x{0, 0, 0, 0};
    mvType d{0, 0, 0, 0};
    mvType y{0, 0, 0, 0};
    mvType v{0, 0, 0, 0};
    mvType w_old_entry{0, 0, 0, 0};
    mvType w_new_entry{0, 0, 0, 0};
    mvType Ui{0, 0, 0, 0};

    //Inititalizing arrays of multivectors
    std::vector<mvType> u_i; //Array of regressors
    // std::vector<mvType> Ui; //Array - plant model
    std::vector<mvType> w_old; //Array - weight vector (old)
    std::vector<mvType> w_new; //Array - weight vector (new)
    std::vector<mvType> w_avg; //Array - weight vector averaged over realizations

    u_i.resize(M);
    // Ui.resize(M);
    w_old.resize(M);
    w_new.resize(M);
    w_avg.resize(M);

    std::default_random_engine u;
    std::normal_distribution<double> normaldist(0,1); //Gaussian Distribution, mean=0, stddev=1;

    std::vector<double> MSE_galms_avg;
    // std::vector<double> EMSE_galms_avg;
    // std::vector<double[iterations]> y_galms_avg;
    std::vector<double> y_galms_avg_0;
    std::vector<double> y_galms_avg_3;
    std::vector<double> y_galms_avg_5;
    std::vector<double> y_galms_avg_6;

    // Resizing the following vectors to allocate memmory. Otherwise
    // a 'segmentation fault'
    MSE_galms_avg.resize(iterations);
    // EMSE_galms_avg.resize(iterations);
    y_galms_avg_0.resize(iterations);
    y_galms_avg_3.resize(iterations);
    y_galms_avg_5.resize(iterations);
    y_galms_avg_6.resize(iterations);

for (size_t j = 0; j < realizations; ++j)
{

    std::cout << "Realization = " << j+1 << "of" << realizations << std::endl;

    // Redefining MSE_galms and EMSE_galms before each realization
    std::vector<double> MSE_galms;
    // std::vector<double> EMSE_galms;
    // std::vector<double[iterations]> y_galms;
    std::vector<double> y_galms_0;
    std::vector<double> y_galms_3;
    std::vector<double> y_galms_5;
    std::vector<double> y_galms_6;

    for (int n=0; n < M; n++) //populating the arrays - regressor and noise
    {
      w_old.at(n) = w_old_entry;
      w_new.at(n) = w_new_entry;
    }

    for (size_t i = 0; i < iterations; ++i)
    {
        for (int n=i; n < (i + M); n++) //populating the arrays - regressor and noise
        {
            // std::cout << "n = " << n << std::endl;
            for (size_t jj = 0; jj < 4; ++jj)
            {
                x[jj] = data[n][jj];
                // x[j] = normaldist(u);
                //v[j] = normaldist(u); // generates normally distributed samples for noise
            }
            u_i.at(n-i) = x;
            // std::cout << "x = " << x << std::endl;
        }
        std::cout << "u_i = " << std::endl;
        for (int nn = 0; nn < M; ++nn)
        std::cerr << u_i[nn] << std::endl;

        for (size_t jk = 0; jk < 4; ++jk)
        {
            Ui[jk] = data[i+M][jk];
        }

        std::cout << "Ui = " << Ui << std::endl;

        // Desirable output
        for (size_t jkk = 0; jkk < 4; ++jkk)
        {
            v[jkk] = normaldist(u); // generates normally distributed samples for noise
        }
        d = Ui + sqrt(var_v)*v;

        // std::cout << "d = " << d << std::endl;

        //GA-LMS
        y = array_prod(reverse_array(u_i),w_old);
        std::cout << "y = " << y << std::endl;
        std::cout << "y[3] = " << y[3] << std::endl;
        // std::cout << "grade(y) = " << grade<0>(y) << std::endl;

        error_galms = (double) eval(magnitude(d - y));
        // emse_galms = (double) eval(magnitude(array_prod(reverse_array(u_i),array_sub(wo_i,w_old))));
        //msd_galms = (double) eval(magnitude(array_sub(wo_i,w_old)));
        MSE_galms.push_back(pow(error_galms,2)); // .push_back shifts the previous content of the vector
        // y_galms.push_back(y[]);
        y_galms_0.push_back(y[0]);
        y_galms_3.push_back(y[1]);
        y_galms_5.push_back(y[2]);
        y_galms_6.push_back(y[3]);
        // EMSE_galms.push_back(pow(emse_galms,2)); // .push_back shifts the previous content of the vector
        //MSD_galms.push_back(10*log10(pow(msd_galms,2))); // .push_back shifts the previous content of the vector
        w_new = array_sum(w_old,array_prod(mu_galms,array_prod(u_i,(d - array_prod(reverse_array(u_i),w_old)))));

        w_old = w_new;

        /*
        //Regenerating regressor - shift register =================
        for (size_t j = 0; j < 8; ++j)
        {
            x[j] = normaldist(u);
            v[j] = normaldist(u);
        }

        std::rotate(u_i.begin(), u_i.begin()+1, u_i.end());
        //std::cout << "regressor_after_rotation = " << std::endl;
        //for (int n = 0; n < M; ++n)
        //std::cerr << u_i[n] << std::endl;

        u_i.at(M-1) = x;//replaces element in the back of u_i
        //std::cout << "regressor_after_replacement = " << std::endl;
        //for (int n = 0; n < M; ++n)
        //std::cerr << u_i[n] << std::endl;
        //=========================================================
        */

        //Regenerating regressor - no shift register ==============
        // for (int n=0; n < M; n++)
        // {
        //     for (size_t j = 0; j < 4; ++j)
        //     {
        //         x[j] = normaldist(u);
        //     }
        //     u_i.at(n)  = x;
        // }

        //std::cout << "new regressor = " << std::endl;
        //for (int n = 0; n < M; ++n)
        //std::cerr << u_i[n] << std::endl;
        //=========================================================

    }

    for (size_t r = 0; r < iterations; ++r)
    {
        std::cout << "MSE_galms[r] = " << MSE_galms[r] << std::endl;

        MSE_galms_avg[r] = MSE_galms_avg[r] + MSE_galms[r]/realizations;
        // EMSE_galms_avg[r] = EMSE_galms_avg[r] + EMSE_galms[r]/realizations;
        y_galms_avg_0[r] = y_galms_avg_0[r] + y_galms_0[r]/realizations;
        y_galms_avg_3[r] = y_galms_avg_3[r] + y_galms_3[r]/realizations;
        y_galms_avg_5[r] = y_galms_avg_5[r] + y_galms_5[r]/realizations;
        y_galms_avg_6[r] = y_galms_avg_6[r] + y_galms_6[r]/realizations;

    }

    w_avg = array_sum(w_avg,array_prod((1/realizations),w_new)); // averaging estimated w

}


    MSE_theory  = (4*var_v) + mu_galms*(M*4)*(4*var_v)/(2-mu_galms*(M*4));
    // EMSE_theory = mu_galms*(M*4)*(4*var_v)/(2-mu_galms*(M*4));

    std::cout << "Iterations = " << iterations << std::endl;
    std::cout << "Number of taps = " << M << std::endl;
    // std::cout << "Optimal wo = " << std::endl;
    // for (int n = 0; n < M; ++n)
    // std::cerr << wo_i[n] << std::endl;
    std::cout << "Estimated w = " << std::endl;
    for (int n = 0; n < M; ++n)
    std::cerr << w_new[n] << std::endl;
    std::cout << "w averaged over realizations = " << std::endl;
    for (int n = 0; n < M; ++n)
    std::cerr << w_avg[n] << std::endl;


    // SAVING ==============================================================================
    std::ofstream output_MSE_galms("./MSE_galms.out"); //saving MSE_galms vector
    std::ostream_iterator<double> output_iterator_MSE_galms(output_MSE_galms, "\n");
    std::copy(MSE_galms_avg.begin(), MSE_galms_avg.end(), output_iterator_MSE_galms);

    std::ofstream output_y_galms_0("./y_galms_0.out"); //saving y_galms_0 vector
    std::ostream_iterator<double> output_iterator_y_galms_0(output_y_galms_0, "\n");
    std::copy(y_galms_avg_0.begin(), y_galms_avg_0.end(), output_iterator_y_galms_0);

    std::ofstream output_y_galms_3("./y_galms_3.out"); //saving y_galms_0 vector
    std::ostream_iterator<double> output_iterator_y_galms_3(output_y_galms_3, "\n");
    std::copy(y_galms_avg_3.begin(), y_galms_avg_3.end(), output_iterator_y_galms_3);

    std::ofstream output_y_galms_5("./y_galms_5.out"); //saving y_galms_0 vector
    std::ostream_iterator<double> output_iterator_y_galms_5(output_y_galms_5, "\n");
    std::copy(y_galms_avg_5.begin(), y_galms_avg_5.end(), output_iterator_y_galms_5);

    std::ofstream output_y_galms_6("./y_galms_6.out"); //saving y_galms_0 vector
    std::ostream_iterator<double> output_iterator_y_galms_6(output_y_galms_6, "\n");
    std::copy(y_galms_avg_6.begin(), y_galms_avg_6.end(), output_iterator_y_galms_6);

    // std::ofstream output_EMSE_galms("./EMSE_galms.out"); //saving EMSE_galms vector
    // std::ostream_iterator<double> output_iterator_EMSE_galms(output_EMSE_galms, "\n");
    // std::copy(EMSE_galms_avg.begin(), EMSE_galms_avg.end(), output_iterator_EMSE_galms);

    // std::ofstream output_EMSE_theory("./EMSE_theory.out"); //saving EMSE_theory bound
    // output_EMSE_theory << EMSE_theory << '\n';

    std::ofstream output_MSE_theory("./MSE_theory.out"); //saving MSE_theory bound
    output_MSE_theory << MSE_theory << '\n';

    std::ofstream output_w_galms("./w_galms.out"); //saving w_avg array
    for (int n = 0; n < M; ++n)
    {
       output_w_galms << w_avg[n] << '\n'; // saves w_avg. Each line is a multivector
    }

    // PLOTTING ==============================================================================

    //gp << "set xrange [-2:2]\nset yrange [-2:2]\n";
    // '-' means read from stdin.  The send1d() function sends data to gnuplot's stdin.
//    gp << "set title 'Learning Curves - GA-LMS'\n";
//    gp << "set xlabel 'Iterations'\n";
//    gp << "set ylabel 'MSE (dB)'\n";
//    gp << "set grid xtics\n";
//    gp << "set grid ytics\n";
//    gp << "set grid mxtics\n";
//    gp << "set grid mytics\n";
//    gp << "plot '-' title 'MSE' with lines, '-' title 'EMSE' with lines, '-' title 'MSE - Theory' with lines, '-' title 'EMSE - Theory' with lines\n";
//    gp.send1d(MSE_galms);
//    gp.send1d(EMSE_galms);
//    gp.send1d(MSE_theory);
//    gp.send1d(EMSE_theory);

}
