#include "gaalet.h"

typedef gaalet::algebra<gaalet::signature<3,0>> em;
typedef gaalet::algebra<gaalet::signature<4,1>> cm;

int main()
{
   typedef gaalet::metric_combination_traits<em::metric,cm::metric>::metric emcm;

   std::cout << "Combined em, cm: p: " << emcm::p << ", q: " << emcm::q << ", emcm.r: " << emcm::r << std::endl;
}
