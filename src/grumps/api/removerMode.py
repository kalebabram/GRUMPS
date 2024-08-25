from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
def removerMode(grumpsObj):
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