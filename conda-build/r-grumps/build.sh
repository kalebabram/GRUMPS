#!/bin/bash

# 'Autobrew' is being used by more and more packages these days
# to grab static libraries from Homebrew bottles. These bottles
# are fetched via Homebrew's --force-bottle option which grabs
# a bottle for the build machine which may not be macOS 10.9.
# Also, we want to use conda packages (and shared libraries) for
# these 'system' dependencies. See:
# https://github.com/jeroen/autobrew/issues/3
export DISABLE_AUTOBREW=1
R -e 'devtools::install_github("kalebabram/r-grumps")' 
mkdir -p ${PREFIX}/bin
wget https://raw.githubusercontent.com/kalebabram/r-grumps/main/cligrumps.R -O ${PREFIX}/bin/r-grumps
chmod +x ${PREFIX}/bin/r-grumps
