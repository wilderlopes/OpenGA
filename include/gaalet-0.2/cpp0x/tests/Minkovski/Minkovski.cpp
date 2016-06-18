#include "gaalet/include/gaalet.h"
#include <cmath>

//space-time algebra
int main()
{
   typedef gaalet::algebra<gaalet::signature<3,1>> st;
   st::mv<0x01>::type e1 = {1.0, 2 , 3};
   st::mv<0x02>::type e2 = {1.0};
   st::mv<0x04>::type e3 = {1.0};
   st::mv<0x08>::type et = {1.0};

   //sp::mv<0x00>::type one = {1.0};
   //std::cout << "sin(one): " << sin(one) << std::endl;

   //sp::mv<0x0f>::type I = e1*e2*e3*et;
   //auto I_expr = e1*e2*e3*et;
   //auto I_mv = eval(e1*e2*e3*et);
   //std::cout << "I_expr: " << I_expr << ", I_mv[0]: " << I_mv[0] << std::endl;
   //sp::mv<0x07>::type i = e1*e2*e3;

   std::cout << "e1: " << e1 << std::endl;
   std::cout << "e2: " << e2 << std::endl;
   std::cout << "e3: " << e3 << std::endl;
   std::cout << "et: " << et << std::endl;
   std::cout << "e1*e1: " << e1*e1 << std::endl;
   std::cout << "e2*e2: " << e2*e2 << std::endl;
   std::cout << "e3*e3: " << e3*e3 << std::endl;
   std::cout << "et*et: " << et*et << std::endl;
   std::cout << "e1*e2: " << e1*e2 << std::endl;
   std::cout << "e1*e3: " << e1*e3 << std::endl;
   std::cout << "e1*et: " << e1*et << std::endl;

   std::cout << "et*conjugate(et): " << et*conjugate(et) << std::endl;
   std::cout << "st_point*conjugate(st_point): " << (e1 + e2 + e3 + et)*conjugate(e1 + e2 + e3 + et) << std::endl;
   

 } 
