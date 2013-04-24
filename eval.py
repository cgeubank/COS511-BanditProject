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
	
	regrets = []
	algParamIndex = 0
	
	# Calculate expected regret for each algorithm for this distribution
	for alg in algorithms:
		armChoices = alg(dist, *(algParams[algParamIndex]))
	
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
	
# Test main
if __name__ == '__main__':
	func1 = epsilonGreedy
	dist = normalDistribution
	numArms = 5
	rounds = 10
	epsilon = 0.6
	
	func2 = boltzmann
	temp = 0.3
	
	regrets = totalExpectedRegret(dist, [func1, func2], [numArms, rounds], [[epsilon], [temp]])
	print regrets 