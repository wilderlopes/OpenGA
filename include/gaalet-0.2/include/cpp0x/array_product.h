#ifndef __GAALET_ARRAY_PRODUCT
#define __GAALET_ARRAY_PRODUCT

namespace gaalet
{

template<class L[], class R[]>
struct array_product : public expression<array_product<L[], R[]>>
{
   typedef typename merge_lists<typename L[]::clist, typename R[]::clist>::clist clist;

   typedef typename metric_combination_traits<typename L[]::metric, typename R[]::metric>::metric metric;

   typedef typename element_type_combination_traits<typename L[]::element_t, typename R[]::element_t>::element_t element_t;

   array_product(const L[]& l_ , const R[]& r_ )
      :  l(l_), r(r_)
   { }

   template<conf_t conf>
   element_t element() const {
	/*
	for (int n = 0; n < M; ++n)
    {        
        aa = A[n]; //selecting nth entry of A
        bb = B[n]; //selecting nth entry of B
        cc += aa * bb;
    }  
*/

      return l[0].element<conf>();
   }

protected:
   const L[]& l;
   const R[]& r;
};

} //end namespace gaalet

/// \brief array_product of two multivectors.
/// \ingroup ga_ops
/*
template <class L, class R> inline
gaalet::addition<L, R>
operator+(const gaalet::expression<L>& l, const gaalet::expression<R>& r) {
   return gaalet::addition<L, R>(l, r);
}
*/
#endif
