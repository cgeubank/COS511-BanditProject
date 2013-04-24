from algorithms import *
from operator import itemgetter

"""
Returns total expected regret for a certain algorithm 
run on a certain distribution
"""
def totalExpectedRegret(dist, algorithms, distParams, algParams):
	# Generate Distribution
	dist, meanList = dist(*distParams)
	numRounds = len(dist)
	
	# Print Distribution in sorted order
	printMeans(meanList)
	
	regrets = []
	algParamIndex = 0
	
	# Calculate expected regret for each algorithm for this distribution
	for alg in algorithms:
		armChoices = alg(dist, *(algParams[algParamIndex]))
	
		# print out choices 
		printChoices(str(alg), armChoices, meanList)
	
		# zip list (concatenate tuples into two separate tuples) and then find max mean
		bestMean = max(meanList)
	
		# calculate total expected regret
		regret = numRounds * bestMean
		for i in range(0, numRounds):
			armIndex = armChoices[i]
			regret = regret - (meanList[armIndex])
			
		algParamIndex += 1
		
		regrets.append(regret)
		
	# Return list of regrets
	return regrets 
	
"""
Prints mean in descending order, including arm index
"""
def printMeans(meanList):
	l = [(i[0], i[1]) for i in sorted(enumerate(meanList), key=lambda x:x[1], reverse=True)]
	for pair in l:
		print (str(pair))

"""
Prints the arm choices made by algorithm
"""	
def printChoices(name, armChoices, meanList):
	print (name + ": ")
	round = 0
	for choice in armChoices:
		print "Round %r: Index: %r, Mean: %r " % (round, choice, meanList[choice])
		round += 1
		
	
	
# Test main
if __name__ == '__main__':
	func1 = epsilonGreedy
	dist = normalDistribution
	numArms = 25
	rounds = 1000
	epsilon = 0.6
	
	func2 = boltzmann
	temp = 0.99
	
	regrets = totalExpectedRegret(dist, [func1, func2], [numArms, rounds], [[epsilon], [temp]])
	print regrets 