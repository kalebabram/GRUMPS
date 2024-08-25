from grumps.core.grumpsObj import grumpsObj
from grumps.core.argParse import argParseFunc

# trigger CLI function
args = argParseFunc()

### initialize the mash object with defaults before setting arg vars
data = grumpsObj(args.filepath)

### check for arg vars and set them within the mash object

data.mode = args.mode
data.cutOff = args.cutoff
data.clusterMethod = args.clustermethod
data.makeHeatmap = args.heatMap
data.figFormat = args.figformat
data.sigma = args.sigma
data.medoid = args.medoid
data.settingString = data.mode + '_' + \
str(data.cutOff) + '_' + data.clusterMethod

if args.targetFP:
    data.targetFilePath = args.targetFP
if args.removeFP:
    data.removeFilePath = args.removeFP



                   
    ### mode  == 'regular'
    if data.mode == 'regular' or 'strict':
        from grumps.modes.regularMode import regularMode
        regularMode(data)
    if data.mode == 'summary':
        from grumps.modes.summaryMode import summaryMode
        summaryMode(data)
    if data.mode == 'target':
        from grumps.modes.targetMode import targetMode
        targetMode(data)
    if data.mode == 'remover':
        from grumps.modes.removerMode import removerMode
        removerMode(data)
    if data.mode == 'small':
        from grumps.modes.smallMode import smallMode
        smallMode(data)
    if data.mode == 'sigma':
        from grumps.modes.sigmaMode import sigmaMode
        sigmaMode(data)
    if data.mode == 'clique':
        from grumps.modes.cliqueMode import cliqueMode
        cliqueMode(data)

if __name__ == "__main__":
    cli()





               
### mode  == 'regular'
if data.mode == 'regular' or 'strict':
    # load neccessary functions
    from grumps.modes.shared import outlierFiller, outlierCountBuilder, outlierKmeans, finalDF
    from grumps.modes.shared import cleanDFOutput, removedGCAOutput, medoidIDOutput, medoidFinder
    
    # if cutoff is set by user run that value is used otherwise 0.05
    outlierFiller(data)
    outlierCountBuilder(data)
    outlierKmeans(data)
    
    # make clean dataframe for outputting
    finalDF(data)

    if data.mode == 'strict':
        from grumps.cleaners.cleaners import meanCleaner
        # run mean cleaner
        meanCleaner(data)
        # make clean dataframe for outputting
        finalDF(data)

    if data.sigma == 'yes':
        from grumps.cleaners.cleaners import sigmaModeCleaner
    # now run sigma cleaner
        sigmaModeCleaner(data)
        data.settingString = data.mode + '_' + 'sigma_'+ \
        str(data.cutOff) + '_' + data.clusterMethod
    # make clean dataframe for outputting
        finalDF(data)
    
    # identify the medoid of the cleaned dataset
    medoidFinder(data)
    
    if data.medoid == 'yes':
        from grumps.cleaners.cleaners import medoidChecker, medoidCleaner
    # now run medoid cleaner
        medoidCleaner(data)
    # make clean dataframe for outputting
        finalDF(data)
    # identify new medoid on the off chance it has changed
        medoidFinder(data)

    # if user doesn't disable heatmap this will trigger and make the heatmap    
    if data.makeHeatmap == 'yes':
        from grumps.modes.shared import heatmapMaker
        heatmapMaker(data)

    # outputs the final clean dataframe        
    cleanDFOutput(data)
    # write out the removed genome list 
    removedGCAOutput(data)
    # write out the identified medoid
    medoidIDOutput(data)
    
### mode == 'summary'    
if data.mode == 'summary':
    from grumps.modes.summary import statBuilder, statSummary, distroCheck
    distroCheck(data)
    statBuilder(data)
    statSummary(data)

### mode == 'target'
if args.mode == 'target':
    from grumps.cleaners.cleaners import targetCleaner
    from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
