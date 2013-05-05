import numpy as np

from dist import *

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
	
	choices = epsilonGreedy(dlist, 0.5)
	print choices