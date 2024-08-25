from grumps.core.argParse import argParseFunc
from grumps.core.grumpsObj import grumpsObj

def cli():

	# trigger CLI function
	args = argParseFunc()

	### initialize the grumps object with defaults before setting arg vars
	data = grumpsObj(args.filepath)

	### check for arg vars and set them within the grumps object
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
	if data.mode == 'regular':
		from grumps.modes.modes import regularMode
		regularMode(data)
	elif data.mode == 'strict':
		from grumps.modes.modes import regularMode
		regularMode(data)
	elif data.mode == 'summary':
		from grumps.modes.modes import summaryMode
		summaryMode(data)
	elif data.mode == 'target':
		from grumps.modes.modes import targetMode
		targetMode(data)
	elif data.mode == 'remover':
		from grumps.modes.modes import removerMode
		removerMode(data)
	elif data.mode == 'small':
		from grumps.modes.modes import smallMode
		smallMode(data)
	elif data.mode == 'sigma':
		from grumps.modes.modes import sigmaMode
		sigmaMode(data)
	elif data.mode == 'clique':
		from grumps.modes.modes import cliqueMode
		cliqueMode(data)

if __name__ == "__main__":
	cli()
