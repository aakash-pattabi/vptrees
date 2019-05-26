from statistics import median
from queue import PriorityQueue
import matplotlib.pyplot as plt
import random
import math

'''
--------------------
Class: LinearScan
Implements a baseline "memorization database" that allows NN queries in
linear time using a linear search over database entries. 
-------------------- 

N/A. 
'''
class LinearScan(object):
	def __init__(self, data, distfunc):
		self.data = data
		self.distfunc = distfunc
	
	def query(self, q):
		min_so_far = self.data[0]
		dist_so_far = self.distfunc(q, min_so_far)
		for element in self.data:
			dist = self.distfunc(q, element)
			if dist < dist_so_far:
				min_so_far = element
				dist_so_far = dist
		return min_so_far

	def get_rank_of(self, q, v):
		assert v in self.data
		dists = sorted([self.distfunc(q, x) for x in self.data])
		return dists.index(self.distfunc(q, v))

'''
--------------------
Class: Node, VPTree
Implements the simplest possible vantage point tree for 1-NN search. 
--------------------

Importantly, let [vpfunc], the argument that selects a vantage point
from the data space to attach to a node, and [indices], the data in each 
node, be defined over the _indices_ of the [data] field in the VPTree. 
Likewise, let [vantage], the vantage point in the node, be defined as an index 
into [self.data].  
'''
class Node(object):
	def __init__(self, indices):
		self.indices = indices
		self.vantage = None
		self.mu = None
		self.left = None
		self.right = None

class VPTree(object):
	def __init__(self, data, distfunc, vpfunc = random.choice):
		self.data = data
		self.root = Node(
				indices = list(range(len(self.data)))
			)
		self.distfunc = distfunc
		self.vpfunc = vpfunc
		self._construct_tree(self.root)

	def _construct_tree(self, node):
		# The node is a leaf node (no candidate children)
		if len(node.indices) == 1:
			node.vantage = node.indices[0]
			return

		node.vantage = self.vpfunc(node.indices)
		node.indices.remove(node.vantage)
		distances = [self.distfunc(self.data[node.vantage], self.data[i]) for i in node.indices]
		node.mu = median(distances)
		left = [node.indices[i] for i in range(len(distances)) if distances[i] < node.mu]
		right = list(set(node.indices) - set(left))

		if left:
			node.left = Node(indices = left)
			self._construct_tree(node.left)

		if right:
			node.right = Node(indices = right)
			self._construct_tree(node.right)

	def print_tree(self):
		print("\n")
		self._print_node(self.root, "")

	def _print_node(self, node, indent):
		if node is None:
			return 
		print(indent + "Vantage: " + (str(self.data[node.vantage])))
		muform = "{:f}" if node.mu else "{}"
		print(indent + "Mu: " + muform.format(node.mu))
		print(indent + "Indices: {}".format(str(node.indices)))
		if node.right:	print(indent + "Right ->")
		self._print_node(node.right, indent + "\t")
		if node.left:	print(indent + "Left ->")
		self._print_node(node.left, indent + "\t")

	'''
	Var. [tau] tracks the _distance of the farthest nearest neighbor_ 
	we've encountered in the search so far (trivial for k = 1). 

	Var. [nvis] tracks by reference the number of node "visits" made in a search
	(e.g. the number of comparisons). (Note, [nvis] must be a list for updates)
	by reference to work. 
	'''
	def query(self, q, nvis = False):
		assert(nvis == [1] or nvis is False)
		tau = float("inf")
		to_search = [self.root]
		nn = self.root.vantage
		while to_search:
			cur = to_search.pop(0)
			d = self.distfunc(q, self.data[cur.vantage])

			if d < tau:								# Node's vantage point is the closest to q
				tau = d 							# seen so far ==> increment [tau] and reassign
				nn = cur 							# the running nearest neigbor

			if cur.mu:								# If not a leaf node
				if cur.left and tau > d - cur.mu:
					to_search.append(cur.left)
					if nvis:	nvis[0] += 1

				if cur.right and tau >= cur.mu - d:
					to_search.append(cur.right)
					if nvis:	nvis[0] += 1

		return self.data[nn.vantage]

	'''
	Performs an "approximate" nearest-neighbor search following a root->leaf 
	path down the tree, returning the leaf node as the nearest neighbor. 
	'''
	def fast_approx_query(self, q, nvis = False):
		assert(nvis == [1] or nvis is False)
		cur = self.root
		closest = None
		while cur:
			closest = cur
			d = self.distfunc(q, self.data[cur.vantage])

			if cur.mu:
				if d < cur.mu:
					cur = cur.left
					if nvis:	nvis[0] += 1

				else: # d >= cur.mu
					cur = cur.right
					if nvis:	nvis[0] += 1
			else:				cur = None

		return self.data[closest.vantage]

class VPForest(object):
	def __init__(self, data, distfunc, vpfunc = random.choice, n_estimators = None):
		self.distfunc = distfunc
		if n_estimators is None:	n_estimators = int(len(data)/math.log2(len(data)))
		self.n_estimators = n_estimators
		self.estimators = [VPTree(data, distfunc, vpfunc) for i in range(self.n_estimators)]

	def query(self, q, n_trees, n_vis = False):
		assert n_trees <= self.n_estimators
		guesses = []
		for i in range(n_trees):
			count = [1] if n_vis else False
			guess = self.estimators[i].fast_approx_query(q, count)
			if n_vis:	n_vis[0] += count[0]
			guesses.append(guess)

		dists = [self.distfunc(guess, q) for guess in guesses]
		__, i = sorted(zip(dists, range(n_trees)))[0]
		return guesses[i]
