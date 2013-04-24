import numpy as np

# Returns List of numbers that follow normal distribution
def normalDistribution(numArms, numRounds):
	# 2-D List where each contained list represents a round
	completeList = []
	
	# list containing mu, sigma for each arm's distribution
	meanList = []

	# mean and standard deviation - generated randomly from (0,1)
	for armIndex in range(0, numArms):
		mu, sigma = np.random.random_sample(), np.random.random_sample()
		meanList.append(mu)
	
	# empty list for each round
	for armIndex in range(0, numRounds):
		completeList.append([])
	
	# generate numbers for each round
	for armIndex in range(0, numArms): 
		# use normal distribution for each arm
		dist = np.random.normal(mu, sigma, numRounds)
		
		# split dist into separate rounds
		roundIndex = 0
		for num in dist:
			(completeList[roundIndex]).append(num);
			roundIndex += 1
		
	return completeList, meanList
	
# Test main
if __name__ == '__main__':
	dlist, meanList = normalDistribution(5, 1)
	for list in dlist:
		print list