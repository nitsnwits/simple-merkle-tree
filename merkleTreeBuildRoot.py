#!/usr/bin/env python

from collections import defaultdict
import hashlib

# Build root of a merkle tree using stack, infact try doing it, because it's not working with hash of lists
# The problem with other approach is I'm building the nodes from the range, which is incorrect
# This is a different tree, and seeing it from completely opposite perspective, it should be built from its leaves
# So, this approach would take two leaves at a time, hash them, and build a node, which would be the parent
# Then, it'll take two nodes at a time, hash them, and build a node, which would be the parent
# This process will be repeated until we get to the root which would be the Merkle Tree Root. 

# global variables
iteration = 0

def buildMerkleRoot(leavesList):
	if len(leavesList) == 1:
		print "\n"
		print "The size of the list is 1. Printing Merkle Tree Root:"
		return leavesList[0] # 0th element will be the merkle tree root
	global iteration
	iteration = iteration + 1
	print "\nNumber of iteration: ", iteration, " Number of branches to handle: ", len(leavesList)

	# Assume the list is of even length, take two elements from the list, and hash them together, and add to nodesList
	nodesList = []
	for i in range(0, len(leavesList) - 1, 2): # 2 is to skip 2nd element
		print "\n"
		print "Branch: ", i+1, " is ", leavesList[i]
		print "Branch: ", i+2, " is ", leavesList[i+1]
		print "Their parent thus becomes: ", hashTwoElements(leavesList[i], leavesList[i+1])
		nodesList.append(hashTwoElements(leavesList[i], leavesList[i+1]))
	if len(leavesList) % 2 == 1: # if the list was of odd lenght, this condition would become true
		# hash the same element twice and append to nodesList
		print "\n"
		print "Branch: ", len(leavesList), " is ", leavesList[-1]
		print "This branch's parent, branch is hashed with itself: ", hashTwoElements(leavesList[-1], leavesList[-1])
		nodesList.append(hashTwoElements(leavesList[-1], leavesList[-1]))
	leavesList = nodesList
	return buildMerkleRoot(leavesList)

def hash(key):
	"""
	generic hash function
	"""
	return str(hashlib.md5(key).hexdigest())

def hashTwoElements(firstLeaf, secondLeaf):
	# hash two leaves to build a parent
	return hash(hash(firstLeaf) + hash(secondLeaf))

leavesListOld = [
	"5",
	"135",
	"170",
	"185"
]

leavesList = [
	"aa",
	"bb",
	"cc",
	"dd",
	"ee",
	"ff",
	"gg",
	"hh",
	"ii",
	"jj",
	"kk",
	"ll",
	"mm",
	"11",
	"22",
	"33",
	"44",
	"55",
	"66",
	"77",
	"88",
	"99" # I don't know if it's odd or even
]
print "\nTrying with a small list: \n"
print buildMerkleRoot(leavesListOld), "\n"
print "\nTrying with a larger list\n"
print buildMerkleRoot(leavesList), "\n"