# attempt to open file with target ID list 
    try:
        with open(data.targetFilePath, 'r') as infile:
            data.targetList = infile.readlines()
        # save the list in the object
        data.targetList = [x.split('\n')[0] for x in data.targetList]
        data.targetSuccess = targetCleaner(data)
        if data.targetSuccess == True:
            # clean the dataset
            finalDF(data)
        # identify the medoid of the dataset
            medoidFinder(data)
            if len(data.distMat) < len(data.initialGCA):
    # if user doesn't disable heatmap this will trigger and make the heatmap    
                if data.makeHeatmap == 'yes':
                    from grumps.modes.shared import heatmapMaker
                    heatmapMaker(data)
        # outputs the final clean dataframe
                cleanDFOutput(data)
                # write out the removed genome list 
                removedGCAOutput(data)
                # write out the identified medoid
                medoidIDOutput(data)
            if len(data.distMat) == len(data.initialGCA):
                print('The provided targets did not filter any genomes.')
                print('If this is unexpected, please double check the provided targets.')
    except FileNotFoundError as e:
        raise FileNotFoundError("The file: \"" + data.targetFilePath + '\" \
cannot be found. Please double check the file name and provide the complete \
filepath to \"-t\" when running in target mode.') from e

### mode == 'remover'
if args.mode == 'remover':
    from grumps.core.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput    
# attempt to open file with list of IDs to remove
    try:
        with open(data.removeFilePath, 'r') as infile:
            data.removeList = infile.readlines()
        data.removeList = [x.split('\n')[0] for x in data.removeList]
        try:
            # identify genomes to retain
            data.cleanGCA = list(set(list(data.distMat.index)) - set(data.removeList))
            # create the clean dataframe for the target genomes
            finalDF(data)
            # identify the medoid
            medoidFinder(data)
            # if user doesn't disable heatmap this will trigger and make the heatmap    
            if data.makeHeatmap == 'yes':
                from grumps.modes.shared import heatmapMaker
                heatmapMaker(data)
            # output the final clean dataframe
            cleanDFOutput(data)
        # write out the removed genome list 
            removedGCAOutput(data)
        # write out the medoid
            medoidIDOutput(data)
        except KeyError as e:
            raise KeyError('Please check that your genome identifiers are correct and in your datasets.') from e
    except FileNotFoundError as e:
        raise FileNotFoundError("The file: \"" + data.removeFilePath + '\" \
cannot be found. Please double check the file name and provide the complete \
filepath to \"-r\" when running in remover mode.') from e

### mode == 'small'
if args.mode == 'small':
    from grumps.modes.cleaners import smallModeCleaner
    from grumps.modes.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
# identify genomes where average (ignoring self-self) is > than cutoff
    smallModeCleaner(data)
    # make clean dataframe for outputting
    finalDF(data)
    # identify the medoid
    medoidFinder(data)
# if user doesn't disable heatmap this will trigger and make the heatmap    
    if data.makeHeatmap == 'yes':
        from grumps.modes.shared import heatmapMaker
        heatmapMaker(data)
    # outputs the final clean dataframe
    cleanDFOutput(data)
# write out the removed genome list 
    removedGCAOutput(data)
    # write out the medoids
    medoidIDOutput(data)

### mode == 'sigma'
if data.mode == 'sigma':
    from grumps.cleaners.cleaners import sigmaModeCleaner
    from grumps.modes.shared import finalDF, cleanDFOutput, removedGCAOutput, medoidFinder, medoidIDOutput
# if cutoff is set by user run that value is used otherwise 0.05
    # now run sigma cleaner
    sigmaModeCleaner(data)
    # make clean dataframe for outputting
    finalDF(data)
    # identify the medoid
    medoidFinder(data)
    # if user doesn't disable heatmap this will trigger and make the heatmap    
    if data.makeHeatmap == 'yes':
        from grumps.modes.shared import heatmapMaker
        heatmapMaker(data)
    # outputs the final clean dataframe        
    cleanDFOutput(data)
    # write out the removed genome list 
    removedGCAOutput(data)
    # write out the medoidID
    medoidIDOutput(data)

### mode == 'clique'
if data.mode == 'clique':
    from grumps.modes.clique import graphBuilder, graphDivider, cliqueWriter
    graphBuilder(data, [])
    data.trimmedGraph = graphDivider(data)
    # run medoid based cleaning
    if data.medoid == 'yes':
        from grumps.modes.clique import graphStatFunction, dictMerge, kmeansSil, outlierFiller, medoidGraphCleaner
        data.trimmedGraph, data.untrimmedNodes = medoidGraphCleaner(data, data.trimmedGraph)
        while len(data.untrimmedNodes) > 1:
            graphBuilder(data, data.untrimmedNodes)
            data.graphDict = graphDivider(data)
            data.graphDict, data.untrimmedNodes = medoidGraphCleaner(data, data.graphDict)
            dictMerge(data.trimmedGraph, data.graphDict)
            if len(data.untrimmedNodes) == 1:
                data.unconnectedNodes.extend(data.untrimmedNodes)
    # write out the cliques
    cliqueWriter(data)
    
