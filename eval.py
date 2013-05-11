from operator import itemgetter
from epsilonGreedy import epsilonGreedy
from boltzmann import boltzmann
from simplePoker import simplePoker
from pureGuess import pureGuess
from dist import *
from boltzPoker import boltzPoker
from greedyPoker import *

import sys

"""
Returns total expected regret for a certain algorithm 
run on a certain distribution
"""
def totalExpectedRegret((dist, muSigmaList), distributionMethod, algorithms, distParams, algParams):
	if dist is None:
		# Generate Distribution
		dist, muSigmaList = distributionMethod(*distParams)
	
	numRounds = len(dist)
	
	# Get means of each distribution
	meanList = []
	for (mu, sigma) in muSigmaList:
		meanList.append(mu)
		
	# Print Distribution in sorted order
	#printMeans(meanList)
	
	regrets = []
	algParamIndex = 0
	
	# Calculate expected regret for each algorithm for this distribution
	for alg in algorithms:
		armChoices = alg(dist, *(algParams[algParamIndex]))
	
		# print out choices 
		#printChoices(str(alg), armChoices, meanList)
	
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
	
"""
Prints mean in descending order, including arm index
"""
def printMeans(meanList):
	l = [(i[0], i[1]) for i in sorted(enumerate(meanList), key=lambda x:x[1], reverse=True)]
	for pair in l:
		print (str(pair))

"""
Prints the arm choices made by algorithm
"""	
def printChoices(name, armChoices, meanList):
	print (name + ": ")
	round = 0
	for choice in armChoices:
		print "Round %r: Index: %r, Mean: %r " % (round, choice, meanList[choice])
		round += 1
		
"""
Print max regret for a certain distribution and number of Rounds
"""
def maxRegret((dist, muSigmaList)):
	numRounds = len(dist)
	maxMean = max(muSigmaList, key = itemgetter(0))[0]
	minMean = min(muSigmaList, key = itemgetter(0))[0]

	# Calculate max regret
	regret = (maxMean - minMean) * numRounds
	
	return regret
	
# Test main
if __name__ == '__main__':
	# Functions ordered in terms of stability
	func1 = epsilonGreedy
	func2 = greedyPoker
	func3 = simplePoker
	func4 = boltzmann
	func5 = boltzPoker
	func6 = pureGuess
	
	# Command line arguments (1. dist; 2. num of rounds; 3. num of trial)
	distNo = int((sys.argv)[1])
	numRounds = int((sys.argv)[2])
	numTrials = int((sys.argv)[3])
	numArms = 100
	
	# Generate distribution
	dist, muSigmaList = getDist(numArms, numRounds, distNo)
	
	# Optimal Epsilon 
	epsilon = 0.07

	# Optimal Epsilon for Poker
	epsilonPoker = 0.07
	
	# Optimal Temp(boltz)
	tempBoltz = 0.15
	
	# Optial Temp(bolz-Poker)
	tempBoltzPoker = 0.15
	
	print("Max Regret: ", maxRegret((dist, muSigmaList)))
	
	# Do each function 
	print("Doing epsilon-Greedy")
	sum = 0
	for trial in range(0, numTrials):
		sum += totalExpectedRegret((dist, muSigmaList), None, [func1], [numArms, numRounds], [[epsilon]])[0]
		
	print("Regret: ", sum/numTrials)	

	# Do each function 
	print("Doing greedy Poker")
	sum = 0
	for trial in range(0, numTrials):
		sum += totalExpectedRegret((dist, muSigmaList), None, [func2], [numArms, numRounds], [[epsilonPoker]])[0]
		
	print("Regret: ", sum/numTrials)
	
	print("Doing simple Poker")
	sum = 0
	for trial in range(0, numTrials):
		sum += totalExpectedRegret((dist, muSigmaList), None, [func3], [numArms, numRounds], [[]])[0]
		
	print("Regret: ", sum/numTrials)	
	
	print("Doing boltzmann")
	sum = 0
	for trial in range(0, numTrials):
		sum += totalExpectedRegret((dist, muSigmaList), None, [func4], [numArms, numRounds], [[tempBoltz]])[0]
		
	print("Regret: ", sum/numTrials)	
	
	print("Doing boltzmann-poker")
	sum = 0
	for trial in range(0, numTrials):
		sum += totalExpectedRegret((dist, muSigmaList), None, [func5], [numArms, numRounds], [[tempBoltzPoker]])[0]
		
	print("Regret: ", sum/numTrials)	

	print("Doing purely random guessing")
	sum = 0
	for trial in range(0, numTrials):
		sum += totalExpectedRegret((dist, muSigmaList), None, [func6], [numArms, numRounds], [[]])[0]
		
	print("Regret: ", sum/numTrials)
	
