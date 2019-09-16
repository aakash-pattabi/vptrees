#ifndef VPTree_Included
#define VPTree_Included

#include <vector>
#include <cfloat>
#include <utility>
#include <random>
#include <iostream>

class VPTree {
	public: 
		// Each node in a vantage point tree maintains the defining (vantage) point, 
		// the radial distance dividing the remainder of the search space in half from that
		// point, and pointers to the left- and right-subchildren
		struct Node {
			std::pair<float, float> point; 
			float mu; 
			Node* left; 
			Node* right; 
		}; 

		// Constructor
		VPTree(std::vector<std::pair<float, float> > data); 

		// Destructor
		~VPTree(); 

		// Search 
		std::pair<float, float> query(std::pair<float, float> target); 

		// Debugging
		void print_tree(); 

	private: 
		Node* root;
		std::default_random_engine generator;

		// Recursive procedure for constructing the main tree and its subtrees
		Node* construct_tree(std::vector<std::pair<float, float> > data); 
		float distance_bw(std::pair<float, float> a, std::pair<float, float> b);

		// Debugging
		void print_node(Node* node, int offset); 
}; 

#endif 
