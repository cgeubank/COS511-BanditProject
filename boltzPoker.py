import math
import numpy as np
from scipy import integrate
from scipy import inf
from scipy.integrate import quad
from random import randrange 
from scipy.stats import rv_discrete

from dist import *

"""
Boltzmann Poker
Assume normal distribution on each arm
Calculates the value of p_i for each arm during each round
Next, uses these p_i values as weights for boltzmann distribution
"""
def boltzPoker(distList, temp):
	armChoices = []
	numRounds = len(distList)
	numArms = len(distList[0])
	
	# Keep track of observed rewards for each arm
	listOfRewards = [[] for i in range(0, numArms)]
	
	# Stores the total reward, sum of squared rewards and number of times an arm is selected
	observedMeans = []
	for arm in range(0, numArms):
		observedMeans.append((0.0, 0.0, 0))

	# Stores the arm indices
	indices = []
	for index in range(0, numArms):
		indices.append(index)
	
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
		armValues = []
		if (roundIndex > 3):
			q = 0
			for (reward, squaredreward, times) in observedMeans:
				if times > 0:
					q += 1
					
			# Sort observed means in desc order
			sortedMeanList = sorted(observedMeans, 
				key = lambda arr : float("-inf") if arr[2] == 0 else arr[0]/arr[2], 
				reverse=True)
			
			# Pick highest and sqrt(q) highest means
			highestObservedMean = sortedMeanList[0][0]/sortedMeanList[0][2]
			sqrtQ = int(math.floor(math.sqrt(q)))
			highestQMean = sortedMeanList[sqrtQ][0]/sortedMeanList[sqrtQ][2]
			
			# Calculate delta
			delta = (highestObservedMean - highestQMean)/math.sqrt(q)
			
			# Find arm with best score
			bestVal = float("-inf")
			bestIndex = -1
			for j in range(0, numArms):
				# Get observed Mean for arm
				total, squaredtotal, count = observedMeans[j]
				if (count == 0):
					mean = averageMean(observedMeans)
				else:
					mean = total/count
					
				# Get observed Std Dev for arm
				if count > 1:
					stdDev = observedStdDevs[j] / math.sqrt(count)
				else:
					stdDev = averageStdDev(observedStdDevs) # QUESTION: DO WE NORMALIZE THIS AS WELL?
				
				# Calculate Integral
				normalProbDist = lambda x : (1/(math.sqrt(2 * math.pi * stdDev))) * math.exp(-((x - mean) * (x - mean))/(2 * stdDev * stdDev))
				intg = integrate.quad(normalProbDist, highestObservedMean + delta, inf)[0]
				
				#print "normal", intg
				
				# Calculate score for arm				
				value = mean + delta*(numRounds - roundIndex) * intg
				#print "score", value, "index", j 
				
				# Maintain arm with best score
				armValues.append(value)

		if roundIndex <= 1:
			bestIndex = firstRandomIndex
		elif roundIndex <= 3:
			bestIndex = secondRandomIndex
		else:
			#normalize arm values to have max value of 1 so as to prevent overflow
			maxVal = float("-inf")
			minVal = float("inf")
			for i in range(0, numArms):
				if armValues[i] > maxVal:
					maxVal = armValues[i]
				if armValues[i] < minVal:
					minVal = armValues[i]
	
			for i in range(0, numArms):
				armValues[i] = (armValues[i] - minVal) / (maxVal - minVal)
				
                    
			probs = calcBoltzProb(armValues, temp)
			boltzDist = rv_discrete(name='custm', values=[tuple(indices), tuple(probs)])
			bestIndex = boltzDist.rvs(size=1)[0]
			
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

"""
Gives Boltzmann probability distribution according to the observed prices/values
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
	dlist, muSigmaList = getPathologicalDist(10,50,.5,1)#getDist(5, 50)
	#for list in dlist:
		#print list
	
	# Get means of each distribution
	#meanList = []
	#for (mu, sigma) in muSigmaList:
	#	meanList.append(mu)
		
	# Print Distribution in sorted order
	#eval.printMeans(meanList)
	
	choices = boltzPoker(dlist, .1)
	print choices
