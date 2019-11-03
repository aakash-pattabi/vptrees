// #include "vptree.h"
#include "datareader.h"
#include "utils.h"
using namespace std; 

// Why is the first value saving as 0...? 
int main() {
	DataReader dr("data.csv", ","); 
	std::vector<CoordPtr> data = dr.get_float_data(); 
	dr.print_float_data(data); 

	/*
	std::vector<std::pair<float, int> > x_coords; 
	for (auto &element : data) { 
		std::pair<float, int> p = std::make_pair(element[0], 0); 
		x_coords.push_back(p); 
	}

	std::pair<float, int> med = select_median(x_coords); 
	std::cout << "Median is " + std::to_string(med.first) << endl; 
	*/

	return 0; 
}
