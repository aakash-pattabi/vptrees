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

std::vector<CoordPtr> DataReader::get_float_data() {
	// Line stream input variables
	std::ifstream data(this->file);  
	std::string line = "";  

	// Line tokenizers
	typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
	boost::char_separator<char> sep{" ,"}; 

	// Get coordinate size for size validation
	getline(data, line); 
	tokenizer tok{line, sep}; 
	std::size_t coord_size = 0; 
	for (auto t = tok.begin(); t != tok.end(); t++) {
		coord_size += 1; 
	}
	data.seekg(0, data.beg); 

	// Instantiate return data structure
	std::vector<CoordPtr> data_list;

	while (getline(data, line)) {  
		std::valarray<float> *init = new std::valarray<float>(coord_size); 
		CoordPtr p(init); 

		tokenizer tok{line, sep};
		std::size_t tmp = 0;
		for (auto &t : tok) {
			float f = atof(t.c_str()); 
			p[tmp] = f; 
			tmp += 1;
		}
		// Validate length of coordinate. Namely, make sure that exactly coord_size elements
		// were in the token stream. ** Is it bad style to make this assertion also "handle" the case
		// where there were _too many_ tokens, causing the array to overflow? Probably... **
		assert(tmp == coord_size); 
		data_list.push_back(std::move(p));  
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
void DataReader::print_float_data(std::vector<CoordPtr> &data) {
	for (auto &ptr : data) {
		std::cout << ptr << std::endl;  
	}
}
