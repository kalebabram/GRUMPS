from grumps.core.summary import statBuilder, statSummary, distroCheck
def summaryMode(grumpsObj):
	distroCheck(grumpsObj)
	statBuilder(grumpsObj)
	statSummary(grumpsObj)