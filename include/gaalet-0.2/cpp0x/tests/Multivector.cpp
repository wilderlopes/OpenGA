#include "gaalet.h"

typedef gaalet::algebra<gaalet::signature<3,0>, double> iem;
typedef gaalet::algebra<gaalet::signature<3,0>, double> dem;

int main()
{
   iem::mv<1,2,4>::type i = {1,2,3};
   std::cout << "i: " << i << std::endl;
   std::cout << "i.element<0>: " << i.element<0>() << std::endl;

   dem::mv<1,2,4>::type d = {1.1,2.2,3.3};
   std::cout << "d: " << d << std::endl;
   std::cout << "d.element<0>: " << d.element<0>() << std::endl;

}
