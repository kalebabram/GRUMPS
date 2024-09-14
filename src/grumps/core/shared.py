#import pandas as pd
from pandas import DataFrame
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

### functions shared by regular and strict modes
def outlierFiller(grumpsObj):
	from pandas import concat, DataFrame
	outlierSize = round(len(grumpsObj.distMat) * .05) + 2
	aboveCutoff = grumpsObj.cutOff * 1.02
	outlierSim = grumpsObj.cutOff/10
	outlierList = [aboveCutoff]*len(grumpsObj.distMat)
	loopList = [outlierSim] * outlierSize
	tempDF1 = DataFrame()
	indexList = list(grumpsObj.distMat.columns)
	for val in range(1,outlierSize+1):
		tempDF1['outlier_' + str(val)] = outlierList
	tempDF1.index = indexList
	tempDF1 = tempDF1.T
	grumpsObj.distMat = concat([grumpsObj.distMat,tempDF1])
	tempDF2 = pd.DataFrame()
	for val in range(0,outlierSize):
		subloopList = loopList[:]
		subloopList[val] = 0
		indexList.append('outlier_' + str(val))
		tempDF2['outlier_' + str(val+1)] = outlierList + subloopList
	tempDF2.index = indexList
	grumpsObj.distMat = concat([grumpsObj.distMat,tempDF2],axis=1)

def outlierCountBuilder(grumpsObj):
	funcDict = dict()
	for col in grumpsObj.distMat.columns:
		loopSeries = grumpsObj.distMat[col]
		loopSeries = loopSeries[loopSeries <= grumpsObj.cutOff]
		funcDict[col] = loopSeries.index.value_counts()
	funcDF = DataFrame(funcDict)
	funcDF.replace(to_replace = 1, value = 0, inplace = True)
	funcDF.fillna(value = 1, inplace = True)
	statDict = dict()
	for col in funcDF:
		funcSeries = funcDF[col]
		statDict[col] = funcSeries.value_counts()
		grumpsObj.outliercountDF = DataFrame(statDict)
		grumpsObj.outliercountDF = grumpsObj.outliercountDF.T

def sizeChecker(clustList):
	if 2 not in clustList:
		print('WARNING: Your dataset failed to partition using k-means \
clustering. Most likely this was caused by the dataset \
being too small. You should rerun GRUMPS with the mode set \
to small [grumps -m small ...]')
		return False
	else:
		return True

def outlierKmeans(grumpsObj):
	Z = linkage(grumpsObj.outliercountDF,  grumpsObj.clusterMethod)
	clusts = fcluster(Z, 2, criterion = 'maxclust')
	sizeCheck = sizeChecker(clusts)
	if sizeCheck == True:
		clust1List = list(grumpsObj.outliercountDF[clusts == 1].index)
		clust2List = list(grumpsObj.outliercountDF[clusts == 2].index)
		if 'outlier_1' in clust1List:
			grumpsObj.cleanGCA = clust2List
		else:
			grumpsObj.cleanGCA = clust1List
	if sizeCheck == False:
		clust1List = [x for x in list(grumpsObj.outliercountDF[clusts == 1].index) if 'outlier_' not in x]
		grumpsObj.cleanGCA = clust1List



### functions shared by regular, strict, target, remover, sigma, and small modes
def finalDF(grumpsObj):
	removedGCA = list(set(grumpsObj.distMat.index) - set(grumpsObj.cleanGCA))
	grumpsObj.distMat.drop(columns = removedGCA, index = removedGCA, inplace=True)
	grumpsObj.removedGCA = list(set(grumpsObj.initialGCA) - set(grumpsObj.distMat.index))
	
	
def cleanDFOutput(grumpsObj):
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_cleaned_' + grumpsObj.settingString + '_distmat.csv'
	except:
		outfp = grumpsObj.mashFile + '_cleaned_' + grumpsObj.settingString + '_distmat.csv'
	grumpsObj.distMat.to_csv(outfp)

def removedGCAOutput(grumpsObj):
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_cleaned_' + grumpsObj.settingString + '_removed_genomes'
	except:
		outfp = grumpsObj.mashFile + '_cleaned_' + grumpsObj.settingString + '_removed_genomes'
	with open(outfp, 'w') as outfile:
		outfile.writelines('\n'.join(grumpsObj.removedGCA))

def heatmapMaker(grumpsObj):
	from seaborn import clustermap
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_cleaned_' + grumpsObj.settingString + '_heatmap'
	except:
		outfp = grumpsObj.mashFile + '_cleaned_' + grumpsObj.settingString + '_heatmap'
	condensedDF = squareform(grumpsObj.distMat)
	Z = linkage(condensedDF, grumpsObj.clusterMethod)
	sns_plot = clustermap(grumpsObj.distMat, row_linkage = Z, col_linkage = Z, cmap = "BrBG_r",yticklabels=False,xticklabels=False)
	if grumpsObj.figFormat == 'png':
		sns_plot.savefig(outfp +'.png', dpi = 600, format = 'png')
	if grumpsObj.figFormat == 'svg':
		sns_plot.savefig(outfp +'.svg', dpi = 600, format = 'svg')
	if grumpsObj.figFormat == 'pdf':
		sns_plot.savefig(outfp +'.pdf', dpi = 600, format = 'pdf')

def medoidFinder(grumpsObj):
	from numpy import argmin
	grumpsObj.medoidID = grumpsObj.distMat.iloc[argmin(grumpsObj.distMat.sum(axis=0))].name
	
def medoidIDOutput(grumpsObj):
	try:
		outfp = grumpsObj.mashFile.split('.csv')[0] + '_cleaned_' + grumpsObj.settingString + '_medoid'
	except:
		outfp = grumpsObj.mashFile + '_cleaned_' + grumpsObj.settingString + '_medoid'
	with open(outfp, 'w') as outfile:
		outfile.writelines('\n'.join([grumpsObj.medoidID]))
	

