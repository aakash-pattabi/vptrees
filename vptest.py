from vptree import *
import numpy as np 
import random

def vptest_ints(nsamples, dim, nqueries, lb = 0, ub = 1000):
	data = [np.random.randint(lb, ub, dim) for i in range(nsamples)]
	tree = VPTree(
			data = data, 
			distfunc = lambda a, b : np.linalg.norm(a-b), 
			vpfunc = random.choice
		)
	baseline = LinearScan(
			data = data, 
			distfunc = lambda a, b : np.linalg.norm(a-b)
		)

	for test in range(nqueries):
		q = np.random.randint(lb, ub, dim)
		vp_soln = tree.query(q)
		baseline_soln = baseline.query(q)
		vp_dist = np.linalg.norm(vp_soln - q)
		baseline_dist = np.linalg.norm(baseline_soln - q)
		err = "VP solution " + np.array2string(vp_soln) + " at distance {:f}".format(vp_dist) + "\n"
		err += "Scan solution " + np.array2string(baseline_soln) + " at distance {:f}".format(baseline_dist)
		assert vp_dist == baseline_dist, err

if __name__ == "__main__":
	vptest_ints(nsamples = 1000, dim = 3, nqueries = 500)
