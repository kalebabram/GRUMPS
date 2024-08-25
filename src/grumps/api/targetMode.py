from grumps.core.cleaners import targetCleaner
from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
def targetMode(grumpsObj):
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
