from grumps.core.cleaners import smallModeCleaner
from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
def smallMode(grumpsObj):
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