# Change Log
All notable changes to this project will be documented in this file.
 
## [Unreleased] 
 
Full integration of GitHub with PyPI and conda
### Added
 - neccessary files/configs to cause new releases of `grumps` to automatically
   build and upload to pip and conda

## [1.0.3] - 2024-09-16
#### `grumps`
To update `grumps` via conda: `conda update kabram::grumps`

To update `grumps` via pip: `pip install grumps --upgrade`
#### `py-grumps`
To update `py-grumps` via conda: `conda update kabram::py-grumps`
#### `r-grumps`
To update `r-grumps` via conda: `conda update kabram::r-grumps`

To update `r-grumps` via R: `R -e "devtools::install_github('kalebabram/r-grumps')"`
### Changed
 - mirrored outlier optimizations to `clique` mode version

## [1.0.2] - 2024-09-14

### Changed
 - tweaked outlier addition function to be more efficient
### Fixed
 - fixed `clique` mode when ran with medoid cleaning to properly account for disconnected nodes as not their own clique

## [1.0.1] - 2024-09-03

### Added
 - conda install compatability
 - pip install compatability
 - R install compatability (via devtools)
 - conda-build recipes
 - toggle for 'medoid' cleaning step: `-M [yes|no]`
 - seperate repository for `r-grumps`: https://www.github.com/kabram/r-grumps.git
 - src/ for `grumps`
 - Python and R libraries for `grumps`
 - `r-grumps` outputs the clustered dendrogram as a .nwk tree file

### Changed
 - code structure of both `grumps` and `r-grumps`
 - GitHub structure of `grumps`
 - unified the 'labels' and 'groups' files output by `r-grumps` into one file
 - versions of R and Python used in `grumps` and `r-grumps`
 - versions of dependencies used in `grumps` and `r-grumps`
 
### Fixed
 - issue with `'clique'` mode which could cause `grumps` to produce "species-level"
   datasets with multiple species if the dataset had sufficient noise
   - Usually only an issue for datasets containing species which have similarity
   values barely outside the species boundary (i.e. *Enterococcus faecium* and *Enterococcus
   lactis*) or datasets with a high raitio of low-quality genomes relative
   to the total number of genomes - i.e. a MAGs dataset
   - added 'medoid' cleaning step to `'clique'` mode: `grumps -m clique -M yes distmat.csv`
     - defaults to 'yes'
 - overall performance of `grumps` by restructering the codebase and loading only the required 
   portions of `grumps` for the specified workflow (mode, cutoff, etc.)
 
## [0.9.9] - 2022-12-20
 
### Added
 - initial version not conda or pip installable   
 - initial GitHub repository for `grumps`: https://www.github.com/kabram/grumps.git
