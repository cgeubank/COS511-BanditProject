import math
import numpy as np
from scipy import integrate
from scipy import inf
from scipy.integrate import quad
from random import randrange 

from dist import *

"""
Greedy Poker
Assume normal distribution on each arm
Then choose best arm in accordance to epsilon
"""
def greedyPoker(distList, epsilon):
	armChoices = []
	numRounds = len(distList)
	numArms = len(distList[0])
	
	# Keep track of observed rewards for each arm
	listOfRewards = [[] for i in range(0, numArms)]
	
	# Stores the total reward, sum of squared rewards and number of times an arm is selected
	observedMeans = []
	for arm in range(0, numArms):
		observedMeans.append((0.0, 0.0, 0))
	
	# Stores std dev for each arm
	observedStdDevs = []
	for arm in range(0, numArms):
		observedStdDevs.append(0)
		
	# Random indices for arms chosen twice in beginning of iteration	
	# Although second index could be equal to the first, we don't allow this
	# To avoid corner case exceptions
	firstRandomIndex = np.random.randint(0, high=numArms)
	secondRandomIndex = firstRandomIndex
	while secondRandomIndex == firstRandomIndex: 
		secondRandomIndex = np.random.randint(0, high=numArms)
	
	for roundIndex in range(0, numRounds): 
		bestVal = float("-inf")
		seenUnknown = False # flags whether we have looked at an arm with count = 0
		if (roundIndex > 3):
			prob = np.random.random_sample()
			# With prob less than epsilon, pick random arm
			if (prob < epsilon):
				bestIndex = np.random.randint(0, high=numArms)

			else:
				q = 0
				for (reward, squaredreward, times) in observedMeans:
					if times > 0:
						q += 1
					
				# Sort observed means in desc order
				sortedMeanList = sorted(observedMeans, 
					key = lambda arr : float("-inf") if arr[2] == 0 else arr[0]/arr[2], reverse=True)
			
				# Pick highest and sqrt(q) highest means
				highestObservedMean = sortedMeanList[0][0]/sortedMeanList[0][2]
				sqrtQ = int(math.floor(math.sqrt(q)))
				highestQMean = sortedMeanList[sqrtQ][0]/sortedMeanList[sqrtQ][2]
			
				# Calculate delta
				delta = (highestObservedMean - highestQMean)/math.sqrt(q)
			
				# Find arm with best score
				bbestVal = float("-inf")
				bestIndex = -1
				avgMean = averageMean(observedMeans)
				avgStd = averageStdDev(observedStdDevs) 
				for j in range(0, numArms):
					# Get observed Mean for arm
					total, squaredtotal, count = observedMeans[j]

					if count == 0 and seenUnknown:
						continue
					if (count == 0):
						mean = avgMean
					else:
						mean = total/count
					
					# Get observed Std Dev for arm
					if count > 1:
						stdDev = observedStdDevs[j] / math.sqrt(count)
					else:
						stdDev = avgStd
				
					# Calculate Integral
					normalProbDist = lambda x : (1/(math.sqrt(2 * math.pi * stdDev))) * math.exp(-((x - mean) * (x - mean))/(2 * stdDev * stdDev))
					intg = integrate.quad(normalProbDist, highestObservedMean + delta, inf)[0]
								
					# Calculate score for arm				
					value = mean + delta*(numRounds - roundIndex) * intg
					if count == 0:
						seenUnknown = True				
					# Maintain arm with best score
					if (value > bestVal):
						bestVal = value
						bestIndex = j
	
		elif roundIndex <= 1:
			bestIndex = firstRandomIndex
		elif roundIndex <= 3:
			bestIndex = secondRandomIndex

		
		
		# Record choice
		armChoices.append(bestIndex)
		
		# Update observed mean
		observedReward = distList[roundIndex][bestIndex]
		listOfRewards[bestIndex].append(observedReward)
		prevTotal, prevSquaredTotal, prevCount = observedMeans[bestIndex] 
		observedMeans[bestIndex] = prevTotal + observedReward, prevSquaredTotal + observedReward * observedReward, prevCount + 1
		
		# Update observed std dev
		(total, sqtotal, count) = observedMeans[bestIndex]
		if count > 1:
			observedStdDevs[bestIndex] = math.sqrt( (sqtotal/count) - (total/count) * (total/count))
		
	return armChoices
		
def averageMean(observedMeans):
	div = 0
	sum = 0
	for (total, squaredtotal, count) in observedMeans:
		if count > 0:
			div += 1
			sum += (total/count)
	
	return (sum/div)
	
def averageStdDev(stdDevs):
	div = 0
	sum = 0
	for stdDev in stdDevs:
		if stdDev != 0:
			div +=1 
			sum += stdDev
			
	return (sum/div)
	
# Test main
if __name__ == '__main__':
	dlist, muSigmaList = getDist(100, 1000)
	for list in dlist:
		print list

	choices = greedyPoker(dlist, .5)
	print choices
