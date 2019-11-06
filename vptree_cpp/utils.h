#ifndef Util_Included
#define Util_Included

#include <vector>
#include <cfloat>
#include <valarray>
#include <memory>
#include <iostream>
#define BLOCK_SIZE 5
#define MEDIAN -1

/* 
 * Who is responsible for deleting the errant CoordPtr when we're done building a tree and 
 * querying it? The data will have been surfaced through a DataReader object which will 
 * store coordinates in a vector (or some such structure). But, in theory, it's not immediately
 * clear who will delete the data ex-post
 * 
 * "Use a shared_ptr only if the valarrays need to continue living _after_ the container holding
 * them is destroyed (e.g the vector produced by the DataReader)"
 * This is probably not the case, since the data structure can construct itself _around_ the 
 * vector / database, which can proprietarily own deletion of the data....
 */
class CoordPtr {
	typedef std::shared_ptr<std::valarray<float> > Ptr;
	public:
		// Direct constructor
		CoordPtr(std::valarray<float> *coord = nullptr) {
			p.reset(coord); 
		}

		// Copy constructor
		CoordPtr(const CoordPtr &c) {
			p = c.p; 
		}

		// Assignment operator
		CoordPtr operator= (const CoordPtr& c) {
			if (&c == this) {
				return *this; 
			}

			p.reset(); 
			p = c.p;  
			return *this; 
		}

		// Destructor
		~CoordPtr() {
			return;
		} 

		// Array access
		float& operator[] (const std::size_t index) {
			std::valarray<float> &v = *(p.get()); 
			return (v[index]); 
		}

		// Euclidean distance
		float distance_bw(CoordPtr b) const {
			std::valarray<float> tmp = (*(this->p).get()) - (*(b.p).get()); 
			float f = std::sqrt(std::pow(tmp, 2).sum()); 
			return (f);  
		}

		std::size_t size() const {
			return (this->p.get()->size()); 
		}

		friend std::ostream& operator << (std::ostream& os, CoordPtr &cp) {
			int s = cp.size(); 
			os << "("; 
			for (int i = 0; i < s-1; i++) {
				os << std::to_string(cp[i]) + ", "; 
			}
			os << std::to_string(cp[s-1]) + ")"; 
			return (os); 
		}

		Ptr& get_p() {
			return (p); 
		}

	private:
		Ptr p; 
}; 

/* 
 * [Some explanation here...]
 */
std::pair<float, int> select_median(std::vector<std::pair<float, int> > data, int index = MEDIAN); 

#endif
