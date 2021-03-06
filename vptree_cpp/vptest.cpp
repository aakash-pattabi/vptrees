#include "vptree.h"
#include "datareader.h"
#include "utils.h"
#include <iostream>

int main() {
	DataReader dr("data.csv", ","); 
	std::vector<CoordPtr> data = dr.get_float_data(); 
	dr.print_float_data(data); 

	CoordPtr c = data[0]; 
	CoordPtr p = data[1]; 

	std::size_t i = 0; 
	for (auto ptr : data) {
		std::string status = (ptr.get_p() == nullptr ? "Null" : "Not null"); 
		std::cout << std::to_string(i) + ": " << status << std::endl; 
		i++; 
	}

	// float f = c.distance_bw(p); 
	// std::cout << std::to_string(f) << std::endl; 

	VPTree vp = VPTree(data); 
	vp.print_tree(); 

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
