#!/usr/bin/env python

from collections import defaultdict
import hashlib

# Global constants
CONSISTENT = 0
FULLY_INCONSISTENT = 1
PARTIALLY_INCONSISTENT = 2

class MerkleTree:
	def __init__(self, partitioner, depth, maxRange):
		self.partitioner = partitioner
		self.depth = depth
		self.maxRange = maxRange
		self.root = ''
		self.partitionList = []
		self.hashList = defaultdict(list)
		self.init()

	def init(self):
		"""
		This method will create boilerplate tree with the nodes defined from max range and partitioner
		It is a naive approach, partitioning is not generalized
		"""
		self.createPartitionList()
		self.setRoot()
		self.createTree()

	def createPartitionList(self):
		"""
		This method creates a basic list of partition ranges for Merkle tree
		"""
		token = 0
		while ((token + self.partitioner) < self.maxRange):
			self.partitionList.append(token + self.partitioner)
			token = token + self.partitioner

	def getPartitionList(self):
		return self.partitionList

	def createTree(self):
		"""
		Create nodes based on the partition list
		"""
		for node in self.partitionList:
			self.hashList[node].append('')
			self.hashList[node].append('')

	def addRows(self, key):
		"""
		This method is used to add a dict to values of the tree
		"""
		# sub method for add rows
		def recursiveAddRows(start, end, key):
			"""
			Recursive binary search within the partition list
			"""
			#print "Iteration: " + " start: " + str(start) + " End: " + str(end)
			if (end - start <= 1):
				return end
			else:
				mid = (start + end)/2
				if (key < self.partitionList[mid]):
					return recursiveAddRows(start, mid - 1, key)
				else:
					return recursiveAddRows(mid + 1, end, key)

		# main add rows method implem
		index = recursiveAddRows(0, len(self.partitionList), key)
		token = self.partitionList[index]

		# decide whether it's a left child or a right child
		if (key < token):
			# it's a left child
			index = 0
		else: 
			# it's a right child
			index = 1
		# to concatenate the leaf value, sum and hash
		self.hashList[token][index] = self.hashSum(token, index, key)

	def hashSum(self, token, index, key):
		"""
		This function will concatentate a leaf value in case of multiple rows
		"""
		if (self.hashList[token][index] is not None):
			# add the two 
			oldValue = self.hashList[token][index]
			newValue = hash(str(key))
			newNodeValue = hash(oldValue + newValue)
			return newNodeValue
		else:
			return hash(str(key))

	def setRoot(self):
		"""
		Set root node of a merkle tree based on the partioned list
		"""
		self.root = self.partitionList[len(self.partitionList)/2]
		#self.partitionList.remove(self.root)

	def getRoot(self):
		"""
		Return root node of a merkle tree
		"""
		return self.root;

	def display(self):
		"""
		Prints an instance of a merkle tree
		"""
		print "Merkle Tree Root = " + str(self.getRoot())
		for token in self.partitionList:
			print "Node Hash: " + str(token) + "\t\tChildren: " + str(self.hashList[token])



def MerkleTreeDifference(ltree, rtree):
	if (ltree.getRoot() == rtree.getRoot()):
		print "Roots are equal: Tree1 Root-> " + str(ltree.getRoot()) + " Tree2 Root-> " + str(rtree.getRoot())
		return CONSISTENT
			

def hash(key):
	"""
	generic hash function
	"""
	return str(hashlib.md5(key).hexdigest())

def main():
	testDepth = 3
	testSize = 8
	testMaxRange = 256
	testPartition = 32

	# create first tree
	ltree = MerkleTree(testPartition, testDepth, testMaxRange)
	ltree.addRows(90)
	ltree.addRows(135)
	ltree.addRows(170)
	ltree.addRows(185)
	print "Tree 1: -> \n"
	ltree.display()

	# create second tree
	rtree = MerkleTree(testPartition, testDepth, testMaxRange)
	rtree.addRows(90)
	rtree.addRows(135)
	rtree.addRows(170)
	rtree.addRows(185)
	print "Tree 2: -> \n"
	rtree.display()

	# find out the difference in the trees
	print "\nCalculating difference in two trees: \n"
	diff = MerkleTreeDifference(ltree, rtree);
	if (diff == CONSISTENT):
		print "\tResult: CONSISTENT"
	elif (diff == FULLY_INCONSISTENT):
		print "\tResult: FULLY_INCONSISTENT"
	elif (diff == PARTIALLY_INCONSISTENT):
		print "\tResult: PARTIALLY_INCONSISTENT"

if __name__ == '__main__':
	print "Simple MerkleTree Implementation Test \n"
	main()
