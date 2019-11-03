#include <string>
#include "utils.h"

/*
 * Currently only works for CSVs of float tuples (though easily adaptable to strings). 
 * How to make it generic? Or to be up-front about what kinds of data formats are 
 * supported? 
 *
 * Some kind of type switch / flag
 */
class DataReader {
	public: 
		// Constructor
		DataReader(std::string fileName, std::string delim);

		// Destructor  
		~DataReader(); 

		std::vector<CoordPtr> get_float_data();
		void print_float_data(std::vector<CoordPtr> &data); 

	private:
		std::string file; 
		std::string delimiter;  
}; 
