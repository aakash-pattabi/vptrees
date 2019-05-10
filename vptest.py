from vptree import *
import numpy as np
import random
import time
random.seed(166)
np.random.seed(166)

def vptest_ints(nsamples, dim, nqueries, lb = 0, ub = 100, verbose = False):
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

	if verbose:	tree.print_tree()

	vp_qtimes, baseline_qtimes = [], []
	for test in range(nqueries):
		q = np.random.randint(lb, ub, dim)

		tic = time.time()
		vp_soln = tree.query(q)
		toc = time.time()
		vp_qtimes.append(toc - tic)

		tic = time.time()
		baseline_soln = baseline.query(q)
		toc = time.time()
		baseline_qtimes.append(toc - tic)

		vp_dist = np.linalg.norm(vp_soln - q)
		baseline_dist = np.linalg.norm(baseline_soln - q)
		err = "Query {}".format(test) + ": " + str(q)
		err += "\nVP solution " + str(vp_soln) + " at distance {:f}".format(vp_dist) + "\n"
		err += "Scan solution " + str(baseline_soln) + " at distance {:f}".format(baseline_dist)
		assert vp_dist == baseline_dist, err

	vpm, baselinem = np.average(vp_qtimes), np.average(baseline_qtimes)
	if verbose:
		print("Passed all tests!")
		print("Mean query time for VP: {:f}".format(vpm))
		print("Mean query time for baseline: {:f}".format(baselinem))
	return vmp, baselinem

if __name__ == "__main__":
	vptest_ints(
			nsamples = 1000, 
			dim = 10, 
			nqueries = 50
		)	
