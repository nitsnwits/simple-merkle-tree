#!/usr/bin/env python

from collections import defaultdict
import hashlib

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
			self.hashList[node] = []
			#self.hashList[node].insert(0, '')
			#self.hashList[node].insert(1, '')


	def addRows(self, key):
		"""
		This method is used to add a dict to values of the tree
		"""
		# sub method for add rows
		def recursiveAddRows(start, end, key):
			"""
			Recursive binary search within the partition list
			"""
			print "Iteration: " + " start: " + str(start) + " End: " + str(end)
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
		print "index: " + str(index)
		token = self.partitionList[index]
		self.hashList[token].append(key)


		# while ((token + self.partitioner) < self.maxRange):
		# 	if (key > token and key < (token + self.partitioner)):
		# 		index = 0
		# 		break;
		# 	# elif (key > (token + self.partitioner) and key < (token + self.partitioner + self.partitioner)):
		# 	# 	index = 1
		# 	# 	break;
		# 	token = token + self.partitioner
		# if (index == 0):
		# 	token = token + self.partitioner
		# self.hashList[token][index] = key


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



#def MerkleTreeDifference(ltree, rtree):



def main():
	testDepth = 3
	testSize = 8
	testMaxRange = 256
	testPartition = 32

	# create first tree
	ltree = MerkleTree(testPartition, testDepth, testMaxRange)
	ltree.addRows(5)
	ltree.addRows(135)
	ltree.addRows(170)
	ltree.addRows(185)
	ltree.display()

	# rtree = MerkleTree(testPartition, testMaxRange, rtreeRows)
	# rtree.display()

	# # find out the difference in the trees
	# diff = MerkleTreeDifference(ltree, rtree);

if __name__ == '__main__':
	print "Simple MerkleTree Implementation Test"
	main()
