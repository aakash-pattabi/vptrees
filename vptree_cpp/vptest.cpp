#include "vptree.h"
using namespace std; 

int main() {
	// Instantiate a (small) dataset
	std::pair<float, float> d1; 
	std::pair<float, float> d2; 
	std::pair<float, float> d3; 
	std::pair<float, float> d4; 
	std::pair<float, float> d5; 

	d1 = std::make_pair(3.7, 0.6); 
	d2 = std::make_pair(9.0, 3.8); 
	d3 = std::make_pair(8.2, 7.6);
	d4 = std::make_pair(8.1, 4.9);
	d5 = std::make_pair(7.6, 7.8);

	std::vector<pair<float, float> > data; 
	data.push_back(d1); 
	data.push_back(d2); 
	data.push_back(d3); 
	data.push_back(d4); 
	data.push_back(d5); 

	// Build a VP tree on the data
 	VPTree* vp = new VPTree(data); 
 	vp->print_tree(); 

 	std::pair<float, float> target; 
 	target = std::make_pair(1, 1); 
 	std::pair<float, float> nearest = vp->query(target); 
 	cout << "Nearest neighbor is: (" + std::to_string(nearest.first) + ", " + 
 		std::to_string(nearest.second) + ")" << endl; 

 	return 0; 
}
