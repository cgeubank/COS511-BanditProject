import math
from scipy.stats import rv_discrete

from dist import *

from random import randrange 

"""
Pure Guessing
Each round randomly pick an arm with uniform probability
"""
def pureGuess(distList):
	armChoices = []
	numRounds = len(distList)
	numArms = len(distList[0])

	for roundIndex in range(0, numRounds):
		armChoices.append(randrange(numArms))	
	
	return armChoices
	
# Test main
if __name__ == '__main__':
	dlist, muSigmaList = getDist(5, 100)
	for list in dlist:
		print list
	
	# Get means of each distribution
	#meanList = []
	#for (mu, sigma) in muSigmaList:
	#	meanList.append(mu)
		
	# Print Distribution in sorted order
	#eval.printMeans(meanList)
	
	choices = pureGuess(dlist)
	print choices