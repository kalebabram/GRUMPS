from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
def regularMode(grumpsObj):
	"""
	Runs the regular or strict mode of GRUMPS using a grumpsObj
	"""
	# load neccessary functions
	from grumps.core.shared import outlierFiller, outlierCountBuilder, outlierKmeans, finalDF
	# if cutoff is set by user run that value is used otherwise 0.05
	outlierFiller(grumpsObj)
	outlierCountBuilder(grumpsObj)
	outlierKmeans(grumpsObj)
	
	# make clean dataframe for outputting
	finalDF(grumpsObj)

	if grumpsObj.mode == 'strict':
		from grumps.core.cleaners import meanCleaner
		# run mean cleaner
		meanCleaner(grumpsObj)
		# make clean dataframe for outputting
		finalDF(grumpsObj)

	if grumpsObj.sigma == 'yes':
		from grumps.core.cleaners import sigmaModeCleaner
	# now run sigma cleaner
		sigmaModeCleaner(grumpsObj)
		grumpsObj.settingString = grumpsObj.mode + '_' + 'sigma_'+ \
		str(grumpsObj.cutOff) + '_' + grumpsObj.clusterMethod
	# make clean dataframe for outputting
		finalDF(grumpsObj)
	
	# identify the medoid of the cleaned dataset
	medoidFinder(grumpsObj)
	
	if grumpsObj.medoid == 'yes':
		grumpsObj.settingString = grumpsObj.settingString + '_' + 'medoid_filt'
		from grumps.core.cleaners import medoidChecker, medoidCleaner
	# now run medoid cleaner
		medoidCleaner(grumpsObj)
	# make clean dataframe for outputting
		finalDF(grumpsObj)
	# identify new medoid on the off chance it has changed
		medoidFinder(grumpsObj)

	# if user doesn't disable heatmap this will trigger and make the heatmap	
	if grumpsObj.makeHeatmap == 'yes':
		from grumps.core.shared import heatmapMaker
		heatmapMaker(grumpsObj)

	# outputs the final clean dataframe		
	cleanDFOutput(grumpsObj)
	# write out the removed genome list 
	removedGCAOutput(grumpsObj)
	# write out the identified medoid
	medoidIDOutput(grumpsObj)

def cliqueMode(grumpsObj):
	"""
	Runs the clique mode of GRUMPS using a grumpsObj
	"""
	from grumps.core.clique import graphBuilder, graphDivider, cliqueWriter
	graphBuilder(grumpsObj, [])
	grumpsObj.trimmedGraph = graphDivider(grumpsObj)
	# run medoid based cleaning
	if grumpsObj.medoid == 'yes':
		#grumpsObj.settingString = grumpsObj.settingString + '_' + 'medoid_filt'
		from grumps.core.clique import graphStatFunction, dictMerge, kmeansSil, outlierFiller, medoidGraphCleaner, trimmedGraphMedoidChecker
		grumpsObj.trimmedGraph, grumpsObj.untrimmedNodes = medoidGraphCleaner(grumpsObj, grumpsObj.trimmedGraph)
		while len(grumpsObj.untrimmedNodes) > 1:
			graphBuilder(grumpsObj, grumpsObj.untrimmedNodes)
			grumpsObj.graphDict = graphDivider(grumpsObj)
			grumpsObj.graphDict, grumpsObj.untrimmedNodes = medoidGraphCleaner(grumpsObj, grumpsObj.graphDict)
			dictMerge(grumpsObj.trimmedGraph, grumpsObj.graphDict)
			if len(grumpsObj.untrimmedNodes) == 1:
				grumpsObj.unconnectedNodes.extend(grumpsObj.untrimmedNodes)
		# run the trimmedGraph medoid checker
		trimmedGraphMedoidChecker(grumpsObj)
	# write out the cliques
	cliqueWriter(grumpsObj)

