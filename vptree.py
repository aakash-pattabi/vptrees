
from statistics import median

class Node(object):
	def __init__(self, indices, parent):
		self.indices = indices
		self.parent = parent
		self.vantage = None
		self.mu = None
		self.left = None
		self.right = None
		
'''
--------------------
Class: VPTree
Implements the simplest possible vantage point tree for 1-NN search. 
--------------------

Importantly, let [vpfunc], the argument that selects a vantage point
from the data space to attach to a node, and [indices], the data in each 
node, be defined over the _indices_ of the [data] field in the VPTree. 
Likewise, let [vantage], the vantage point in the node, be defined as an index 
into [self.data]. 

The [Node] class as defined above includes a [parent] pointer, but it 
may be unnecessary. Can delete later if we don't need it to revise the tree. 
'''
class VPTree(object):
	def __init__(self, data, distfunc, vpfunc):
		self.data = data
		self.root = Node(
				indices = range(len(self.data)), 
				parent = None
			)
		self.distfunc = distfunc
		self.vpfunc = vpfunc
		self._construct_tree(self.root)

	def _construct_tree(self, node):
		# If the parent node is (already) a leaf
		if len(node.indices) == 1:
			node.vantage = node.indices[0]
			return

		node.vantage = self.vpfunc(node.indices)
		distances = [self.distfunc(node.vantage, self.data[i]) for i in node.indices]
		node.mu = median(distances)
		left = [i for i in node.indices if distances[i] < node.mu]
		right = list(set(node.indices) - set(left))

		node.left = Node(
				indices = left, 
				parent = node
			)

		node.right = Node(
				indices = right, 
				parent = node
			)

	def query(self, q):
		cur = self.root
		while (q != self.data[cur.vantage]):
			# If the current node is (already) a leaf
			candidate = self.data[cur.vantage]
			if (len(cur.indices) == 1):
				return candidate
			if (self.distfunc(candidate, q) < cur.mu):	# Go left
				cur = cur.left
			else:										# Go right
				cur = cur.right
		return q

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
