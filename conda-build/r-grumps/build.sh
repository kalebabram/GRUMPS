#!/bin/bash

export DISABLE_AUTOBREW=1

${R} CMD INSTALL --build . ${R_ARGS}

#{{ R }} -e 'devtools::install_github("kalebabram/r-grumps")' 
mkdir -p ${PREFIX}/bin
#wget https://raw.githubusercontent.com/kalebabram/r-grumps/main/cligrumps.R -O ${PREFIX}/bin/r-grumps
mv ${RECIPE_DIR}/cligrumps.R ${PREFIX}/bin/r-grumps
chmod +x ${PREFIX}/bin/r-grumps
