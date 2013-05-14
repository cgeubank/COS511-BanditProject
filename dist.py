import numpy as np
from scipy.stats import invgauss
from random import randrange 
import math as math

import csv

def getDistFromFile():
	distList = []
	muSigmaList = []
	
	numArms = 760
	numRounds = 1361
	
	# empty list for each round
	for roundIndex in range(0, numRounds):
		distList.append([])
	
	# csv reader to read from text file
	filename = "univ-latencies.txt"
	file = open(filename, "r")
	csv_reader = csv.reader(file)
	
	# Read rewards from text file
	lineCount = 0
	for line in csv_reader:
		lineCount += 1
		
		# First line is just list of universities, so skip
		if lineCount == 1:
			continue
		else:
			# Each line contains the rewards for a certain round
			roundIndex = 0
			for reward in line:
				distList[lineCount - 2].append(-1.0 * float(reward)) # negative rewards since we are dealing with payoffs

	# Given that the values are in integers, add a small bit of Gaussian noise to prevent std. dev of 0
	for armIndex in range(0, numArms):
		for roundIndex in range(0, numRounds):
			distList[roundIndex][armIndex] += np.random.normal(0, 1)
			
	# Calculate mean and standard deviation from reward info
	for armIndex in range(0, numArms):
		# Mean:
		mean = 0.0
		for roundIndex in range(0, numRounds):
			mean += distList[roundIndex][armIndex]
		
		mean = mean/numRounds;
		
		# Std Deviation:
		stdDev = 0.0
		for roundIndex in range(0, numRounds):
			stdDev += (distList[roundIndex][armIndex] - mean)*(distList[roundIndex][armIndex] - mean)
			
		stdDev = math.sqrt(stdDev/numRounds)
		
		# Record mean and std dev for each arm
		muSigmaList.append((mean, stdDev))
		
	return distList, muSigmaList
	

# Generates the distribution on the arms with some probability
# Returns list of lists where first level list is by round
# and within each list, it is the number produced by an arm 
def getDist(numArms, numRounds, distDecision = 0):
	distList = []
	muSigmaList = []
	
	for roundIndex in range(0, numRounds):
		distList.append([])
	
	for armIndex in range(0, numArms):
		if distDecision == 0:
			dist, muSigma = normalDistribution(numRounds)
		elif distDecision == 1:
			dist, muSigma = inverseGaussian(numRounds)
		elif distDecision == 2:
			dist, muSigma = gumbel(numRounds)
			
		for i in range(0, numRounds):
			distList[i].append(dist[i])
			
		muSigmaList.append(muSigma)
		
	return distList, muSigmaList 
		
# Returns List of numbers that follow normal distribution
def normalDistribution(numRounds):
	# mean and standard deviation - generated randomly from (0,1)
	mu, sigma = np.random.random_sample(), np.random.random_sample()
	
	# use normal distribution for arm
	dist = np.random.normal(mu, sigma, numRounds)
	
	return dist, (mu, sigma)

# Returns a distribution in which the first propBad arms are close to zero (but not equal)
# The rest of the arms have reward magGood
def getPathologicalDist(numArms, numRounds, propBad, magGood):
	distList = []
	muSigmaList = []
	
	for roundIndex in range(0, numRounds):
		distList.append([])

	for armIndex in range(0, numArms):
		if armIndex < propBad * numArms:
			dist = np.random.normal((armIndex+1) * 0.0000000001, 0.00001, numRounds)
			muSigma = ((armIndex+1) * 0.0000000001, 0.00001)
		else:
			dist = np.random.normal(magGood, 1, numRounds)
			muSigma = (magGood, 1)

		for i in range(0, numRounds):
			distList[i].append(dist[i])

		muSigmaList.append(muSigma)

	return distList, muSigmaList

# Returns List of numbers that follow inverse Gaussian distribution	
def inverseGaussian(numRounds):
	mu = np.random.random_sample()
	sigma = math.sqrt(invgauss.var(mu))
	
	# use inverse Gaussian distribution for arm
	dist = invgauss.rvs(mu, size=numRounds)
	
	return dist, (mu, sigma)
	
# Returns list of numbers that follow Gumbel distribution
def gumbel(numRounds):
	mu = np.random.random_sample();
	beta = 0.1;
	
	# use Gumbel distribution for arm
	dist = np.random.gumbel(mu, beta, numRounds)
	
	# fix mean and std deviation
	mu = mu + 0.57721 * beta 
	var = ((math.pi * math.pi)/6)*(beta * beta)
	sigma = math.sqrt(var)
	
	return dist, (mu, sigma)

# Normalize the distribution so means are in [0,1]
# Does not do anything to standard deviations
def normalizeDist(dlist, meanList):
	numRounds = len(dlist)
	numArms = len(dlist[0])

	minVal = float("inf")
	maxVal = float("-inf")
	
	for i in range(0, len(meanList)):
		(mu, sigma) = meanList[i]
		if mu < minVal:
			minVal = mu
		if mu > maxVal:
			maxVal = mu

	for i in range(0, len(meanList)):
		(mu, sigma) = meanList[i]
		meanList[i] = ((mu-minVal)/(maxVal-minVal), sigma)

	for armIndex in range(0, numArms):
		for roundIndex in range(1, numRounds):
			dlist[roundIndex][armIndex] = (dlist[roundIndex][armIndex]-minVal)/(maxVal-minVal)

	return dlist, meanList
	
# Test main
if __name__ == '__main__':
	dlist, meanList = getDist(5, 10)
	for list in dlist:
		print list
		