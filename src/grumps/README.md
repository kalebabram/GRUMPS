# GRUMPS
***G***enomic distance based ***R***apid ***U***ncovering of ***M***icrobial ***P***opulation ***S***tructures.

`grumps` is designed to assist and speed up the construction of species level population structures using Mash distances as an input. ANI values can be used as well if the ANI values are converted to a decimal difference value {i.e. (100 - ANIvalue) /100}. Additional helper scripts are provided if you do not have a correctly formatted distance matrix to input.

`grumps` reads a normalized distance matrix and returns a filtered result. It can be run in `summary`, `regular`, `strict`, `sigma`, `target`,
`clique`, and `small` modes. 

For more information about these modes please see the white paper:
https://doi.org/10.1101/2022.12.19.521123

## Dependencies
`grumps` utilizes the following python libraries:
* python >=3.7
* pandas
* networkx
* seaborn
* scipy
* scikit-learn

## Installation

`grumps` is installable from conda, pip or from source. 

The best installation method for `grumps` is conda within a new environment. 

### Installing from conda
#### Creating a new environment
```sh
conda env create -n grumps_env kabram::grumps
```
**Note:** using [mamba](https://mamba.readthedocs.io/en/latest/) as a replacement for conda can spead up the environment creation process.

#### Installing into existing environment
```sh
conda install kabram::grumps
```
`grumps` has two components in the conda package: `py-grumps` and `r-grumps`. Each component is a conda package which contains all necessary dependencies for that component. 

To install the python component:
```sh
conda install kabram::py-grumps
```
To install the R component:
```sh
conda install kabram::r-grumps
```
### Installing from other sources
#### pip
```sh
pip install grumps
```
**Note:** the pip version does not have the R dependecies needed for `r-grumps`. 

#### r-devtools
```sh
R -e 'devtools::install_github("kalebabram/r_grumps")'
```
**Note:** R library `devtools` is required: `install.packages('devtools')` or `conda install r-devtools` for this approach. To get the CLI entrypoint, download `cligrumps.R` from the repository. You can rename the Rscript to `r-grumps`, relocate it to a directory in your $PATH, and make it executable for equivalent behavior to the conda install of `r-grumps`. 

#### Source
All neccessary files needed to build the python package of `grumps` are found in `src/grumps` in the `grumps` repository: https://github.com/kalebabram/grumps.git

All neccessary files needed to build the R package of `grumps` are found in the `r-grumps` repository: https://github.com/kalebabram/r-grumps.git

In order to get the CLI entrypoint for the R package, simply download the Rscript `cligrumps.R` to your computer. You can rename the Rscript to `r-grumps`, relocate it to a directory in your `$PATH`, and make it executable for equivalent behavior to the conda install of `r-grumps`. 

## `grumps` library support
### python
`grumps` also is available as a python library to allow easy integration into existing python based workflows.

While `grumps` has many components, the following overview summarizes functions which users are intended to interact with:
```sh
grumps
├── .api
│   └── .pipeLine()
├── .core
│   ├── .grumpsObj()
│   └── .distmatConverter()
└── .modes
    ├── .regularMode()
    ├── .removerMode()
    ├── .targetMode()
    ├── .smallMode()
    ├── .sigmaMode()
    ├── .summaryMode()
    └── .cliqueMode()
```
**Note:** `import grumps.api as grumps` will automatically load all the above functions which can be accessed via `grumps.<function_name>` (i.e. `grumps.grumpsObj()`)

The intended use of the python `grumps` library is as follows:
```py
import grumps.api as grumps
# if you need to convert your input file to NxN distance matrix. The location of the converted file is printed.
grumps.distmatConverter('/path/to/input/file.tab')
# load in the NxN distance matrix
data = grumps.grumpsObj('/path/to/distmat/file.csv')
# change these grumpsObj defaults or the cleaning modes/pipeline will run with defaults
data.mode = 'regular'
data.cutOff = 0.05
data.clusterMethod = 'ward'
data.makeHeatmap = 'yes'
data.figFormat = 'png'
data.targetFilePath = ''
data.removeFilePath = ''
data.sigma = 'yes'
data.medoid = 'yes'
# if you want to run grumps automatically
grumps.pipeLine(data)
# if you want to use a specific cleaning mode
data = grumps.regularMode(data)
```

## Usage Summary
### `grumps`
The following section provides a set of minimal command line commands to use `grumps`. Please use the help page, `grumps -h`, to see all command line options and what modes these options can be used with.  

* **Produce help page.** Quickly check the software usage and available command line options.
```sh
grumps -h
```

* **Produce summary of input dataset.** Quickly obtain multiple statistical summaries as well as a histogram for the input dataset
```sh
grumps -m summary [filepath_to_dataset]
```

* **Clean input dataset using `regular` cleaning mode.** Clean the input dataset using K-means clustering. 
```sh
grumps -m regular [filepath_to_dataset] 
```

* **Clean input dataset using `strict` cleaning mode.** Clean the input dataset using K-means clustering followed by a three-sigma rule based cleaning step using the means of each genome.
```sh
grumps -m strict [filepath_to_dataset]
```

* **Clean input dataset using `clique` cleaning mode.** Clean the input dataset with a graph-based clustering approach. Useful for dividing datasets containing multiple species into a collection of uncleaned species level datasets.
```sh
grumps -m clique [filepath_to_dataset]
```

* **Clean input dataset using `sigma` cleaning mode.** Clean the input dataset using a three-sigma rule based cleaning step applied to the extreme left and right tails of value distribution for each genome. **Note:** this step is automatically performed in `regular` and `strict` cleaning modes if `-s no` not specified.
```sh
grumps -m sigma [filepath_to_dataset]
```

* **Clean input dataset using `target` cleaning mode.** Clean the input dataset using a set of target genomes. Any genome that has a value greater than the cutoff (default 0.05) to any of the provided target genomes are removed.
```sh
grumps -m target -t [filepath_to_file_with_target_ids] [filepath_to_dataset]
```

* **Clean input dataset using `remover` cleaning mode.** Remove a set of genomes from the input dataset by ID. 
```sh
grumps -m remover -r [filepath_to_file_with_ids_to_remove] [filepath_to_dataset]
```

## Helper Script
`distmat_converter` reads a regularly delimited file and returns a .csv distance matrix result. By default, the output of `mash dist` can be used by `distmat_converter` to obtain a Mash distance matrix for `grumps`
```sh
distmat_converter [filepath_to_mash_output.tab]
```
If an ANI delimited file is input, please specify how `distmat_converter` should handle the ANI values with the options `-c yes` or `-i yes`. **Note:** `-c` or `-i` are conflicting options with `-c` having a higher priority. `-c yes` converts the ANI values to Mash values via (100-ANI)/1. `-i yes` simply inverts ANI values via 100-ANI. 
```sh
distmat_converter -c yes [filepath_to_fastANI_output.tab]
```
