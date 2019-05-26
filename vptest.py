from vptree import *
import numpy as np
import random
import time
import matplotlib.pyplot as plt
random.seed(166)
np.random.seed(166)

class TestHarness(object):
	def __init__(self, data, scan_params, tree_params, forest_params):
		scan_params["data"] = data
		tree_params["data"] = data
		forest_params["data"] = data
		self.estimators = [LinearScan(**scan_params), \
			VPTree(**tree_params), 
			VPForest(**forest_params)]
		self.n = len(data)

	def test(queries):
		n_queries = len(queries)
		results = {}
		times = []
		for q in queries:
			tic = time.time()
			self.estimators[0].query(q)
			toc = time.time() - tic
			times.append(toc)
		results["LinearScan"] = times

		for est in self.estimators[1:]:
			times = []
			name = est.__name__
			for q in queries:
				ct = [1]
				tic = time.time()
				est.query(q, ct)
				toc = time.time() - tic
				times.append((toc, ct[0]))
			results[name] = times

		return results

	def plot_and_summarize(results):
		

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
