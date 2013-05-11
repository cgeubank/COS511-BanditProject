from operator import itemgetter
from epsilonGreedy import epsilonGreedy
from boltzmann import boltzmann
from simplePoker import simplePoker
from pureGuess import pureGuess
from dist import *
from boltzPoker import boltzPoker
from eval import *

import sys

	
# Test main
if __name__ == '__main__':
	# Functions ordered in terms of stability
	func1 = epsilonGreedy
	func2 = boltzmann
	func3 = boltzPoker
	
	# Command line arguments (1. dist; 2. num of rounds; 3. num of trial)
	distNo = int((sys.argv)[1])
	numRounds = int((sys.argv)[2])
	numTrials = int((sys.argv)[3])
	algType = int((sys.argv)[4])
	numArms = 100
	
	# Generate distribution
	dist, muSigmaList = getDist(numArms, numRounds, distNo)
	
	
	print("Max Regret: ", maxRegret((dist, muSigmaList)))
	
	# Do each function 
	if algType == 1:
		print("Doing epsilon-Greedy from 0.05 to 1 in increments of 0.05")
		for epsilon in np.arange(0.05, 1, 0.05):
			sum = 0
			for trial in range(0, numTrials):
				sum += totalExpectedRegret((dist, muSigmaList), None, [func1], [numArms, numRounds], [[epsilon]])[0]
		
			print sum/numTrials	
	
	if algType == 2:
		print("Doing boltzmann from 0.1 to 0.5 in increments of 0.05")
		for tempBoltz in np.arange(0.05, 0.5, 0.05):
			sum = 0
			for trial in range(0, numTrials):
				sum += totalExpectedRegret((dist, muSigmaList), None, [func2], [numArms, numRounds], [[tempBoltz]])[0]
		
			print sum/numTrials	
	
	if algType == 3:
		print("Doing boltzmann-poker from 0.1 to 0.5 in increments of 0.05")
		for tempBoltz in np.arange(0.05, 0.5, 0.05):
			sum = 0
			for trial in range(0, numTrials):
				sum += totalExpectedRegret((dist, muSigmaList), None, [func2], [numArms, numRounds], [[tempBoltz]])[0]	

			print sum/numTrials
