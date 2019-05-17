from statistics import median
from queue import PriorityQueue
import matplotlib.pyplot as plt

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
		dists = [self.distfunc(q, x) for x in self.data]
		ranked = [x for __,x in sorted(zip(dists, self.data))]
		return ranked.index(v)

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
	def __init__(self, indices, parent):
		self.indices = indices
		self.parent = parent
		self.vantage = None
		self.mu = None
		self.left = None
		self.right = None

class VPTree(object):
	def __init__(self, data, distfunc, vpfunc):
		self.data = data
		self.root = Node(
				indices = list(range(len(self.data))), 
				parent = None
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
			node.left = Node(indices = left, parent = node)
			self._construct_tree(node.left)

		if right:
			node.right = Node(indices = right, parent = node)
			self._construct_tree(node.right)

	'''
	def draw_tree(self, default_linewidth = 2, decay = 0.9):
		assert len(self.data[0]) == 2
		min_x, max_x, min_y, max_y = 0, 0, 0, 0
		fig, ax = plt.subplots()
		to_draw = [self.root]
		elem = 0
		while elem < len(self.data):
			cur = to_draw[elem]
			if cur.left:	to_draw.append(cur.left)
			if cur.right:	to_draw.append(cur.right)
			elem += 1

		to_draw = list(reversed(to_draw))
		while to_draw:
			cur = to_draw.pop()
			point, rad = self.data[cur.vantage], cur.mu

			if not rad:					continue
			if point[0] + rad > max_x:	max_x = point[0] + rad
			if point[1] + rad > max_y:	max_y = point[1] + rad
			if point[0] - rad < min_x:	min_x = point[0] - rad
			if point[1] - rad < min_y:	min_y = point[1] - rad

			width = default_linewidth*(decay**elem)
			circ = plt.Circle(point, rad, 
							  fill = False, edgecolor = "black", 
							  clip_on = True, linewidth = width)
			ax.add_artist(circ)
			elem -= 1

		plt.xlim(left = min_x, right=max_x)
		plt.ylim(bottom = min_y, top = max_y)
		plt.xlabel("X")
		plt.ylabel("Y")
		plt.title("VP-tree on {} elements".format(len(self.data)))
		plt.savefig("vptree_{}elements.png".format(len(self.data)))
		'''

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
