def pipeLine(grumpsObj,mode='regular',cutOff=0.05,clusterMethod = 'ward',makeHeatmap='yes',figFormat = 'png',sigma='yes',medoid='yes',targetFilePath=None,removeFilePath=None):
	"""
	Takes a grumpsObj and runs the GRUMPS pipeline with the specified parameters.
	"""
	grumpsObj.mode = mode
	grumpsObj.cutOff = cutOff
	grumpsObj.clusterMethod = clusterMethod
	grumpsObj.makeHeatmap = makeHeatmap
	grumpsObj.figFormat = figFormat
	grumpsObj.sigma = sigma
	grumpsObj.medoid = medoid
	if targetFilePath != None:
		grumpsObj.targetFilePath = targetFilePath
	if removeFilePath != None:
		grumpsObj.removeFilePath = removeFilePath

	if grumpsObj.mode == 'regular':
		from grumps.modes.modes import regularMode
		regularMode(grumpsObj)
	elif grumpsObj.mode == 'strict':
		from grumps.modes.modes import regularMode
		regularMode(grumpsObj)
	elif grumpsObj.mode == 'summary':
		from grumps.modes.modes import summaryMode
		summaryMode(grumpsObj)
	elif grumpsObj.mode == 'target':
		from grumps.modes.modes import targetMode
		targetMode(grumpsObj)
	elif grumpsObj.mode == 'remover':
		from grumps.modes.modes import removerMode
		removerMode(grumpsObj)
	elif grumpsObj.mode == 'small':
		from grumps.modes.modes import smallMode
		smallMode(grumpsObj)
	elif grumpsObj.mode == 'sigma':
		from grumps.modes.modes import sigmaMode
		sigmaMode(grumpsObj)
	elif grumpsObj.mode == 'clique':
		from grumps.modes.modes import cliqueMode
		cliqueMode(grumpsObj)
