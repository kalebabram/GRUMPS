from pandas import read_csv
class grumpsObj(object):
	"""
	This object is designed to assist and speed up the construction of 
	species level population structures using mash distances as an input.
	ANI values can be used as well if the ANI is converted to a decimal 
	difference value {i.e. (100 - ANI)/100 }
	"""

	def __init__(self, mashFile):
		# set fp within the object and try to read it.
		# If wrong filepath, error will be raised
		self.mashFile = mashFile
		try:
			self.distMat = read_csv(self.mashFile, index_col = 0)
		except FileNotFoundError as e:
			print("The name file or folder is incorrect.\
				  An error has occurred.")
			raise FileNotFoundError("The file name or filepath is incorrect. \
Please double check the filepath or file name.") from e
			
		# initialize object variables in object at object creation	
		self.mode = 'regular'
		self.cutOff = 0.05
		self.clusterMethod = 'ward'
		self.makeHeatmap = 'yes'
		self.figFormat = 'png'
		self.targetFilePath = ''
		self.removeFilePath = ''		
		self.sigma = 'yes'
		self.medoid = 'yes'
		self.settingString = ''
		self.initialGCA = list(self.distMat.index)
		self.outlierDF = ''
		self.outliercountDF = ''
		self.cleanGCA = []
		self.removedGCA = []
		self.medoidID = ''
		self.targetList = []
		self.outlierDict = dict()
		self.unconnectedNodes = []
		self.untrimmedGraph = ''
		self.trimmedGraph = dict()
		self.rerunDict = dict()
		self.untrimmedNodes = []
		self.removeList = []
		self.targetCols = []
		self.graphID = 1
		self.refIndex = []
		self.subGraphs = ''