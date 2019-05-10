from vptree import *
import numpy as np 
import random

def vptest_ints(nsamples, dim, lb = 0, ub = 1000):
	data = [np.random.randint(lb, ub, dim) for i in range(nsamples)]
	tree = VPTree(
			data = data, 
			distfunc = lambda a, b : np.linalg.norm(a-b), 
			vpfunc = random.choice
		)

if __name__ == "__main__":
	vptest_ints(nsamples = 1000, dim = 3)
