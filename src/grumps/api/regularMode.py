from grumps.core.shared import outlierFiller, outlierCountBuilder, outlierKmeans, finalDF, cleanDFOutput, removedGCAOutput, medoidIDOutput, medoidFinder
def regularMode(grumpsObj):
	# load neccessary functions

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