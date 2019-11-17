#include "vptree.h"
#include <cmath>
#include <string>
#include <queue>
#define LEAF -1

VPTree::VPTree(std::vector<CoordPtr> &data) {
	std::cout << "Starting to construct tree" << std::endl; 
	this->root = this->construct_tree(data); 
	return; 
}

VPTree::~VPTree(){
	return; 
}

void VPTree::print_tree() {
	std::cout << "" << std::endl; 
	this->print_node(this->root, 0); 
	return; 
}

VPTree::Node* VPTree::construct_tree(std::vector<CoordPtr> &data) {
	// Recursive base case(s) -- the data vector only contains one element, which means this
	// element will be encapsulated in a child node, as is
	if (data.empty())					return nullptr; 
	else if (data.size() == 1) {
		Node* node = new Node; 
		node->point = data[0]; node->mu = LEAF; 
		node->left = nullptr; node->right = nullptr; 
		return node; 
	} 			 
 
	std::cout << "1" << std::endl;

 	// 1. Generate random "pivot" element that oversees the remaining data as a vantage
 	int n = data.size(); 
	std::uniform_int_distribution<int> dist(0, n-1); 
	int pivot = dist(this->generator); 
	CoordPtr vantage = data[pivot]; 

	std::cout << "2" << std::endl;

	std::cout << "Pivot is: " + std::to_string(pivot) << std::endl; 
	std::cout << "n is: " + std::to_string(n) << std::endl; 

	// 2. Compute distances between all other data elements and the pivot (and keep track of indices)
	std::vector<float> distances;
	distances.reserve(n-1);  
	for (int i = 0; i < n; i++) {
		if (i != pivot) 	distances.push_back(vantage.distance_bw(data[i]));
	}

	std::cout << "3" << std::endl;

	// 3. Sort in ascending order of distance between data elements and the vantage and take the median to 
	// divide the data in half. Elements closer to the vantage point than the median distance go in the left
	// subtree of the vantage point node, and elements further away go in the right subtree. 
	float mu = hybrid_select_median(distances); 

	// std::sort(distances.begin(), distances.end(), 
	// 	[](const std::pair<float, int> &a, const std::pair<float, int> &b) -> bool {
	// 	return (a.first < b.first); 
	// });
	// float mu = (distances[(n-1)/2]).first; 

	std::cout << "3.5" << std::endl;

	// 4. Partition datasets into left and right subtree sets
	std::vector<CoordPtr> left; std::vector<CoordPtr> right;
	left.reserve((n-2)/2); right.reserve((n-1)/2); 
	for (int i = 0; i < distances.size(); i++) {
		if (i != pivot && distances[i] < mu)	left.push_back(data[i]); 
		else if (i != pivot)					right.push_back(data[i]); 
	}

	std::cout << "4" << std::endl;

	// 5. Construct the Node object and recursively construct the left and right subtrees
	Node* node = new Node; 
	node->point = vantage; node->mu = mu;
	node->left = this->construct_tree(left); 
	node->right = this->construct_tree(right); 
	return node;  
}

CoordPtr VPTree::query(const CoordPtr &target) const {
	std::queue<Node*> to_search; 
	to_search.push(this->root); 
	float tau = std::numeric_limits<float>::infinity(); 

	CoordPtr nearest; 
	while (!to_search.empty()) {
		Node* cur = to_search.front(); to_search.pop(); 
		float dist = target.distance_bw(cur->point); 

		if (dist < tau) {
			tau = dist; 
			nearest = cur->point; 
		}

		if (cur->mu != LEAF) {
			if (cur->left != nullptr && tau > dist - cur->mu)		to_search.push(cur->left);
			if (cur->right != nullptr && tau >= cur->mu - dist)		to_search.push(cur->right);  
		}
	}

	return (nearest); 
}

void VPTree::print_node(Node* &node, int offset) const {
	if (node == nullptr)		return; 

	std::string indent(offset, '\t'); 
	std::string vantage; std::string mu; std::string left; std::string right;

	vantage = indent + "Vantage: ";  
	std::cout << vantage << node->point << std::endl;

	mu = indent + "Mu: " + std::to_string(node->mu);
	std::cout << mu << std::endl; 

	left = indent + "Left ->";
	std::cout << left << std::endl; 
	this->print_node(node->left, offset+1); 

	right = indent + "Right ->"; 
	std::cout << right << std::endl; 
	this->print_node(node->right, offset+1); 
}
