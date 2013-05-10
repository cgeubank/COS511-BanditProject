import math
from scipy.stats import rv_discrete

from dist import *

"""
Boltzmann Exploration
Pick each arm with a probability that is proportional to its average reward
In this case, we use boltzmann distribution.

The temp variable controls the randomness of the choice.
temp = 0 => pure greedy, temp = infinity => arms picked u.a.r
"""
def boltzmann(distList, temp):
	armChoices = []
	numRounds = len(distList)
	numArms = len(distList[0])

	indices = []
	for index in range(0, numArms):
		indices.append(index)
	
	# Stores the total reward and number of times an arm is selected
	observedMeans = []
	for arm in range(0, numArms):
		observedMeans.append((0.0,0))

	for roundIndex in range(0, numRounds):

		#normalize means to prevent overflow
		normalizedMeans = []
		minVal = float("inf")
		maxVal = float("-inf")
		for (total, count) in observedMeans:
			if count == 0:
				continue
			mean = total/count
			if mean < minVal:
				minVal = mean
			if mean > maxVal:
				maxVal = mean
		
		for (total, count) in observedMeans:
			if count == 0:
				normalizedMeans.append(0.0)
				continue
			mean = total/count
			if minVal == maxVal:
				normalizedMeans.append(mean)
				continue
			normalizedMeans.append((mean-minVal)/(maxVal-minVal))

		probs = calcBoltzProb(normalizedMeans, temp)
		
		boltzDist = rv_discrete(name='custm', values=[tuple(indices), tuple(probs)])
		armIndex = boltzDist.rvs(size=1)[0]
		
		# Record choices made
		armChoices.append(armIndex)
		
		# Update the empirical mean for choice made
		observedReward = distList[roundIndex][armIndex]
		prevTotal, prevCount = observedMeans[armIndex] 
		observedMeans[armIndex] = prevTotal + observedReward, prevCount + 1
		
	return armChoices

"""
Gives Boltzmann probability distribution according to the observed mean of
choices 
"""
def calcBoltzProb(observedValues, temp):
	l = []
	sum = 0.0
	for value in observedValues:
		sum += math.exp(value/temp)
	
	for value in observedValues:
		l.append(math.exp(value/temp)/sum)

	return l
	
# Test main
if __name__ == '__main__':
	dlist, muSigmaList = getDist(5, 100)
	for list in dlist:
		print list
	
	# Get means of each distribution
	meanList = []
	for (mu, sigma) in muSigmaList:
		meanList.append(mu)
		
	# Print Distribution in sorted order
	#eval.printMeans(meanList)
	
	choices = boltzmann(dlist, 0.5)
	print choices