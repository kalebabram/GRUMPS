from grumps.__about__ import __version__
from grumps.__about__ import __author__
from grumps.__about__ import __date__
class outputConverter(object):
	"""
	This object is designed to assist and speed up the construction of 
	symetrical distance matrices from the output of Mash or FastANI.
	"""

	def __init__(self, inFile):
		# set fp within the object and try to read it.
		# If wrong filepath, error will be raised
		self.inFile = inFile
		try:
			f = open(self.inFile)
			f.close()
		except FileNotFoundError as e:
			print("The name file or folder is incorrect.\
				  An error has occurred.")
			raise FileNotFoundError("The file name or filepath is incorrect. \
Please double check the filepath or file name.") from e

		# store empty versions of final data in object at object creation	
		self.delimiter = '\t'
		self.trimOpt = 'yes'
		self.convertANI = 'no'
		self.invertANI = 'no'
		self.header = []
		self.refPos = ''
	
	# function to determine which position is reference
	def refFinder(self,):
		pos_0 = []
		pos_1 = []
		i=1
		with open(self.inFile, 'r') as fp:
			for line in fp:
				while i < 3:
					split = line.split('\n')[0].split(self.delimiter)
					pos_0.append(split[0])
					pos_1.append(split[1])
					i+=1
		if pos_0[0] == pos_0[1]:
			self.refPos = 'pos_0'
		if pos_1[0] == pos_1[1]:
			self.refPos = 'pos_1'

	# function to create the header
	def headerBuilder(self,):
		i=1
		currentRef = ''
		previousRef = ''
		with open(self.inFile, 'r') as fp:
			for line in fp:
				split = line.split('\n')[0].split(self.delimiter)
				if self.refPos == 'pos_0':
					if i == 1:
						currentRef = split[0]
						self.header.append(split[1])
						i+=1
					else:
						previousRef = currentRef
						currentRef = split[0]
						if currentRef != previousRef:
							break
						else:
							self.header.append(split[1])
				if self.refPos == 'pos_1':
					if i ==1:
						currentRef = split[1]
						self.header.append(split[0])
						i+=1
					else:
						previousRef = currentRef
						currentRef = split[1]
						if currentRef != previousRef:
							break
						else:
							self.header.append(split[0])
		if self.trimOpt == 'yes':
			self.header = [x.rsplit('/')[-1] for x in self.header]

	# function to create the output
	def outputMaker(self,):
		currentRef = ''
		previousRef = ''
		loopDist = []
		loopID = []
		fileLines = ''
		i=1
		try:
			outFP = self.inFile.rsplit('.',1)[0] + '_distmat.csv'
		except:
			outFP = self.inFile+ '_distmat.csv'
		outFile = open(outFP, 'w')
		outFile.write(','.join(self.header) + '\n')
		with open(self.inFile, 'r') as fp:
			for line in fp:
				split = line.split('\n')[0].split(self.delimiter)
				if self.refPos == 'pos_0':
					if i == 1:
						currentRef = split[0]
						if self.trimOpt == 'yes':
							loopID.append(split[0].rsplit('/')[-1])
						else:
							loopID.append(split[0])
						loopDist.append(split[2])
						i+=1
					else:
						previousRef = currentRef
						currentRef = split[0]
						if currentRef != previousRef:
							if self.convertANI == 'yes':
								fileLines = ','.join(loopID + [str(round((1-float(x))/100,6)) for x in loopDist])
							if self.invertANI == 'yes':
								fileLines = ','.join(loopID + [str(round(100-float(x),6)) for x in loopDist])
							else:
								fileLines = ','.join(loopID + loopDist)
							outFile.write(fileLines + '\n')
							loopDist = []
							loopID = []
							fileLines = ''
							if self.trimOpt == 'yes':
								loopID.append(split[0].rsplit('/')[-1])
							else:
								loopID.append(split[0])
							loopDist.append(split[2])
						else:
							loopDist.append(split[2])
				if self.refPos == 'pos_1':
					if i == 1:
						currentRef = split[1]
						if self.trimOpt == 'yes':
							loopID.append(split[1].rsplit('/')[-1])
						else:
							loopID.append(split[1])
						loopDist.append(split[2])
						i+=1
					else:
						previousRef = currentRef
						currentRef = split[1]
						if currentRef != previousRef:
							if self.convertANI == 'yes':
								fileLines = ','.join(loopID + [str(round((1-float(x))/100,6)) for x in loopDist])
							if self.invertANI == 'yes':
								fileLines = ','.join(loopID + [str(round(100-float(x),6)) for x in loopDist])
							else:
								fileLines = ','.join(loopID + loopDist)
							outFile.write(fileLines + '\n')
							fileLines = ''
							loopDist = []
							loopID = []
							if self.trimOpt == 'yes':
								loopID.append(split[1].rsplit('/')[-1])
							else:
								loopID.append(split[1])
							loopDist.append(split[2])
						else:
							loopDist.append(split[2])
			if self.convertANI == 'yes':
				fileLines = ','.join(loopID + [str(round((1-float(x))/100,6)) for x in loopDist])
			if self.invertANI == 'yes':
				fileLines = ','.join(loopID + [str(round(100-float(x),6)) for x in loopDist])
			else:
				fileLines = ','.join(loopID + loopDist)
			outFile.write(fileLines)
			outFile.close()
			
