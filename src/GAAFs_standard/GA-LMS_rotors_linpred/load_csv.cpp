#include <fstream>
#include <sstream>
#include <iostream>

int main()
{
    int n_rows = 474;
    int n_cols = 4;

    double data[n_rows][n_cols];
    std::ifstream file("/home/wilder/dev/OpenGA/data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS.csv");

    for(int row = -1; row < n_rows; ++row)
    {
        std::string line;
        std::getline(file, line);
        // if ( !file.good() )
        //     break;

        std::stringstream iss(line);
        // std::cout << "line = " << line << std::endl;

        if (row >= 0)
        {
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

                // std::cout << "val = " << val << std::endl;

                std::stringstream convertor(val);
                convertor >> data[row][col];
              }
          }
        }
    }

    std::cout << "final array = \n" << std::endl;
    for (int i = 0; i < n_rows; ++i)
    {
        for (int j = 0; j < n_cols; ++j)
        {
            std::cout << data[i][j] << ' ';
        }
        std::cout << std::endl;
    }
    return 0;
}
