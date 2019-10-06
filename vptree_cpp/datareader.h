#include <string>
#include <vector>
#include <cfloat>

/*
 * Currently only works for CSVs of int tuples (though easily adaptable to strings). 
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

		std::vector<std::vector<float> > get_float_data();
	
		void print_float_data(std::vector<std::vector<float> > data); 

	private:
		std::string file; 
		std::string delimiter; 
}; 
