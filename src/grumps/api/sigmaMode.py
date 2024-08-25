from grumps.core.cleaners import sigmaModeCleaner
from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
def sigmaMode(grumpsObj):
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