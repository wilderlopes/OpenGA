#include "gaalet.h"

typedef gaalet::algebra<gaalet::signature<3,0>> em;
static em::mv<0x01>::type e1 = {1.0};
static em::mv<0x02>::type e2 = {1.0};
static em::mv<0x04>::type e3 = {1.0};

int main()
{
   auto S = -0.5*M_PI*(e1^e2);
   auto R = exp(0.5*S);

   em::mv<1,2,4>::type a = {1.6, 3.2, 5.5}; 
   auto b = eval(grade<1>(R*a*(~R)));

   std::cout << "S: " << S << ", R: " << R << std::endl;
   std::cout << "a: " << a << ", b: " << b << std::endl;
}
