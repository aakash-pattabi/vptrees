#ifndef VPTree_Included
#define VPTree_Included

#include <utility>
#include <random>
#include <iostream>
#include "utils.h"

class VPTree {
	public: 
		// Each node in a vantage point tree maintains the defining (vantage) point, 
		// the radial distance dividing the remainder of the search space in half from that
		// point, and pointers to the left- and right-subchildren
		struct Node {
			CoordPtr point; 
			float mu; 
			Node* left; 
			Node* right; 
		}; 

		// Constructor
		VPTree(std::vector<CoordPtr> data); 

		// Destructor
		~VPTree(); 

		// Search 
		CoordPtr query(const CoordPtr &target) const; 

		// Debugging
		void print_tree(); 

	private: 
		Node* root;
		std::default_random_engine generator;

		// Recursive procedure for constructing the main tree and its subtrees
		Node* construct_tree(std::vector<CoordPtr> data); 

		// Debugging
		void print_node(Node* &node, int offset) const; 
}; 

#endif 
