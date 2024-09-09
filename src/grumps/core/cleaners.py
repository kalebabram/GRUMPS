from pandas import Series
### function for sigma cleaning
def sigmaModeCleaner(grumpsObj):
	from numpy import percentile, mean
	leftDict = dict()
	rightDict = dict()
	for col in grumpsObj.distMat:
		loopSeries = percentile(grumpsObj.distMat[col], q=[.3,99.7])
		leftDict[col] = loopSeries[0]
		rightDict[col] = loopSeries[1]
	leftStat = Series(leftDict)
	rightStat = Series(rightDict)
	leftCutoff = leftStat.mean() + (3 * leftStat.std())
	rightCutoff = rightStat.mean() + (3 * rightStat.std())
	leftStat = leftStat[leftStat <= leftCutoff]
	rightStat = rightStat[rightStat <= rightCutoff]
	grumpsObj.cleanGCA = list(set(leftStat.index) & set(rightStat.index))

### functions for medoid cleaning
def medoidChecker(grumpsObj):
	checkSet = grumpsObj.distMat[grumpsObj.medoidID]
	filteredSet = checkSet[checkSet <= grumpsObj.cutOff]
	filteredSet = filteredSet.dropna()
	returnList = list(filteredSet.index)
	return returnList

def medoidCleaner(grumpsObj):
	removedGCA = list(set(grumpsObj.distMat.index) - set(medoidChecker(grumpsObj)))
	grumpsObj.distMat.drop(columns = removedGCA, index = removedGCA, inplace = True)
	grumpsObj.removedGCA.extend(removedGCA) # this was a self refer that is broken now
	#return removedGCA

### functions for strict mode
def meanCleaner(grumpsObj):
	from numpy import mean
	statDict = dict()
	removedGCA = list(set(grumpsObj.distMat.index) - set(grumpsObj.cleanGCA))
	grumpsObj.distMat.drop(index = removedGCA, columns = removedGCA, inplace=True)
	for col in grumpsObj.distMat:
		statDict[col] = mean(grumpsObj.distMat[col])
	cutOff = Series(statDict).mean() + (Series(statDict).std()*3)
	cleanList = list(Series(statDict)[Series(statDict)<=grumpsObj.cutOff].index)
	grumpsObj.cleanGCA = cleanList


### functions for target mode
def targetCleaner(grumpsObj):
	targetList = []
	for target in grumpsObj.targetList:
		for col in grumpsObjinitialGCA:
			if target in col:
				targetList.append(col)
	try:
		checkSet = grumpsObj.distMat[targetList]
		filteredSet = checkSet[checkSet <= grumpsObj.cutOff]
		filteredSet = filteredSet.dropna()
		returnList = list(filteredSet.index)
		if len(returnList) == 0:
			print('Please check that your targets are correct. There is no \
union between the given targets.')
			return False
		grumpsObj.cleanGCA = returnList
		#grumpsObj.removedGCA = list(set(grumpsObj.initialGCA) - set(returnList))
		#grumpsObj.distMat.drop(columns = removedGCA, index = removedGCA, inplace=True)
		return True
	except KeyError as e:
		raise KeyError('Please check that your target identifiers are correct and in your dataset.') from e

### functions for small mode
def smallModeCleaner(grumpsObj):
	from pandas import DataFrame
	statDict = dict()
	for col in grumpsObj.distMat:
		loop = grumpsObj.distMat[col][[x for x in grumpsObj.distMat.index if col not in x]]
		statDict[col] = loop.describe()
	dfStat = DataFrame(statDict)
	dfStat = dfStat.T
	dfStat = dfStat[dfStat['mean'] <= grumpsObj.cutOff]
	grumpsObj.cleanGCA = list(dfStat.index)
	