def distmatConverter(filePath, delimiter = '\t', trimOpt = 'yes', convertANI = 'no', invertANI = 'no'):
	convertedDistmat = outputConverter(filePath)
	convertedDistmat.delimiter = delimiter
	convertedDistmat.trimOpt = trimOpt
	convertedDistmat.convertANI = convertANI
	convertedDistmat.invertANI = invertANI
	if convertANI == 'yes':
		invertANI == 'no'
	# run refFinder to find reference position
	convertedDistmat.refFinder()
	# run headerBuilder to build header
	convertedDistmat.headerBuilder()
	# write the output
	convertedDistmat.outputMaker()
	try:
		outFP = convertedDistmat.inFile.rsplit('.',1)[0] + '_distmat.csv'
	except:
		outFP = convertedDistmat.inFile+ '_distmat.csv'
	print('Converted distance matrix located at: ' + outFP)

def main():
	import argparse
	usage = """%(prog)s reads a regularly delimited file and returns a .csv \
			   distance matrix result. If using ANI values, please specify \
			   how %(prog)s should handle the ANI values with the options '-c yes' or \
			   '-i yes'. Note: '-c' or '-i' are conflicting options with \
			   '-c' having a higher priority."""

	descript = """%(prog)s is a GRUMPS helper script intended to help researchers \
			   quickly modify their data. See the white paper: doi: 10.--.--."""
			   

	parser = argparse.ArgumentParser(description=usage, epilog = descript)
	parser.add_argument("filepath", metavar="filepath",
						help="The filepath to a Mash or ANI tabular output \
						with a genome ID for each pairwise comparision in two \
						columns and the 'distance' in the thrid column\
						", type=str)
	parser.add_argument("-d", "--delimiter", dest="delimiter",
						help="If delimiter is not tab, specify. [default: '\t']\
						", type=str, default = '\t')
	parser.add_argument("-t", "--trimopt", dest = "trimOpt",
						help="Trim the row and column IDs by removing \
						anything before the last '/' character. \
						[default: 'yes']\
						", type=str, default = 'yes', choices = ['yes', 'no'])
	parser.add_argument("-c", "--convertani", dest = "convertANI",
						help="Specify if ANI values should be \
						converted into Mash distances using \
						1-(ANI/100). [default: 'no']\
						", type=str, default = 'no', choices = ['yes', 'no'])
	parser.add_argument("-i", "--invertani", dest = "invertANI",
						help="Specify if ANI values should be inverted \
						for using ANI values with GRUMPS. \
						[default: 'no']\
						", type=str, default = 'no', choices = ['yes', 'no'])
	parser.add_argument("-v", "--version", action="version", version="%(prog)s \
						v{} ({}) By: {}\
						".format(__version__, __date__, __author__))


	args = parser.parse_args()
	filepath = args.filepath
	delimiter = args.delimiter
	trimOpt = args.trimOpt
	convertANI = args.convertANI
	invertANI = args.invertANI

	if convertANI == 'yes':
		invertANI == 'no'

	convertedDistmat = outputConverter(filepath)

	if args.delimiter:
		convertedDistmat.delimiter = delimiter
	if args.trimOpt:
		convertedDistmat.trimOpt = trimOpt
	if args.convertANI:
		convertedDistmat.convertANI = convertANI
	if args.invertANI:
		convertedDistmat.invertANI = invertANI

	# run refFinder to find reference position
	convertedDistmat.refFinder()

	# run headerBuilder to build header
	convertedDistmat.headerBuilder()

	# write the output
	convertedDistmat.outputMaker()

###########
# Module test
if __name__ == "__main__":
	main()
