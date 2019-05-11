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

	vp_qtimes, vp_vis, baseline_qtimes = [], [], []
	for test in range(nqueries):
		q = np.random.randint(lb, ub, dim)

		tic = time.time()
		vp_soln, nvis = tree.query(q)
		toc = time.time()
		vp_qtimes.append(toc - tic)
		vp_vis.append(nvis)

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

	vpm, baselinem, vpvisits = np.average(vp_qtimes), np.average(baseline_qtimes), np.average(vp_vis)
	print("Passed all tests!")
	print("Mean query time for VP: {:f}".format(vpm))
	print("Mean search visits for VP: {:f}".format(vpvisits))
	print("Mean query time for baseline: {:f}".format(baselinem))
	return vpm, baselinem

if __name__ == "__main__":
	vptest_ints(
			nsamples = 1000, 
			dim = 3, 
			nqueries = 50, 
			verbose = False
		)	
