from networkx import Graph, connected_components
from numpy import argmin
from pandas import DataFrame, Series, concat
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

### functions for clique mode
def dictMerge(dict1, dict2):
	return(dict1.update(dict2))

def graphBuilder(grumpsObj, aList):
	if len(aList) > 0:
		unstack = grumpsObj.distMat[aList].loc[aList].unstack()
	else:
		unstack = grumpsObj.distMat.unstack()
	unstackIndex = list(unstack.index)
	unstackIndex = [tuple(sorted(i)) for i in unstackIndex]
	unstackIndex = list(set(unstackIndex))
	unstack = unstack[unstack.index.isin(unstackIndex)]
	unstack = unstack[unstack < grumpsObj.cutOff]
	grumpsObj.untrimmedGraph = Graph()
	grumpsObj.untrimmedGraph.add_nodes_from([x[0] for x in list(unstack.index)])
	grumpsObj.untrimmedGraph.add_edges_from(list(unstack.index))
	#return untrimmedGraph

def graphDivider(grumpsObj):
	i = grumpsObj.graphID
	unconnected = []
	funcDict = dict()
	for x in (grumpsObj.untrimmedGraph.subgraph(c) for c in connected_components(grumpsObj.untrimmedGraph)):
		if len(list(x.nodes)) > 1:
			funcDict['clique_' + str(i)] = list(x.nodes)
			i+=1
		if len(list(x.nodes)) < 2:
			grumpsObj.unconnectedNodes.extend(list(x.nodes))
	#grumpsObj.trimmedGraph = dictMerge(grumpsObj.trimmedGraph,funcDict)
	grumpsObj.graphID = i
	return funcDict

def graphStatFunction(distMat, aBool):
	stats = distMat.describe(percentiles = [.1,.25,.5,.75,.9,.95,.997])
	stats = stats[stats.index.isin(['10%','25%','50%','75%','90%','95%','99.7%'])]
	statsT = stats.T.describe()
	checkStat = statsT.loc['max'][statsT.loc['max'] >0.05].index[0]
	dropList = list(stats[stats[stats.index == checkStat]>0.05].dropna(how='all').loc[checkStat].dropna().index)
	if len(dropList) > 0:
		aBool = True
	else:
		aBool = False
	return dropList, aBool

def kmeansSil(numClusters, xVals):
	silScore = []
	for num in numClusters:
		kms = KMeans(n_clusters=num)
		kms.fit(xVals)
		silScore.append(silhouette_score(xVals, kms.labels_))
	return silScore	

def outlierFiller(grumpsObj,distMat):
	outlierSize = round(len(distMat) * .05) + 2
	aboveCutoff = grumpsObj.cutOff * 1.02
	outlierSim = grumpsObj.cutOff/10
	outlierList = [aboveCutoff]*len(distMat)
	loopList = [outlierSim] * outlierSize
	tempDF1 = DataFrame()
	indexList = list(distMat.columns)
	for val in range(1,outlierSize+1):
		tempDF1['outlier_' + str(val)] = outlierList
	tempDF1.index = indexList
	tempDF1 = tempDF1.T
	distMat = concat([distMat, tempDF1])
	tempDF2 = pd.DataFrame()
	for val in range(0,outlierSize):
		subloopList = loopList[:]
		subloopList[val] = 0
		indexList.append('outlier_' + str(val))
		tempDF2['outlier_' + str(val+1)] = outlierList + subloopList
	tempDF2.index = indexList
	distMat = concat([distMat,tempDF2])
	return distMat

