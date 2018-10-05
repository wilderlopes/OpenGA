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

int main(int argc, char* argv[])
{

    double error_galms, emse_galms, msd_galms;
    double MSE_theory = 0, EMSE_theory = 0;
    double mu_galms = 0;
    double realizations = 10;
    double iterations = 1000;
    double var_v = 0; // measurement noise variance
    double var_q = 0; // random walk variance
    double corr_input = 0.95; // level of correlation between input entries
    int M = 4; //number of taps

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

    //typedef gaalet::algebra<gaalet::signature<3,0> > em;


    // Initializing multivectors in gaalet
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type x{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type d{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type v{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type q{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type w_old_entry{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type w_new_entry{0, 0, 0, 0, 0, 0, 0, 0};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type wo{0.55, 0, 1, 2, 0.71, 1.3, 4.5, 3};
    em::mv<0, 1, 2, 3, 4, 5, 6, 7>::type entry{1,0,0,0,0,0,0,0};

    //Inititalizing arrays of multivectors
    std::vector<mvType> u_i; //Array of regressors
    std::vector<mvType> u_i_old; //Array of regressors from past time instant
    std::vector<mvType> wo_i; //Array - plant model
    std::vector<mvType> w_old; //Array - weight vector (old)
    std::vector<mvType> w_new; //Array - weight vector (new)
    std::vector<mvType> w_avg; //Array - weight vector averaged over realizations

    u_i.resize(M);
    u_i_old.resize(M);
    wo_i.resize(M);
    w_old.resize(M);
    w_new.resize(M);
    w_avg.resize(M);

    std::default_random_engine u;
    std::normal_distribution<double> normaldist(0,1); //Gaussian Distribution, mean=0, stddev=1;

    std::vector<double> MSE_galms_avg;
    std::vector<double> EMSE_galms_avg;

    // Resizing the following vectors to allocate memmory. Otherwise
    // a 'segmentation fault' occurs.
    MSE_galms_avg.resize(iterations);
    EMSE_galms_avg.resize(iterations);


for (size_t j = 0; j < realizations; ++j)
{

    std::cout << "Realization = " << j+1 << "of" << realizations << std::endl;

    for (int n=0; n < M; n++) //populating the arrays - regressor and noise
    {
        for (size_t j = 0; j < 8; ++j)
        {
            x[j] = normaldist(u);
        }
        u_i.at(n)  = x;
        u_i_old.at(n)  = x;
        wo_i.at(n) = wo;
        w_old.at(n) = w_old_entry;
        w_new.at(n) = w_new_entry;
    }

    // Redefining MSE_galms and EMSE_galms before each realization
    std::vector<double> MSE_galms;
    std::vector<double> EMSE_galms;

for (size_t i = 0; i < iterations; ++i)
    {

        // Desirable output
        for (size_t j = 0; j < 8; ++j)
        {
            v[j] = normaldist(u); // generates normally distributed samples for noise
        }
        d = array_prod(reverse_array(u_i),wo_i) + sqrt(var_v)*v;

        //GA-LMS
        error_galms = (double) eval(magnitude(d - array_prod(reverse_array(u_i),w_old)));
        emse_galms = (double) eval(magnitude(array_prod(reverse_array(u_i),array_sub(wo_i,w_old))));
        //msd_galms = (double) eval(magnitude(array_sub(wo_i,w_old)));
        MSE_galms.push_back(pow(error_galms,2)); // .push_back shifts the previous content of the vector
        EMSE_galms.push_back(pow(emse_galms,2)); // .push_back shifts the previous content of the vector
        //MSD_galms.push_back(10*log10(pow(msd_galms,2))); // .push_back shifts the previous content of the vector
        w_new = array_sum(w_old,array_prod(mu_galms,array_prod(u_i,(d - array_prod(reverse_array(u_i),w_old)))));

        // Random walk
        for (int n=0; n < M; n++)
        {
          for (size_t j = 0; j < 8; ++j)
          {
            q[j] = normaldist(u); // generates normally distributed samples for random-walk noise
          }
          w_new.at(n) = w_new.at(n) + sqrt(var_q)*q;
        }

        w_old = w_new;

        u_i_old = u_i;

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
        for (int n=0; n < M; n++)
        {
            for (size_t j = 0; j < 8; ++j)
            {
                x[j] = normaldist(u);
            }
            u_i.at(n) = x;
        }

        //std::cout << "new regressor = " << std::endl;
        //for (int n = 0; n < M; ++n)
        //std::cerr << u_i[n] << std::endl;
        //=========================================================

        // Correlated input - Auto-regressive (AR) Process ========
        if (corr_input > 0)
        {
          // Building up the Regressor vector. Note that entry n=0 is left intact.
          for (int n=1; n < M; n++)
          {
            u_i.at(n) = sqrt(1 - pow(corr_input, 2))*u_i.at(n) + corr_input*u_i_old.at(n);
          }
        }
        //=========================================================

    }

    for (size_t r = 0; r < iterations; ++r)
    {
      MSE_galms_avg[r] = MSE_galms_avg[r] + MSE_galms[r]/realizations;
      EMSE_galms_avg[r] = EMSE_galms_avg[r] + EMSE_galms[r]/realizations;
    }

    w_avg = array_sum(w_avg,array_prod((1/realizations),w_new)); // averaging estimated w
}

    MSE_theory  = (8*var_v) + mu_galms*(M*8)*(8*var_v)/(2-mu_galms*(M*8));
    EMSE_theory = mu_galms*(M*8)*(8*var_v)/(2-mu_galms*(M*8));

    std::cout << "Iterations = " << iterations << std::endl;
    std::cout << "Number of taps = " << M << std::endl;
    std::cout << "Optimal wo = " << std::endl;
    for (int n = 0; n < M; ++n)
    std::cerr << wo_i[n] << std::endl;
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

    std::ofstream output_EMSE_galms("./EMSE_galms.out"); //saving EMSE_galms vector
    std::ostream_iterator<double> output_iterator_EMSE_galms(output_EMSE_galms, "\n");
    std::copy(EMSE_galms_avg.begin(), EMSE_galms_avg.end(), output_iterator_EMSE_galms);

    std::ofstream output_EMSE_theory("./EMSE_theory.out"); //saving EMSE_theory bound
    output_EMSE_theory << EMSE_theory << '\n';

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
