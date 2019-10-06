#include "datareader.h"
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include <fstream>
#include <iostream>

/*
 * @func: DataReader()
 * ----------
 * Constructor for the DataReader class
 * 
 * @args 
 * 		fileName:
 * 
 * 		delim:
 * 
 * @return
 */
DataReader::DataReader(std::string fileName, std::string delim) {
	this->file = fileName; this->delimiter = delim; 
	return; 
}

/*
 * @func: ~DataReader()
 * ----------
 * Destructor for the DataReader class
 * 
 * @args n/a
 *
 * @return n/a
 */
DataReader::~DataReader() {
	return; 
}

std::vector<std::vector<float> > DataReader::get_float_data() {
	// Line stream input variables
	std::ifstream data(this->file);  
	std::string line = "";  

	// Line tokenizers
	typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
	boost::char_separator<char> sep{" ,"}; 

	// Return data structure and size validation
	std::vector<std::vector<float> > data_list;
	std::size_t coord_size = -1;

	while (getline(data, line)) { 
		std::vector<float> coords; 
		tokenizer tok{line, sep};	
		for (auto &t : tok) {
			float f = atof(t.c_str()); 
			coords.push_back(f); 
		}

		// Validate length of coordinate / # of entries to prevent malformed input 
		// (tuples of differential sizes)
		if (coord_size != -1)	assert(coords.size() == coord_size); 
		else 					coord_size = coords.size(); 
		data_list.push_back(coords); 
	} 
	return (data_list); 
}

/*
 * @func: DataReader::print_float_data()
 * ----------
 * @args 
 * 		data:
 * 
 * @return n/a
 */
void DataReader::print_float_data(std::vector<std::vector<float> > data) {
	for (auto &tuple : data) {
		for (auto &element : tuple) {
			std::cout << std::to_string(element); 
			if (&element != &tuple.back())	std::cout << ","; 
		}

		std::cout << std::endl; 
	}
}
