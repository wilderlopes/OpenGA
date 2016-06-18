#ifndef __GAALET_CONJUGATE_H
#define __GAALET_CONJUGATE_H

#include "utility.h"

namespace gaalet {

template<class A>
struct conjugate : public expression<conjugate<A>>
{
   typedef typename A::clist clist;

   typedef typename A::metric metric;
   
   typedef typename A::element_t element_t;

   conjugate(const A& a_)
      :  a(a_)
   { }

   template<conf_t conf>
   element_t element() const {
      return a.element<conf>() * Power<-1, BitCount<conf>::value*(BitCount<conf>::value+1)/2>::value;
   }

protected:
   const A& a;
};


}  //end namespace gaalet

/// \brief Reverse of a multivector.
/// \ingroup ga_ops
template <class A> inline
gaalet::conjugate<A>
conjugate(const gaalet::expression<A>& a) {
   return gaalet::conjugate<A>(a);
}

#endif
