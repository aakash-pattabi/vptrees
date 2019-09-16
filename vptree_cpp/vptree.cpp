#include "vptree.h"
#include <cmath>
#include <string>
#include <queue>
#define LEAF -1

VPTree::VPTree(std::vector<std::pair<float, float> > data) {
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

VPTree::Node* VPTree::construct_tree(std::vector<std::pair<float, float> > data) {
	// Recursive base case(s) -- the data vector only contains one element, which means this
	// element will be encapsulated in a child node, as is
	if (data.empty())					return nullptr; 
	else if (data.size() == 1) {
		Node* node = new Node; 
		node->point = data[0]; node->mu = LEAF; 
		node->left = nullptr; node->right = nullptr; 
		return node; 
	} 			 
 
 	// 1. Generate random "pivot" element that oversees the remaining data as a vantage
 	int n = data.size(); 
	std::uniform_int_distribution<int> dist(0, n-1); 
	int pivot = dist(this->generator); 
	std::pair<float, float> vantage = data[pivot]; 

	// 2. Compute distances between all other data elements and the pivot (and keep track of indices too)
	std::vector<std::pair<float, int> > distances(n-1); 
	for (int i = 0; i < n; i++) {
		if (i < pivot) 					distances[i] = std::make_pair(distance_bw(vantage, data[i]), i); 
		else if (i > pivot)				distances[i-1] = std::make_pair(distance_bw(vantage, data[i]), i); 
	}

	// 3. Sort in ascending order of distance between data elements and the vantage and take the median to 
	// divide the data in half. Elements closer to the vantage point than the median distance go in the left
	// subtree of the vantage point node, and elements further away go in the right subtree. 
	// 
	// TODO: Implement O(n) median selection algorithm to avoid using O(nlogn) sorting procedure
	std::sort(distances.begin(), distances.end(), 
		[](const std::pair<float, int> &a, const std::pair<float, int> &b) -> bool {
		return (a.first < b.first); 
	});
	float mu = (distances[(n-1)/2]).first; 

	// 4. Partition datasets into left and right subtree sets
	std::vector<std::pair<float, float> > left; std::vector<std::pair<float, float> > right;
	left.reserve((n-2)/2); right.reserve((n-1)/2); 
	for (int i = 0; i < distances.size(); i++) {
		if (distances[i].first < mu)	left.push_back(data[distances[i].second]); 
		else							right.push_back(data[distances[i].second]); 
	}

	// 5. Construct the Node object and recursively construct the left and right subtrees
	Node* node = new Node; 
	node->point = vantage; node->mu = mu;
	node->left = this->construct_tree(left); 
	node->right = this->construct_tree(right); 
	return node;  
}

std::pair<float, float> VPTree::query(std::pair<float, float> target) {
	std::queue<Node*> to_search; 
	to_search.push(this->root); 
	float tau = std::numeric_limits<float>::infinity(); 

	std::pair<float, float> nearest; 
	while (!to_search.empty()) {
		Node* cur = to_search.front(); to_search.pop(); 
		float dist = this->distance_bw(target, cur->point); 

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

float VPTree::distance_bw(std::pair<float, float> a, std::pair<float, float> b) {
	float x = a.first - b.first; 
	float y = a.second - b.second; 
	return (sqrt((x*x) + (y*y))); 
}

void VPTree::print_node(Node* node, int offset) {
	if (node == nullptr)		return; 

	std::string indent("\t\t", offset); 
	std::string vantage; std::string mu; std::string left; std::string right; 
	vantage = indent + "Vantage: (" + std::to_string((node->point).first) + ", " + 
		std::to_string((node->point).second) + ")"; 
	mu = indent + "Mu: " + std::to_string(node->mu); 
	left = indent + "Left ->"; 
	right = indent + "Right ->"; 

	std::cout << vantage << std::endl; 
	std::cout << mu << std::endl; 

	std::cout << left << std::endl; 
	this->print_node(node->left, offset+1); 

	std::cout << right << std::endl; 
	this->print_node(node->right, offset+1); 
}
