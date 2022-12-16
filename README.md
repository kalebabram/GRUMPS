# GRUMPS
***G***enomic distance based ***R***apid ***U***ncovering of ***M***icrobial ***P***opulation ***S***tructures.

**GRUMPS** is designed to assist and speed up the construction of species level population structures using Mash distances as an input. ANI values can be used as well if the ANI values are converted to a decimal difference value {i.e. (100 - ANIvalue) /100}. Additional helper scripts are provided if you do not have a correctly formatted distance matrix to input.

**GRUMPS** reads a normalized distance matrix and returns a filtered result. It can be run in 'summary', 'regular', 'strict', 'sigma', 'target',
'clique', and 'small' modes. For more information about these modes please see the white paper:
doi:1-.--.----



## Installation

Currently **GRUMPS** is only available from this repository. However, we are in the process of creating a conda package and these instructions will be updated once that is available. 

The easiest installation method using conda to create an environment is described below. However, **GRUMPS** can be deployed in a different manner if all dependencies are met.
* Clone this repo and change directories to the local clone 
* Create a conda environment using environment.yml: `conda env create -f ./environment.yml`
* Move the contents of ./scripts to the bin folder of the newly created environment: `mv ./scripts/* ~/.conda/envs/grumps/bin` 
* Test your install by activating the newly created environment and calling **GRUMPS** in help mode: `conda activate grumps; grumps -h`
* Optional: remove the repository clone directory 

Note: if your conda environments are stored in a different place than ~/.conda/envs, then you will need to modify the mv command above to where conda envs are located.

### Dependencies
**GRUMPS** utilizes the following python libraries and versions:
* python 3.7.1
* pandas 1.2.4
* networkx 2.3
* seaborn 0.11.1
* scipy 1.6.2

The optional Rscript `r_grumps` utilizes the following R libraries and versions:
* r-essentials 3.6.0
* r-sparcl 1.0.4
* r-optparse 1.6.2

Note: Some of these packages are not using the latest available version. As a part of creating the conda package for **GRUMPS**, we are working on updating the dependency versions to ensure **GRUMPS** retains all of its current features. 

## Usage Summary

The following section provides a set of minimal command line commands to use **GRUMPS**. Please use the help page, `grumps -h`, to see all command line options and what modes these options can be used with.  

* **Produce help page.** Quickly check the software usage and available command line options.
```sh
$ grumps -h
```

* **Produce summary of input dataset.** Quickly obtain multiple statistical summaries as well as a histogram for the input dataset
```sh
$ grumps -m summary [filepath_to_dataset]
```

* **Clean input dataset using 'regular' cleaning mode.** Clean the input dataset using K-means clustering. 
```sh
$ grumps -m regular [filepath_to_dataset] 
```

* **Clean input dataset using 'strict' cleaning mode.** Clean the input dataset using K-means clustering followed by a three-sigma rule based cleaning step using the means of each genome.
```sh
$ grumps -m strict [filepath_to_dataset]
```

* **Clean input dataset using 'clique' cleaning mode.** Clean the input dataset with a graph-based clustering approach. Useful for dividing datasets containing multiple species into a collection of uncleaned species level datasets.
```sh
$ grumps -m clique [filepath_to_dataset]
```

* **Clean input dataset using 'sigma' cleaning mode.** Clean the input dataset using a three-sigma rule based cleaning step applied to the extreme left and right tails of value distribution for each genome. Note: this step is automatically performed in 'regular' and 'strict' cleaning modes if `-s no` not specified.
```sh
$ grumps -m sigma [filepath_to_dataset]
```

* **Clean input dataset using 'target' cleaning mode.** Clean the input dataset using a set of target genomes. Any genome that has a value greater than the cutoff (default 0.05) to any of the provided target genomes are removed.
```sh
$ grumps -m target -t [filepath_to_file_with_target_ids] [filepath_to_dataset]
```

* **Clean input dataset using 'remover' cleaning mode.** Remove a set of genomes from the input dataset by ID. 
```sh
$ grumps -m remover -r [filepath_to_file_with_ids_to_remove] [filepath_to_dataset]
```

## Example 
![Screenshot](data/Figure_3.tif)
