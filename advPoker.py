import math
from scipy import integrate
from scipy import inf
from scipy.integrate import quad

from dist import *

"""
Simple Poker
Assume normal distribution on each arm
"""
def advPoker(distList):
	armChoices = []
	numRounds = len(distList)
	numArms = len(distList[0])
	
	# Keep track of observed rewards for each arm
	listOfRewards = [[] for i in range(0, numArms)]
	
	# Stores the total reward and number of times an arm is selected
	observedMeans = []
	for arm in range(0, numArms):
		observedMeans.append((0.0,0))
	
	# Stores std dev for each arm
	observedStdDevs = []
	for arm in range(0, numArms):
		observedStdDevs.append(0.0)
	
	firstRandomIndex = np.random.randint(0, high=numArms)
	secondRandomIndex = np.random.randint(0, high=numArms)
	
	bestIndex = -1
	for roundIndex in range(0, numRounds): 
		if (roundIndex > 3):
			q = 0
			for (reward, times) in observedMeans:
				if times > 0:
					q += 1
					
			# Sort observed means in desc order
			sortedMeanList = sorted(observedMeans, 
				key = lambda arr : 0 if arr[1] == 0 else arr[0]/arr[1], 
				reverse=True)
			
			# Pick highest and sqrt(q) highest means
			highestObservedMean = sortedMeanList[0][0]/sortedMeanList[0][1]
			sqrtQ = int(math.sqrt(q))
			highestQMean = sortedMeanList[sqrtQ][0]/sortedMeanList[sqrtQ][1]
			
			# Calculate delta
			delta = (highestObservedMean - highestQMean)/math.sqrt(q)
			
			# Find arm with best score
			bestVal = 0
			bestIndex = -1
			for j in range(0, numArms):
				# Get observed Mean for arm
				total, count = observedMeans[j]
				if (count == 0):
					mean = averageMean(observedMeans)
				else:
					mean = total/count
					
				# Get observed Std Dev for arm
				stdDev = observedStdDevs[i]
				if (stdDev == 0):
					stdDev = averageStdDev(observedStdDevs)
				
				# Calculate Integral
				normalProbDist = lambda x : (1/(stdDev * math.sqrt(math.pi * 2))) * math.exp(-((x - mean) * (x - mean))/(2 * stdDev * stdDev))
				normalIntg = integrate.quad(normalProbDist, highestObservedMean + delta, inf)[0]
				
				#print "normal", normalIntg
				
				invGausDist = lambda x : (1/math.sqrt(2*math.pi*x**3)) * math.exp(-(x-mean)**2/(2*x*mean**2))
				invGausIntg = integrate.quad(invGausDist, highestObservedMean + delta, inf)[0]
				
				#print "invGauss", invGausIntg
				
				gumbelDist = lambda x : ((math.exp(-(x - mean)/0.1))/(0.1))*(math.exp(-math.exp((-(x - mean)/0.1))))
				gumbelIntg = integrate.quad(gumbelDist, highestObservedMean + delta, inf)[0]
				
				#print "gumbel", gumbelIntg
				
				# Calculate score for arm				
				intg = (1.0/3)*normalIntg + (1.0/3)*invGausIntg + (1.0/3)*gumbelIntg
				value = mean + delta * (numRounds - roundIndex) * intg
				#print "score", value, "index", j 
				#print "delta", delta
				#print "diff", numRounds - roundIndex
				
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
		prevTotal, prevCount = observedMeans[bestIndex] 
		observedMeans[bestIndex] = prevTotal + observedReward, prevCount + 1
		newMean = observedMeans[bestIndex][0]/observedMeans[bestIndex][1]
		
		# Update observed std dev
		newStdDev = 0
		for reward in listOfRewards[bestIndex]:
			newStdDev += (reward - newMean)*(reward - newMean)
		
		newStdDev = math.sqrt(newStdDev/len(listOfRewards[bestIndex]))/math.sqrt(len(listOfRewards[bestIndex]))
		observedStdDevs[bestIndex] = newStdDev
		
	return armChoices
		
def averageMean(observedMeans):
	div = 0
	sum = 0
	for (total, count) in observedMeans:
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
	dlist, muSigmaList = getDist(5, 100)
	for list in dlist:
		print list
	
	# Get means of each distribution
	meanList = []
	for (mu, sigma) in muSigmaList:
		meanList.append(mu)
		
	# Print Distribution in sorted order
	eval.printMeans(meanList)
	
	choices = simplePoker(dlist)
	print choices