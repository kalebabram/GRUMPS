from numpy import std, mean, min, max, percentile, concatenate, shape, array
from pandas import concat, Series, DataFrame, cut

### functions for summary mode
def statBuilder(grumpsObj):
	perList = [.3, 1.0, 2.5, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 90.5, 91.0, 91.5, 92.0, 92.5, 93.0, 93.5, 94.0, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 99.6, 99.7, 99.8, 99.9, 99.95, 99.96, 99.97, 99.98, 99.99, 99.995]
	dfStat = concat([concat({'mean':mean(grumpsObj.distMat,axis = 1),'std':std(grumpsObj.distMat,axis=1),'min':min(grumpsObj.distMat,axis=1),'max':max(grumpsObj.distMat,axis=1)}, axis = 1),DataFrame(percentile(grumpsObj.distMat,perList, axis=0), columns = grumpsObj.distMat.index, index = [str(x)+'%' for x in perList]).T],axis=1)
	meanStat = dfStat['mean'].describe(percentiles = [.003,.1,.25,.5,.75,.9,.997])
	print('The means of your data are described below:')
	print(meanStat.to_string())
	specificStat = Series(concatenate((array([shape(grumpsObj.distMat)[0],mean(grumpsObj.distMat.values),std(grumpsObj.distMat.values)]),percentile(grumpsObj.distMat.values,[.3,10,25,50,75,90,99.7]),max(grumpsObj.distMat.values)), axis = None),index = ['count', 'mean', 'std','0.3%', '10%', '25%', '50%', '75%', '90%', '99.7%', 'max'])
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_genome_summary_table.csv'
	except:
		outfp = grumpsObj.mashFile + '_genome_summary_table.csv'
	try:
		outfp2 = grumpsObj.mashFile.split('.csv')[0] + '_mean_summary_table.csv'
	except:
		outfp2 = grumpsObj.mashFile + '_mean_summary_table.csv'
	try:
		outfp3 = grumpsObj.mashFile.split('.csv')[0] + '_overall_summary_table.csv'
	except :
		outfp3 = grumpsObj.mashFile + '_overall_summary_table.csv'
	dfStat.to_csv(outfp)
	meanStat.to_csv(outfp2, header = False)
	specificStat.to_csv(outfp3, header = False)

def statSummary(grumpsObj):
	histUnstack =  grumpsObj.distMat.unstack()
	ax = histUnstack.hist(bins = 1000)
	fig = ax.get_figure()
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_summary_histogram'
	except:
		outfp = grumpsObj.mashFile + '_summary_histogram'
	if grumpsObj.figFormat == 'png':
		fig.savefig(outfp +'.png', dpi = 600, format = 'png')
	if grumpsObj.figFormat == 'svg':
		fig.savefig(outfp +'.svg', dpi = 600, format = 'svg')
	if grumpsObj.figFormat == 'pdf':
		fig.savefig(outfp +'.pdf', dpi = 600, format = 'pdf')

def distroCheck(grumpsObj):
	unstack = grumpsObj.distMat.unstack()
	distMean = mean(grumpsObj.distMat.values)
	if distMean > 0.05:
		print('\nThe mean of your data is above the species boundary of 0.05. \nYour dataset may contain more than one species. \nPlease run GRUMPS in clique mode before proceeding. \nIf you have already run GRUMPS in clique mode with a cutoff of 0.05, try rerunning GRUMPS in clique mode with a lower cutoff.')
	if grumpsObj.cutOff != 0.05:
		binList = [0,grumpsObj.cutOff,1]
	else:
		binList = [0,0.05,1]
	normalCheck = cut(unstack, bins=binList, include_lowest=True).value_counts(sort=False)/len(unstack)
	normalEval = normalCheck[0] >= .997
	if normalEval == False:
		print('\nLess than 99.7% of your data is contained between 0 and {cutoff}.\n'.format(cutoff=grumpsObj.cutOff))
	if normalEval == True:
		print('\n99.7% or more of your data is contained between 0 and {cutoff}.\n'.format(cutoff=grumpsObj.cutOff))