def removerMode(grumpsObj):
	"""
	Runs the remover mode of GRUMPS using a grumpsObj
	"""	
	try:
		with open(grumpsObj.removeFilePath, 'r') as infile:
			grumpsObj.removeList = infile.readlines()
		grumpsObj.removeList = [x.split('\n')[0] for x in grumpsObj.removeList]
		try:
			# identify genomes to retain
			grumpsObj.cleanGCA = list(set(list(grumpsObj.distMat.index)) - set(grumpsObj.removeList))
			# create the clean dataframe for the target genomes
			finalDF(grumpsObj)
			# identify the medoid
			medoidFinder(grumpsObj)
			# if user doesn't disable heatmap this will trigger and make the heatmap	
			if grumpsObj.makeHeatmap == 'yes':
				from grumps.core.shared import heatmapMaker
				heatmapMaker(grumpsObj)
			# output the final clean dataframe
			cleanDFOutput(grumpsObj)
		# write out the removed genome list 
			removedGCAOutput(grumpsObj)
		# write out the medoid
			medoidIDOutput(grumpsObj)
		except KeyError as e:
			raise KeyError('Please check that your genome identifiers are correct and in your datasets.') from e
	except FileNotFoundError as e:
		raise FileNotFoundError("The file: \"" + grumpsObj.removeFilePath + '\" \
cannot be found. Please double check the file name and provide the complete \
filepath to \"-r\" when running in remover mode.') from e

def sigmaMode(grumpsObj):
	"""
	Runs the sigma mode of GRUMPS using a grumpsObj
	"""
	from grumps.core.cleaners import sigmaModeCleaner
	# if cutoff is set by user run that value is used otherwise 0.05
	# now run sigma cleaner
	sigmaModeCleaner(grumpsObj)
	# make clean dataframe for outputting
	finalDF(grumpsObj)
	# identify the medoid
	medoidFinder(grumpsObj)
	# if user doesn't disable heatmap this will trigger and make the heatmap	
	if grumpsObj.makeHeatmap == 'yes':
		from grumps.core.shared import heatmapMaker
		heatmapMaker(grumpsObj)
	# outputs the final clean dataframe		
	cleanDFOutput(grumpsObj)
	# write out the removed genome list 
	removedGCAOutput(grumpsObj)
	# write out the medoidID
	medoidIDOutput(grumpsObj)

def smallMode(grumpsObj):
	"""
	Runs the small mode of GRUMPS using a grumpsObj
	"""	
	from grumps.core.cleaners import smallModeCleaner
	# identify genomes where average (ignoring self-self) is > than cutoff
	smallModeCleaner(grumpsObj)
	# make clean dataframe for outputting
	finalDF(grumpsObj)
	# identify the medoid
	medoidFinder(grumpsObj)
	# if user doesn't disable heatmap this will trigger and make the heatmap	
	if grumpsObj.makeHeatmap == 'yes':
		from grumps.core.shared import heatmapMaker
		heatmapMaker(grumpsObj)
	# outputs the final clean dataframe
	cleanDFOutput(grumpsObj)
	# write out the removed genome list 
	removedGCAOutput(grumpsObj)
	# write out the medoids
	medoidIDOutput(grumpsObj)

def summaryMode(grumpsObj):
	"""
	Runs the summary mode of GRUMPS using a grumpsObj
	"""
	from grumps.core.summary import statBuilder, statSummary, distroCheck
	distroCheck(grumpsObj)
	statBuilder(grumpsObj)
	statSummary(grumpsObj)

def targetMode(grumpsObj):
	"""
	Runs the target mode of GRUMPS using a grumpsObj
	"""	
	from grumps.core.cleaners import targetCleaner
	try:
		with open(grumpsObj.targetFilePath, 'r') as infile:
			grumpsObj.targetList = infile.readlines()
		# save the list in the object
		grumpsObj.targetList = [x.split('\n')[0] for x in grumpsObj.targetList]
		grumpsObj.targetSuccess = targetCleaner(grumpsObj)
		if grumpsObj.targetSuccess == True:
			# clean the dataset
			finalDF(grumpsObj)
		# identify the medoid of the dataset
			medoidFinder(grumpsObj)
			if len(grumpsObj.distMat) < len(grumpsObj.initialGCA):
	# if user doesn't disable heatmap this will trigger and make the heatmap	
				if grumpsObj.makeHeatmap == 'yes':
					from grumps.modes.shared import heatmapMaker
					heatmapMaker(grumpsObj)
		# outputs the final clean dataframe
				cleanDFOutput(grumpsObj)
				# write out the removed genome list 
				removedGCAOutput(grumpsObj)
				# write out the identified medoid
				medoidIDOutput(grumpsObj)
			if len(grumpsObj.distMat) == len(grumpsObj.initialGCA):
				print('The provided targets did not filter any genomes.')
				print('If this is unexpected, please double check the provided targets.')
	except FileNotFoundError as e:
		raise FileNotFoundError("The file: \"" + grumpsObj.targetFilePath + '\" \
cannot be found. Please double check the file name and provide the complete \
filepath to \"-t\" when running in target mode.') from e