def medoidGraphCleaner(grumpsObj, aGraphDict):
	initialGraphID = grumpsObj.graphID
	numClusters = [i for i in range(2,11)]
	rerunDict = dict()
	keepDict = dict()
	for clique in aGraphDict.keys():
		loopDF = grumpsObj.distMat[aGraphDict[clique]].loc[aGraphDict[clique]]
		loopDF = outlierFiller(grumpsObj,loopDF)
		loopDFScaled = StandardScaler().fit_transform(loopDF)
		if len(loopDF) < 11:
			numClusters = [i for i in range(2,len(loopDF) - 1)]
		loopSilScores = kmeansSil(numClusters, loopDFScaled)
		kmeansClusters = numClusters[loopSilScores.index(max(loopSilScores))]
		loopKMeans = KMeans(n_clusters = kmeansClusters)
		loopKMeans.fit(loopDFScaled)
		loopDict = dict(zip(loopDF.index,list(loopKMeans.labels_)))
		loopSeries = Series(loopDict)
		loopSeries = loopSeries[~loopSeries.index.str.contains('outlier_')]
		loopMedoidList = []
		loopGroupList = list(set(loopSeries))
		for group in loopGroupList:
			subloopList = list(loopSeries[loopSeries == group].index)
			subloopDF = loopDF[subloopList].loc[subloopList]
			subloopMedoid = subloopDF.iloc[argmin(subloopDF.sum(axis=0))].name
			loopMedoidList.append(subloopMedoid)
		loopMedoidDF = loopDF[loopMedoidList].loc[loopMedoidList]
		rerun = True
		while rerun:
			try:
				loopDropList, rerun = graphStatFunction(loopMedoidDF,rerun)
				loopMedoidDF.drop(columns = [loopDropList[0]], index = [loopDropList[0]], inplace = True)
			except:
				rerun = False
				continue
		loopInSpeciesMedoids = list(loopMedoidDF.index)
		loopOutSpeciesMedoids = list(set(loopMedoidList) - set(loopInSpeciesMedoids))
		loopInGroups = list(loopSeries[loopInSpeciesMedoids])
		loopOutGroups = list(loopSeries[loopOutSpeciesMedoids])
		loopInSpecies = list(loopSeries[loopSeries.isin(loopInGroups)].index)
		loopOutSpecies = list(loopSeries[loopSeries.isin(loopOutGroups)].index)
		keepDict[clique] = loopInSpecies
		rerunDict['clique_' + str(initialGraphID)] = loopOutSpecies
		initialGraphID += 1
		rerunList = []
		for x in rerunDict.values():
			rerunList.extend(x)
	return keepDict,rerunList

def trimmedGraphMedoidChecker(grumpsObj):
	i = 1
	unconnectedList = []
	connectedDict = dict()
	for aKey in grumpsObj.trimmedGraph.keys():
		if len(grumpsObj.trimmedGraph[aKey]) >1:
			connectedDict['clique_' + str(i)] = grumpsObj.trimmedGraph[aKey]
			i+=1
		else:
			unconnectedList.extend(grumpsObj.trimmedGraph[aKey])
	grumpsObj.unconnectedNodes.extend(unconnectedList)
	grumpsObj.trimmedGraph = connectedDict

def cliqueWriter(grumpsObj):
	stringy = grumpsObj.mode + '_' + str(grumpsObj.cutOff)
	if grumpsObj.medoid == 'yes':
		stringy = stringy + '_medoid_filt'
	medoidDict = dict()
	for key in grumpsObj.trimmedGraph.keys():
		try:
			outfp = grumpsObj.mashFile.split('.csv')[0] + '_' + key + '_' + stringy + '_distmat.csv'
		except:
			outfp = grumpsObj.mashFile + '_' + key + '_' + stringy + '_distmat.csv'
		loopDF = grumpsObj.distMat[grumpsObj.trimmedGraph[key]].loc[grumpsObj.trimmedGraph[key]]
		loopDF.to_csv(outfp)
		medoidDict[key] = loopDF.iloc[argmin(loopDF.sum(axis=0))].name
	medoidDF = DataFrame(data = zip(medoidDict.keys(),medoidDict.values()), columns=['clique','medoid'])
	medoidDF['sort'] = [int(x.split('_')[-1]) for x in medoidDF['clique']]
	medoidDF.sort_values(by=['sort'], inplace = True)
	del medoidDF['sort']
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_medoids_' + stringy + '.csv'
	except:
		outfp = grumpsObj.mashFile + '_medoids_' + stringy + '.csv'
	medoidDF.to_csv(outfp,index = False)
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_unconnected_' + stringy + '.txt'
	except:
		outfp = grumpsObj.mashFile + '_unconnected_' + stringy + '.txt'		
	with open(outfp, 'w') as outfile:
		outfile.write('\n'.join(grumpsObj.unconnectedNodes))
		
def medoidFinder(grumpsObj):
	grumpsObj.medoidID = grumpsObj.distMat.iloc[argmin(grumpsObj.distMat.sum(axis=0))].name
	
def medoidIDOutput(grumpsObj):
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_cleaned_' + grumpsObj.settingString + '_medoid'
	except:
		outfp = grumpsObj.mashFile + '_cleaned_' + grumpsObj.settingString + '_medoid'
	with open(outfp, 'w') as outfile:
		outfile.writelines('\n'.join([grumpsObj.medoidID]))



