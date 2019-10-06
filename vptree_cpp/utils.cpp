#include <vector>
#include <cfloat>
#include <algorithm>
#define BLOCK_SIZE 5
#define MEDIAN -1

// Want to find the median in worst-case linear time in a data structure 
// consisting of pairs of <float, int>. In this case, the <float> part of the 
// pair is the distance between the vantage point ("pivot") in the data and the
// given element, identified by the <int> which is an index into the data. 
// 
// That is, find the median in a std::vector<std::pair<float, int> > sorting along
// the floats. 
// 
// TODO: Modify to select_median, taking an input data vector and an index... 

/*
 * ----------
 * @args 
 * 		data: A vector of pairs where the median is to be selected from the first elements
 * 			  and the second elements serve as indices into the "original" vector of data 
 *			  or the database
 *
 * 		index: The index for the order selection, e.g. |data.size()/2| if a median is 
 *			   desired. 
 */
std::pair<float, int> select_median(std::vector<std::pair<float, int> > data, int index = MEDIAN) {
	// Recursive base case
	if (data.size() == 1)		return (data[0]); 

	// If the base case is not satisfied, and a median is desired with no argument
	// input, determine the position of the median element in a hypothetical sorted data vector
	if (index == MEDIAN)			index = (data.size() % 2 == 0) ? (data.size()/2)-1 : data.size()/2; 

	// 1. Divide the data into groups of 5 (and a remainder)
	// 2. Sort each group of 5 and find the median "manually" (thru sorting)
	int last_block_seen = 0; 
	std::vector<std::pair<float, int> > medians; 
	for (int i = 0; i < data.size(); i++) {
		if ((i+1) % BLOCK_SIZE == 0) {
			auto block_start = data.begin() + (i+1) - BLOCK_SIZE; 
			auto block_end = data.begin() + (i+1); // STL sorting is non-inclusive of last element
			std::sort(block_start, block_end, 
				[](const std::pair<float, int> &a, const std::pair<float, int> &b) -> bool {
					return (a.first < b.first); 
				});  

			int offset = (i+1) - BLOCK_SIZE + (BLOCK_SIZE/2); 
			medians.push_back(data[offset]); 
			last_block_seen += BLOCK_SIZE;

		} else if (i == data.size()-1) {
			auto block_start = data.begin() + last_block_seen; 
			int num_elems = data.size() - last_block_seen; 
			std::sort(block_start, data.end(), 
				[](const std::pair<float, int> &a, const std::pair<float, int> &b) -> bool {
					return (a.first < b.first); 
				});

			int offset = last_block_seen + (num_elems/2); 
			medians.push_back(data[offset]); 
		}
	}

	// 3. Recursively use SELECT to find the median of medians
	std::pair<float, int> med = select_median(medians); 

	// 4. Partition the data around the median of medians
	// How do you extend to handle cases where elements in the vector are duplicates
	// (corresponding to data elements in the database that are equidistant from the selected
	// vantage point?)
	std::vector<std::pair<float, int> > left_of_pivot; 
	std::vector<std::pair<float, int> > right_of_pivot;  
	for (int i = 0; i < data.size(); i++) {
		if (data[i].first < med.first)			left_of_pivot.push_back(data[i]); 
		else if (data[i].first > med.first)		right_of_pivot.push_back(data[i]); 	
	}

	/*
 	 * 5. Either return pivot or recursively apply SELECT again. The pivot is returned if
	 * it is the median -- that is, the size of the left_of_partition vector is 
	 * |data.size()/2| (floor). 
	 * 
	 * Of course, since the current implementation allows the client
	 * to "easily" signal that they want a median with the sentinel MEDIAN argument, 
	 * we check for the value of order first...
	 */ 
	if (left_of_pivot.size() == index)			return (med); 
	else if (left_of_pivot.size() > index)		return select_median(left_of_pivot, index); 
	else 										return select_median(right_of_pivot, index-(left_of_pivot.size()+1)); 
}
