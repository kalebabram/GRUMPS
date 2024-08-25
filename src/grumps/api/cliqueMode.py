from grumps.core.clique import graphBuilder, graphDivider, cliqueWriter
def cliqueMode(grumpsObj):
	graphBuilder(grumpsObj, [])
	grumpsObj.trimmedGraph = graphDivider(grumpsObj)
	# run medoid based cleaning
	if grumpsObj.medoid == 'yes':
		grumpsObj.settingString = grumpsObj.settingString + '_' + 'medoid_filt'
		from grumps.core.clique import graphStatFunction, dictMerge, kmeansSil, outlierFiller, medoidGraphCleaner
		grumpsObj.trimmedGraph, grumpsObj.untrimmedNodes = medoidGraphCleaner(grumpsObj, grumpsObj.trimmedGraph)
		while len(grumpsObj.untrimmedNodes) > 1:
			graphBuilder(grumpsObj, grumpsObj.untrimmedNodes)
			grumpsObj.graphDict = graphDivider(grumpsObj)
			grumpsObj.graphDict, grumpsObj.untrimmedNodes = medoidGraphCleaner(grumpsObj, grumpsObj.graphDict)
			dictMerge(grumpsObj.trimmedGraph, grumpsObj.graphDict)
			if len(grumpsObj.untrimmedNodes) == 1:
				grumpsObj.unconnectedNodes.extend(grumpsObj.untrimmedNodes)
	# write out the cliques
	cliqueWriter(grumpsObj)