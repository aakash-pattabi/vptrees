from vptree import *
import numpy as np
import random
import time
import matplotlib.pyplot as plt
random.seed(166)
np.random.seed(166)

def vptest_ints(nsamples = 1000, dim = 3, nqueries = 100, \
		lb = 0, ub = 100, verbose = False):
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
	vp_visits = []
	for test in range(nqueries):
		q = np.random.randint(lb, ub, dim)

		tic = time.time()
		nvis = [1]
		vp_soln = tree.query(q, nvis = nvis)
		toc = time.time()
		vp_qtimes.append(toc - tic)
		vp_visits.append(nvis)

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

	vp_avgtime, baseline_avgtime = np.average(vp_qtimes), np.average(baseline_qtimes)
	vp_avgqueries = np.average(vp_visits)
	print("Passed all tests!")
	print("Mean query time for VP: {:f}".format(vp_avgtime))
	print("Mean query time for baseline: {:f}".format(baseline_avgtime))
	print("Mean queries for VP: {:.2f} (vs. log(n) = {:.2f})".format(vp_avgqueries, np.log2(nsamples)))
	return vp_avgtime, baseline_avgtime, vp_avgqueries

if __name__ == "__main__":
	npoints = 50
	samps = 10**np.linspace(1, 4, npoints).astype(int)
	dims = [2, 5, 10, 50, 100, 1000]

	# Battery of tests over various database sizes
	samp_tests = np.zeros((npoints, 3))
	i = 0
	for samp in samps:
		vp_avgtime, baseline_avgtime, vp_avgqueries = vptest_ints(
				nsamples = samp
			)
		samp_tests[i,:] = np.array([vp_avgtime, baseline_avgtime, vp_avgqueries])
		i += 1

	plt.plot(samps, samp_tests[:,0], color = "blue", label = "VP-tree")
	plt.plot(samps, samp_tests[:,1], color = "red", label = "Lin. scan")
	plt.legend(loc = "lower right")
	plt.title("VP-tree vs. linear scan as n increases")
	plt.xlabel("n (# of samples)")
	plt.xlabel("Avg. query time (s) (100 queries)")
	plt.savefig("./output/querytime_n.png")
	plt.clf()

	plt.plot(samps, samp_tests[:,2], color = "blue", label = "VP-tree")
	plt.plot(samps, np.log2(samps), color = "red", label = "Lg(n) target")
	plt.legend(loc = "lower right")
	plt.title("VP-tree queries vs. optimal ZPS target")
	plt.xlabel("n (# of samples)")
	plt.xlabel("Avg. node visits per query (100 queries)")
	plt.savefig("./output/querytime_visits.png")
	plt.clf()

	# Battery of tests over various data dimensionalities
	dim_tests = np.zeros((len(dims), 2))
	i = 0	
	for dim in dims:
		vp_avgtime, baseline_avgtime, __ = vptest_ints(
				dim = dim
			)
		dim_tests[i,:] = np.array([vp_avgtime, baseline_avgtime])
		i += 1

	plt.plot(dims, dim_tests[:,0], color = "blue", label = "VP-tree")
	plt.plot(dims, dim_tests[:,1], color = "red", label = "Lin. scan")
	plt.legend(loc = "lower right")
	plt.title("VP-tree vs. linear scan as d increases")
	plt.xlabel("d (dimensionality of sample)")
	plt.xlabel("Avg. query time (s) (100 queries)")
	plt.savefig("./output/querytime_d.png")
