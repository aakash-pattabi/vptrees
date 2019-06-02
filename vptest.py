from vptree import *
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import pickle
import re
import argparse, sys
from progress.bar import Bar
random.seed(166)
np.random.seed(166)

class Test(object):
	def __init__(self, data, scan_params, tree_params, forest_params, 
				 save_name = None):
		scan_params["data"] = data
		tree_params["data"] = data
		forest_params["data"] = data
		self.estimators = [
			LinearScan(**scan_params),
			VPTree(**tree_params), 
			VPForest(**forest_params)
		]
		self.n = len(data)
		self.save_name = save_name

	def test(self, queries, random_searching = False):
		assert queries
		n_queries = len(queries)
		results = {}

		bar = Bar("LinearScan: Query hits", max = n_queries, fill = "=")
		times = []
		for q in queries:
			tic = time.time()
			self.estimators[0].query(q)
			toc = time.time() - tic
			times.append(toc)
			bar.next()
		results["LinearScan"] = times
		bar.finish()

		bar = Bar("VPTree: Query hits" + 4*" ", max = n_queries, fill = "=")
		times = []
		for q in queries:
			ct = [1]
			tic = time.time()
			self.estimators[1].query(q, ct)
			toc = time.time() - tic
			times.append((toc, ct[0]))
			bar.next()
		results["VPTree"] = times
		bar.finish()

		total_trees = self.estimators[2].n_estimators
		trees_to_query = np.unique(np.linspace(1, total_trees, int(total_trees**0.8)).astype(int))
		print("Testing {} #s of trees/query, checking from {}-{} trees/query".format(
			len(trees_to_query), trees_to_query[0], trees_to_query[-1])
		)
		bar = Bar("VPForest: Query hits" + 2*" ", max = n_queries*len(trees_to_query), fill = "=")
		times_by_tree = {}
		for n_trees in trees_to_query:
			times = []
			for q in queries:
				ct = [1]
				tic = time.time()
				result = self.estimators[2].query(q, n_trees, ct, random_searching)
				toc = time.time() - tic
				error = self.estimators[0].get_rank_of(q, result)
				times.append((toc, ct[0], error))
				bar.next()
			times_by_tree[n_trees] = times
		results["VPForest"] = times_by_tree
		bar.finish()

		results = self._summarize(results)
		return results

	def _summarize(self, results):
		assert "LinearScan" in results
		assert "VPTree" in results
		assert "VPForest" in results

		summary = {
			"n" : self.n
		}
		summary["LinearScan-Time"] = np.mean(results["LinearScan"])
		summary["VPTree-Time"] = np.mean([el[0] for el in results["VPTree"]])
		summary["VPTree-Hits"] = np.mean([el[1] for el in results["VPTree"]])

		for n_trees in results["VPForest"].keys():
			summary["VPForest-Time-" + str(n_trees)] = np.mean([el[0] for el in results["VPForest"][n_trees]])
			summary["VPForest-Hits-" + str(n_trees)] = np.mean([el[1] for el in results["VPForest"][n_trees]])
			summary["VPForest-Error-" + str(n_trees)] = {
				"min" :		np.min([el[2] for el in results["VPForest"][n_trees]]), 
				"mean" : 	np.mean([el[2] for el in results["VPForest"][n_trees]]),
				"median" : 	np.median([el[2] for el in results["VPForest"][n_trees]]), 
				"max" : 	np.max([el[2] for el in results["VPForest"][n_trees]])
			}
		return summary

	def plot_results(self, results):
		assert self.save_name

		keys = [k for k in results.keys() if "VPForest" in k]		
		n_trees = [int(re.search(r"\d+", k).group()) for k in keys if "Time-" in k]

		times = [k for __, k in sorted(zip(n_trees, [results[k] for k in keys if "Time-" in k]))]
		hits = [k for __, k in sorted(zip(n_trees, [results[k] for k in keys if "Hits-" in k]))]
		error_mins = [k for __, k in sorted(zip(n_trees, [results[k]["min"] for k in keys if "Error-" in k]))]
		error_meds = [k for __, k in sorted(zip(n_trees, [results[k]["median"] for k in keys if "Error-" in k]))]
		error_maxs = [k for __, k in sorted(zip(n_trees, [results[k]["max"] for k in keys if "Error-" in k]))]
		n_trees = sorted(n_trees)
		half_succeed = n_trees[np.argmin(error_meds)]
		all_succeed = n_trees[np.argmin(error_maxs)]

		plt.clf()
		plt.plot(n_trees, times, color = "blue", label = "VPForest")
		plt.axhline(results["VPTree-Time"], color = "green", label = "VPTree")
		plt.axhline(results["LinearScan-Time"], color = "red", label = "LinearScan")
		plt.axvline(half_succeed, color = "cornflowerblue", linestyle = ":", label = "> {} trees => VPF is 0.5 exact".format(half_succeed))
		plt.axvline(all_succeed, color = "orange", linestyle = ":", label = "> {} trees => VPF is exact".format(all_succeed))
		plt.xlabel("# of trees in forest")
		plt.ylabel("Mean query time (s)")
		plt.legend(loc = "lower right")
		plt.title("VPForest avg. query time by # trees: " + str(self.n) + " points")
		plt.tight_layout()
		plt.savefig(self.save_name + "_time.png")

		plt.clf()
		plt.plot(n_trees, hits, color = "blue", label = "VPForest")
		plt.axhline(results["VPTree-Hits"], color = "green", label = "VPTree")
		plt.axhline(self.n, color = "red", label = "LinearScan")
		plt.axvline(half_succeed, color = "cornflowerblue", linestyle = ":", label = "> {} trees => VPF is 0.5 exact".format(half_succeed))
		plt.axvline(all_succeed, color = "orange", linestyle = ":", label = "> {} trees => VPF is exact".format(all_succeed))
		plt.xlabel("# of trees in forest")
		plt.ylabel("Mean search hits")
		plt.legend(loc = "lower right")
		plt.title("VPForest avg. search hits by # trees: " + str(self.n) + " points")
		plt.tight_layout()
		plt.savefig(self.save_name + "_hits.png")

		all_succeed = n_trees[np.argmin(error_maxs)]
		plt.clf()
		plt.plot(n_trees, error_mins, color = "blue", label = "Best query error")
		plt.plot(n_trees, error_meds, color = "green", label = "Median query error")
		plt.plot(n_trees, error_maxs, color = "red", label = "Worst query error")
		plt.axvline(half_succeed, color = "cornflowerblue", linestyle = ":", label = "> {} trees => VPF is 0.5 exact".format(half_succeed))
		plt.axvline(all_succeed, color = "orange", linestyle = ":", label = "> {} trees => VPF is exact".format(all_succeed))
		plt.xlabel("# of trees in forest")
		plt.ylabel("Rank error (0 is best)")
		plt.legend(loc = "upper right")
		plt.title("VPForest rank error over all queries by # trees: " + str(self.n) + " points")
		plt.tight_layout()
		plt.savefig(self.save_name + "_error.png")

