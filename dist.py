import numpy as np
from scipy.stats import invgauss
from random import randrange 
import math as math

# Generates the distribution on the arms with some probability
# Returns list of lists where first level list is by round
# and within each list, it is the number produced by an arm 
def getDist(numArms, numRounds):
	distList = []
	muSigmaList = []
	
	for roundIndex in range(0, numRounds):
		distList.append([])
	
	for armIndex in range(0, numArms):
		distDecision = randrange(1)
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
	
	for roundIndex in range(0, numRounds):
		distList.append([])

	for armIndex in range(0, numArms):
		if armIndex < propBad * numArms:
			dist = np.random.normal((armIndex+1) * 0.0000000001, 0.00000000000000000001, numRounds)
		else:
			dist = np.random.normal(magGood, 0.00000000000000000001, numRounds)

		for i in range(0, numRounds):
			distList[i].append(dist[i])

	return distList

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
	
# Test main
if __name__ == '__main__':
	dlist, meanList = getDist(5, 10)
	for list in dlist:
		print list