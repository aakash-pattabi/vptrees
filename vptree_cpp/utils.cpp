#include "utils.h"
#include <algorithm>
#define BLOCK_SIZE 5
#define SORT_THRESHOLD 200000 // Experimentally, compiler optimization yields more speed, see Note

/*
 * ----------
 * @args 
 * 		data: A vector of pairs where the median is to be selected from the first elements
 * 			  and the second elements serve as indices into the "original" vector of data 
 *			  or the database
 *
 * 		index: The index for the order selection, e.g. |data.size()/2| if a median is 
 *			   desired. 
 * 
 * Note: When compiler optimization is turned off, simply calling std::sort() on the vector and
 * returning the median index is faster than this implementation. But, with compiler optimization
 * set to -Ofast, this implementation is faster for float vectors of size 200,000 or greater, yielding
 * an "even better" hybrid algorithm that simply std::sort()s on smaller vectors and applies this
 * technique on larger ones... 
 */
float select_median(std::vector<float> data, int index) {
	// Recursive base case
	assert(!data.empty()); 
	if (data.size() == 1)		return (data[0]); 

	// If the base case is not satisfied, and a median is desired with no argument input, 
	// determine the position of the median element in a hypothetical sorted data vector
	if (index == MEDIAN)		index = (data.size() % 2 == 0) ? (data.size()/2)-1 : data.size()/2; 

	// 1. Divide the data into groups of 5 (and a remainder)
	// 2. Sort each group of 5 and find the median "manually" (thru sorting)
	int last_block_seen = 0; 
	std::vector<float> medians; 
	medians.reserve(1+(data.size()/5)); 
	for (int i = 0; i < data.size(); i++) {
		if ((i+1) % BLOCK_SIZE == 0) {
			auto block_start = data.begin() + last_block_seen; 
			auto block_end = data.begin() + last_block_seen + BLOCK_SIZE; 
			std::sort(block_start, block_end);  

			int offset = last_block_seen + (BLOCK_SIZE/2); 
			medians.push_back(data[offset]); 
			last_block_seen += BLOCK_SIZE;
		} else if (i == data.size()-1) {
			auto block_start = data.begin() + last_block_seen; 
			int num_elems = data.size() - last_block_seen;
			int offset_into_block = (num_elems % 2 == 0) ? (num_elems/2)-1 : num_elems/2;  
			std::sort(block_start, data.end());

			int offset = last_block_seen + offset_into_block; 
			medians.push_back(data[offset]); 
		}
	}

	// 3. Recursively use SELECT to find the median of medians, keeping track of whether the median
	// 		of medians is a duplicate element (to ensure "copies" are preserved when the vector
	//		is partitioned)
	float med = select_median(medians); 
	int duplicate_medians = 0; 
	for (auto &elem : data) {
		if (elem == med)						duplicate_medians += 1; 
	}

	// 4. Partition the data around the median of medians
	std::vector<float> left_of_pivot; 
	std::vector<float> right_of_pivot;  
	for (int i = 0; i < data.size(); i++) {
		if (data[i] < med)						left_of_pivot.push_back(data[i]); 
		else if (data[i] > med)					right_of_pivot.push_back(data[i]);
		else if (data[i] == med && duplicate_medians > 1) {
			right_of_pivot.push_back(data[i]); 
			duplicate_medians -= 1; 
		}
	}

	/*
 	 * 5. Either return pivot or recursively apply SELECT again. The pivot is returned if
	 * it is the median -- that is, the size of the left_of_partition vector is 
	 * |data.size()/2| (floor). 
	 */ 
	if (left_of_pivot.size() == index)			return (med); 
	else if (left_of_pivot.size() > index)		return select_median(left_of_pivot, index); 
	else 										return select_median(right_of_pivot, index-(1+left_of_pivot.size())); 
}

float hybrid_select_median(std::vector<float> data) {
	assert(!data.empty()); 
	if (data.size() >= SORT_THRESHOLD) {
		return (select_median(data)); 
	} else {
		int index = (data.size()%2 == 0) ? (data.size()/2)-1 : (data.size()/2); 
		std::sort(data.begin(), data.end()); 
		return (data[index]); 
	}
}
