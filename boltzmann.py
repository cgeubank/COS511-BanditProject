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
		probs = calcBoltzProb(observedMeans, temp)
		
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
def calcBoltzProb(observedMeans,temp):
	l = []
	sum = 0
	for total, count in observedMeans:
		if count != 0:
			sum += math.exp((total/count)/temp)
		else:
			sum += 1
	
	for total, count in observedMeans:
		if count != 0:
			l.append(math.exp((total/count)/temp)/sum)
		else:
			l.append((1.0/sum))
	
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
	eval.printMeans(meanList)
	
	choices = boltzmann(dlist, 0.5)
	print choices