'''
Assumes for the time being that all data and queries are _Euclidean_ tables of the form (n x d), where
[n] is the number of data points and [d] is the dimensionality of each pointer. A query, therefore, takes the
form of a [d]-length vector. 
'''
class TestHarness(object):
	def __init__(self, data_sequence, scan_params, tree_params, forest_params, save_name):
		self.n_tests = len(data_sequence)
		print("Initializing data structures for all tests. This may take a while...")
		self.tests = [Test(
				data_sequence[i], 
				scan_params, 
				tree_params, 
				forest_params, 
				save_name = save_name + "_{n}x{d}".format(
					n = data_sequence[i].shape[0], 
					d = data_sequence[i].shape[1]
				)
			) for i in range(self.n_tests)]
		self.save_name = save_name
		self.results = None

	def test(self, query_sequence, random_searching = False):
		assert len(query_sequence) == self.n_tests
		self.results = []
		for i in range(self.n_tests):
			print("\nRunning test [{}/{}]:".format(i+1, self.n_tests))
			res = self.tests[i].test(query_sequence[i], random_searching)
			self.results.append(res)
		self._save()
		return self.results

	def plot_results(self):
		assert self.results
		for i, t in enumerate(self.tests):
			t.plot_results(self.results[i])

	def _save(self):
		assert self.results
		with open(self.save_name + "_results.pkl", "wb") as f:
			pickle.dump(self.results, f)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--n", nargs = "+", type = int, required = True, 
		help = "Number of data points to generate for each test; currently from a uniform distribution U(0, 1).")

	parser.add_argument("--d", nargs = "+", type = int, required = True, 
		help = "Dimensionality of data points for each test, which will be over data of size (n_i, d_i) for (n, d) pair i.")

	parser.add_argument("--n_queries", nargs = "+", type = int, required = True, 
		help = "Number of queries over which to summarize performance statistics; either one integer or one integer _per test_.")

	parser.add_argument("--random_searching", default = False, action = "store_true", 
		help = "Flag -- indicates whether or not to use diameter-proportioned random searching in VPForest approximate queries.")

	parser.add_argument("--random_vp", default = False,
		help = "Flag -- indicates whether or not to use a random vantage point or choose one at the edge of space")

	args = parser.parse_args()
	if len(args.d) != len(args.n):
		parser.error("The number of arguments passed to --n and --d must be the same! (Each data set has an (n, d) pair.)")

	if len(args.n_queries) != 1 and len(args.n_queries) < len(args.d):
		parser.error("Either pass one value of --n_queries for _each test_, or one global value for all tests!")

	if len(args.n_queries) == 1:
		args.n_queries *= len(args.n)

	df = lambda a, b : np.linalg.norm(a-b)

	if args.random_vp:
		vpfunc = random.choice
	else:
		vpfunc = lambda i, d: i[np.argsort(np.linalg.norm(d, axis = 1)[i])[-1]]

	scan_params = {
		"distfunc" : df
	}
	tree_params = {
		"distfunc" : df,
		"vpfunc" : vpfunc
	}
	forest_params = {
		"distfunc" : df, 
		"n_estimators" : None,		# By default, grow n/log(n) estimators ==> global O(n) query time
		"vpfunc" : vpfunc
	}

	shapes = zip(args.n, args.d)
	queries = zip(args.d, args.n_queries)

	random_searching_flag = "_RandomSearching" if args.random_searching else ""
	data_sequence = [np.random.rand(*shape) for shape in shapes]
	query_sequence = [[np.random.rand(d) for i in range(n_q)] for d, n_q in queries]

	th = TestHarness(
			data_sequence = data_sequence, 
			scan_params = scan_params, 
			tree_params = tree_params, 
			forest_params = forest_params, 
			save_name = "output/Euclidean" + random_searching_flag
		)
	th.test(query_sequence, args.random_searching)
	th.plot_results()
