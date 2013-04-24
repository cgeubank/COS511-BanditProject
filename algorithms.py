import numpy as np
import math
from dist import *
from scipy.stats import rv_discrete

"""
Epsilon-Greedy Algorithm:
Picks random arm with prob epsilon and arm with highest observed mean
with prob (1 - epsilon)
"""
def epsilonGreedy(distList, epsilon):
	#print distList
	armChoices = []
	numRounds = len(distList)
	numArms = len(distList[0])
	
	# Stores the total reward and number of times an arm is selected
	observedMeans = []
	for arm in range(0, numArms):
		observedMeans.append((0.0,0))
	
	for roundIndex in range(0, numRounds):
		prob = np.random.random_sample()
		# With prob less than epsilon, pick random arm
		if (prob < epsilon):
			armIndex = np.random.randint(0, high=numArms)
		# With prob 1 - epsilon, pick arm with highest empirical mean	
		else:
			# Find highest empirical mean
			max = 0.0
			armIndex = -1
			for i in range(0, len(observedMeans)):
				total, count = observedMeans[i]
				if count == 0:
					if armIndex == -1:
						armIndex = i
				else:
					if ((total/count) > max):
						max = total/count
						armIndex = i
			
		# Record choices made
		armChoices.append(armIndex)
		
		# Update the empirical mean for choice made
		observedReward = distList[roundIndex][armIndex]
		prevTotal, prevCount = observedMeans[armIndex] 
		observedMeans[armIndex] = prevTotal + observedReward, prevCount + 1
		
	return armChoices
	
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
		armIndex = list(boltzDist.rvs(size=1))[0]
		
		# Record choices made
		armChoices.append(armIndex)
		
		# Update the empirical mean for choice made
		observedReward = distList[roundIndex][armIndex]
		prevTotal, prevCount = observedMeans[armIndex] 
		observedMeans[armIndex] = prevTotal + observedReward, prevCount + 1
		
	return armChoices

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
	dlist, meanList = normalDistribution(5, 10)
	print dlist
	choices = epsilonGreedy(dlist, 0.5)
	#print choices
	
	dlist, meanList = normalDistribution(5, 10)
	choices = boltzmann(dlist, 0.5)
	print choices
	