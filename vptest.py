from vptree import *
import numpy as np
import random
import time
import matplotlib.pyplot as plt
random.seed(166)
np.random.seed(166)

class Test(object):
	def __init__(self, data, scan_params, tree_params, forest_params):
		scan_params["data"] = data
		tree_params["data"] = data
		forest_params["data"] = data
		self.estimators = [
			LinearScan(**scan_params),
			VPTree(**tree_params), 
			VPForest(**forest_params)
		]
		self.n = len(data)

	def test(queries):
		assert queries
		n_queries = len(queries)
		results = {}

		times = []
		for q in queries:
			tic = time.time()
			self.estimators[0].query(q)
			toc = time.time() - tic
			times.append(toc)
		results["LinearScan"] = times

		times = []
		for q in queries:
			ct = [1]
			tic = time.time()
			self.estimators[1].query(q, ct)
			toc = time.time() - tic
			times.append((toc, ct[0]))
		results["VPTree"] = times

		trees_to_query = np.linspace(1, self.n, self.n**0.8).astype(int)
		times_by_tree = {}
		for n_trees in trees_to_query:
			times = []
			for q in queries:
				ct = [1]
				tic = time.time()
				self.estimators[1].query(q, n_trees, ct)
				toc = time.time() - tic
				times.append((toc, ct[0]))
			times_by_tree[n_trees] = times
		results["VPTree"] = times_by_tree

		results = self._sanitize(results)
		return results

	def _sanitize(results):
		sanitized = {}
		for est in results:
			times = results[est]
			n_vis = (len(times[0]) > 1)
			if not n_vis:	
				sanitized[est] = np.mean(times)
			else:
				sanitized[est] = (np.mean([el[0] for el in times]), \
								  np.mean([el[1] for el in times]))

		sanitized["n"] = self.n
		return sanitized

class TestHarness(object):
	def __init__(self, data_sequence, scan_params, tree_params, forest_params, save_name):
		self.n_tests = len(data_sequence)
		self.tests = [Test(
				data_sequence[i], 
				scan_params, 
				tree_params, 
				forest_params
			) for i in range(self.n_tests)]
		self.save_name = save_name
		self.results = None

	def test(self, query_sequence):
		assert len(query_sequence) == self.n_tests
		results = [self.tests[i].test(query_sequence[i]) for i in range(self.n_tests)]
		self.results = self._concat_results(results)
		return self.results

	def _concat_results(results):
		concat = [[res["n"], res["LinearScan"]] + list(res["VPTree"]) + list(res["VPForest"]) for res in results]
		return np.array(concat)

	def plot(self):
		assert self.results
		headers = ["n", "LinearScan-Time", "VPTree-Time", "VPTree-Hits", "VPForest-Time", "VPForest-Hits"]

		plt.clf()
		plt.plot(self.results[0], self.results[1], color = "blue", label = headers[1])
		plt.plot(self.results[0], self.results[2], color = "red", label = headers[3])
		plt.plot(self.results[0], self.results[4], color = "green", label = headers[4])
		plt.legend(loc = "lower right")
		plt.xlabel("n (# of samples)")
		plt.ylabel("Avg. query time (s)")
		plt.savefig(self.save_name + "_time.png")

		plt.clf()
		plt.plot(self.results[0], self.results[3], color = "red", label = headers[3])
		plt.plot(self.results[0], self.results[5], color = "green", label = headers[5])
		plt.legend(loc = "lower right")
		plt.xlabel("n (# of samples)")
		plt.ylabel("Avg. hits per query")
		plt.savefig(self.save_name + "_hits.png")


if __name__ == "__main__":
	df = lambda a, b : np.linalg.norm(a-b)
	scan_params = {
		"distfunc" = df
	}
	tree_params = {
		"distfunc" = df
	}
	forest_params = {
		"distfunc" = df, 
		n_estimators = None		# By default, grow n/log(n) estimators --> global O(n) query time
	}


