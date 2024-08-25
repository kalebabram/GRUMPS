from grumps.__about__ import __author__, __version__
from grumps.core.grumpsObj import grumpsObj
from grumps.modes.modes import regularMode, targetMode, sigmaMode, smallMode, cliqueMode, summaryMode, targetMode, removerMode
from grumps.api.pipeLine import pipeLine

__all__ = [
	# objects
	"__author__",
	"__version__",
	"grumpsObj",
	"regularMode",
	"targetMode",
	"summaryMode",
	"smallMode",
	"sigmaMode",
	"removerMode",
	"cliqueMode",
	"pipeLine",
]
