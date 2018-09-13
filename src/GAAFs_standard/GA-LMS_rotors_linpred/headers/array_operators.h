// Overloaded functions for multiplying arrays of rotors
// Wilder Lopes (wilderlopes@gmail.com) and Anas Al-Nuaimi (anas.alnuaimi@tum.de)
// February 2016

typedef gaalet::algebra<gaalet::signature<3,0> > em;
typedef em::mv<0, 3, 5, 6>::type mvType;
mvType zeros{0,0,0,0};

//Function to sum array of multivectors
std::vector<mvType> array_sum(std::vector<mvType> leftMVArr, std::vector<mvType> rightMVArr)
{
    int M = leftMVArr.size();
    std::vector<mvType> sumMV;
    sumMV.resize(M);

    for (int n=0; n < leftMVArr.size(); n++) //populating sumMV
    {
        sumMV.at(n) = zeros;
    }

    for (int iter = 0 ; iter < leftMVArr.size(); iter++)
    {
        sumMV.at(iter) = eval(leftMVArr.at(iter) + rightMVArr.at(iter));
    }
    return sumMV;
}

//Function to subtract array of multivectors
std::vector<mvType> array_sub(std::vector<mvType> leftMVArr, std::vector<mvType> rightMVArr)
{
    int M = leftMVArr.size();
    std::vector<mvType> sumMV;
    sumMV.resize(M);

    for (int n=0; n < leftMVArr.size(); n++) //populating sumMV
    {
        sumMV.at(n) = zeros;
    }

    for (int iter = 0 ; iter < leftMVArr.size(); iter++)
    {
        sumMV.at(iter) = eval(leftMVArr.at(iter) - rightMVArr.at(iter));
    }
    return sumMV;
}

//Function to multiply two arrays of multivectors
// array_prod<MVArr,MVArr>
mvType array_prod(std::vector<mvType> leftMVArr, std::vector<mvType> rightMVArr)
{
    mvType sumMV{0,0,0,0,0,0,0,0};
    for (int iter = 0 ; iter < leftMVArr.size(); iter++)
    {
        sumMV = eval(sumMV +  eval(leftMVArr.at(iter)*rightMVArr.at(iter)));
    }
    return sumMV;
}

//Function to multiply an array of multivectors by a multivector
// array_prod<MVArr,MV>
std::vector<mvType> array_prod(std::vector<mvType> leftMVArr, mvType rightMV)
{
    int M = leftMVArr.size();
    std::vector<mvType> sumMV;
    sumMV.resize(M);

    for (int n=0; n < leftMVArr.size(); n++) //populating sumMV
    {
        sumMV.at(n) = zeros;
    }

    for (int iter = 0 ; iter < leftMVArr.size(); iter++)
    {
        sumMV.at(iter) = eval(leftMVArr.at(iter)*rightMV);
    }
    return sumMV;
}

//Function to multiply a multivector by an array of multivectors
// array_prod<MV,MVArr>
std::vector<mvType> array_prod(mvType leftMV, std::vector<mvType> rightMVArr)
{
    int M = rightMVArr.size();
    std::vector<mvType> sumMV;
    sumMV.resize(M);

    for (int n=0; n < rightMVArr.size(); n++) //populating sumMV
    {
        sumMV.at(n) = zeros;
    }

    for (int iter = 0 ; iter < rightMVArr.size(); iter++)
    {
        sumMV.at(iter) = eval(leftMV*rightMVArr.at(iter));
    }
    return sumMV;
}

//Function to multiply an int by an array of multivectors
// array_prod<int,MVArr>
std::vector<mvType> array_prod(int leftInt, std::vector<mvType> rightMVArr)
{
    int M = rightMVArr.size();
    std::vector<mvType> sumMV;
    sumMV.resize(M);

    for (int n=0; n < rightMVArr.size(); n++) //populating sumMV
    {
        sumMV.at(n) = zeros;
    }

    for (int iter = 0 ; iter < rightMVArr.size(); iter++)
    {
        sumMV.at(iter) = eval(leftInt*rightMVArr.at(iter));
    }
    return sumMV;
}

//Function to multiply a double by an array of multivectors
// array_prod<double,MVArr>
std::vector<mvType> array_prod(double leftDouble, std::vector<mvType> rightMVArr)
{
   int M = rightMVArr.size();
    std::vector<mvType> sumMV;
    sumMV.resize(M);

    for (int n=0; n < rightMVArr.size(); n++) //populating sumMV
    {
        sumMV.at(n) = zeros;
    }

    for (int iter = 0 ; iter < rightMVArr.size(); iter++)
    {
        sumMV.at(iter) = eval(leftDouble*rightMVArr.at(iter));
    }
    return sumMV; 
}

//Function to reverse an array of multivectors for ga_300
std::vector<mvType> reverse_array(std::vector<mvType> MVArr)
{
    int M = MVArr.size();
    std::vector<mvType> revMVArr; //reversed MVArr
    revMVArr.resize(M);

    for (int iter1 = 0 ; iter1 < MVArr.size(); iter1++)
    {
        revMVArr.at(iter1) = ~(MVArr.at(iter1));
    }
    return revMVArr;
}

//Function to invert an array of multivectors for ga_300
std::vector<mvType> inverse_array(std::vector<mvType> MVArr)
{
    int M = MVArr.size();
    std::vector<mvType> invMVArr; //inverted MVArr
    invMVArr.resize(M);

    for (int iter1 = 0 ; iter1 < MVArr.size(); iter1++)
    {
        mvType MVArrgrades = MVArr.at(iter1);
        mvType MVentry{MVArrgrades[0], -MVArrgrades[1], -MVArrgrades[2],
                    MVArrgrades[3], -MVArrgrades[4], MVArrgrades[5],
                    MVArrgrades[6], -MVArrgrades[7]};
        invMVArr.at(iter1) = MVentry;
    }
    return invMVArr;
}

//Function to conjugate an array of multivectors for ga_300
std::vector<mvType> conjugate_array(std::vector<mvType> MVArr)
{
    int M = MVArr.size();
    std::vector<mvType> conjMVArr; //conjugated MVArr
    conjMVArr.resize(M);

    for (int iter1 = 0 ; iter1 < MVArr.size(); iter1++)
    {
        mvType MVArrgrades = MVArr.at(iter1);
        mvType MVentry{MVArrgrades[0], -MVArrgrades[1], -MVArrgrades[2],
                    -MVArrgrades[3], -MVArrgrades[4], -MVArrgrades[5],
                    -MVArrgrades[6], MVArrgrades[7]};
        conjMVArr.at(iter1) = MVentry;
    }
    return conjMVArr;
}

