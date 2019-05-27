from vptree import *
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import pickle
import re
import argparse, sys
from progress.bar random.seed(166)
np.random.seed(166)

class Test(object):
	def __init__(self, data, scan_params, tree_params, forest_params, 
				 save_name = None):
		scan_params["data"] = data
		tree_params["data"] = data
		forest_params["data"] = data
		print("Setting up data structures...")
		self.estimators = [
			LinearScan(**scan_params),
			VPTree(**tree_params), 
			VPForest(**forest_params)
		]
		self.n = len(data)
		self.save_name = save_name

	def test(self, queries):
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

		bar = Bar("VPTree: Query hits", max = n_queries, fill = "=")
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
		trees_to_query = np.unique(np.linspace(1, total_trees, total_trees**0.8).astype(int))
		print("Hitting VPForest with {} queries, checking from {}-{} trees/query".format(n_queries, trees_to_query[0], trees_to_query[-1]))
		bar = Bar("VPForest: Query hits (all #s of trees)", max = n_queries*len(trees_to_query), fill = "=")
		times_by_tree = {}
		for n_trees in trees_to_query:
			times = []
			for q in queries:
				ct = [1]
				tic = time.time()
				result = self.estimators[2].query(q, n_trees, ct)
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
		all_succeed = n_trees[np.argmin(error_maxs)]

		plt.clf()
		plt.plot(n_trees, times, color = "blue", label = "VPForest")
		plt.axhline(results["VPTree-Time"], color = "green", label = "VPTree")
		plt.axhline(results["LinearScan-Time"], color = "red", label = "LinearScan")
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
		plt.axvline(all_succeed, color = "orange", linestyle = ":", label = "> {} trees => VPF is exact".format(all_succeed))
		plt.xlabel("# of trees in forest")
		plt.ylabel("Rank error (0 is best)")
		plt.legend(loc = "upper right")
		plt.title("VPForest rank error over all queries by # trees: " + str(self.n) + " points")
		plt.tight_layout()
		plt.savefig(self.save_name + "_error.png")

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
		self.results = [self.tests[i].test(query_sequence[i]) for i in range(self.n_tests)]
		self.save()
		return self.results

	def _save(self):
		assert self.results
		with open(self.save_name + "_results.pkl", "wb") as f:
			pickle.dump(self.results, f)

if __name__ == "__main__":
	df = lambda a, b : np.linalg.norm(a-b)
	scan_params = {
		"distfunc" : df
	}
	tree_params = {
		"distfunc" : df
	}
	forest_params = {
		"distfunc" : df, 
		"n_estimators" : None		# By default, grow n/log(n) estimators ==> global O(n) query time
	}

	parser = argparse.ArgumentParser()
	parser.add_argument("--n", type = int)
	parser.add_argument("--d", type = int)
	parser.add_argument("--n_queries", type = int)
	args = parser.parse_args()

	data = np.random.rand(args.n, args.d)
	q = [np.random.rand(args.d) for i in range(args.n_queries)]
	t = Test(data, scan_params, tree_params, forest_params, save_name = "output/{}x{}_Euclidean".format(args.n, args.d))
	results = t.test(q)
	t.plot_results(results)
