# GRUMPS
[![Anaconda-Server Badge](https://anaconda.org/kabram/grumps/badges/version.svg)](https://anaconda.org/kabram/grumps)[![Anaconda-Server Badge](https://anaconda.org/kabram/grumps/badges/latest_release_date.svg)](https://anaconda.org/kabram/grumps)

***G***enomic distance based ***R***apid ***U***ncovering of ***M***icrobial ***P***opulation ***S***tructures.

`grumps` is designed to assist and speed up the construction of species level population structures using Mash distances as an input. ANI values can be used as well if the ANI values are converted to a decimal difference value {i.e. (100 - ANIvalue) /100}. Additional helper scripts are provided if you do not have a correctly formatted distance matrix to input.

`grumps` reads a normalized distance matrix containing NxN pairwise genome comparisons and returns a filtered result. 

It can be run in `summary`, `regular`, `strict`, `sigma`, `target`,
`clique`, and `small` modes. 

For more information about these modes please see the white paper:
https://doi.org/10.1101/2022.12.19.521123

## Installation

`grumps` is installable from conda, pip or from source. 

The best installation method for `grumps` is conda within a new environment. Currently `grumps` and `r-grumps` are only available on conda for Linux and MacOSX.

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
All neccessary files needed to build the python package of `grumps` are found in `src/grumps` within this repository.

All neccessary files needed to build the R package of `grumps` are found in the `r-grumps` repository: https://github.com/kalebabram/r-grumps.git

In order to get the CLI entrypoint for the R package, simply download the Rscript `cligrumps.R` to your computer. You can rename the Rscript to `r-grumps`, relocate it to a directory in your `$PATH`, and make it executable for equivalent behavior to the conda install of `r-grumps`. 

## Dependencies
`grumps` utilizes the following python libraries:
* python 
* pandas
* networkx
* seaborn
* scipy
* scikit-learn

`r-grumps` utilizes the following R libraries:
* MASS
* optparse
* grDevices
* RColorBrewer
* stats
* utils

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

### R
`r-grumps` also has an R library available. 

An example RScript using `r-grumps` is given below:
```R
library(rgrumps)
# change filepath to path of the distance matrix
# change mode to one of the following: 'heatmap', 'dendrogram', or 'general'
grumps <- grumpsFunc(filepath='', mode = '', cutoff = 1.25E-02, clusteringmethod = 'ward.D2', tree = 'yes')
grumps = dataframeFunc(grumps)
grumps = clusterFunc(grumps)
if (grumps$mode == 'heatmap'){
  grumps= mclFunc(grumps)
  heatmapFunc(grumps)
  labeloutFunc(grumps)
  dendrogramFunc(grumps)
  if (grumps$tree == 'yes'){
    treeFunc(grumps)
  }
}

if (grumps$mode == 'dendrogram'){
  grumps = mclFunc(grumps)
  labeloutFunc(grumps)
  dendrogramFunc(grumps)
  if (grumps$tree == 'yes'){
    treeFunc(grumps)
  }
}

if (grumps$mode == 'general'){
  heatmapFunc(grumps)
  grumps = heightCutter(grumps)
  dendrogramFunc(grumps)
  if (grumps$tree == 'yes'){
    treeFunc(grumps)
  }  
}
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
### `r-grumps`
The following section provides an overview of the command line component of `r-grumps`. Please use the help page, `r-grumps -h`, to see all command line options and what modes these options can be used with. 

**Note:** all modes print the height used to cut the clustered dendrogram and produce clusters (this information is also found in the filenames output by `r-grumps`). 

* **Produce help page.** Quickly check the software usage and available command line options.
```sh
r-grumps -h
```

* **Produce a clustered heatmap of input dataset.** Produces publication quality clustered heatmap of the supplied dataset and outputs the clustering results in the following 3 files: a colored dendrogram of the clustering results as a .png, a csv file (genomeID and clusterID as columns), and a .nwk file contaning a newick tree of the dendrogram used to create the clustered heatmap.
```sh
r-grumps -m heatmap -f [filepath_to_dataset]
```

* **Produce dendrogram of clustering results.** Performs clustering without creating a clustered heatmap. Outputs the clustering results in the following 3 files: a colored dendrogram of the clustering results as a .png, a csv file (genomeID and clusterID as columns), and a .nwk file contaning a newick tree of the dendrogram used to create the clustered heatmap.
```sh
r-grumps -m dendrogram -f [filepath_to_dataset] 
```
* **Create clusters at a different cutoff.** `r-grumps` by default uses the max height of the dendrogram multiplied by 1.25E-02 to cut the clustered dendrogram and produce clusters (for E. coli, this height roughly corresponds to subgroups at the phylogroup/phylotype level). The value supplied to `-c`/`--cutoff` will be what the max height of the clustered dendrogram will be multiplied to obtain clusters (i.e. `-c 1` would cut the tree at the root creating a single cluster)
```sh
r-grumps -m heatmap -c 1.25E-01 -f [filepath_to_dataset]
```

* **Create clusters at a set cutoff.** `r-grumps` by default uses the max height of the dendrogram multiplied by 1.25E-02 to produce clusters (for E. coli, this height roughly corresponds to subgroups at the phylogroup/phylotype level). The value supplied to `-c`/`--cutoff` will be what the height of the clustered dendrogram will be cut to obtain clusters. Note: this height is dataset dependent and should not be applied in a "one size fits all" fashion.
```sh
r-grumps -m general -f [filepath_to_dataset]
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

## Example 
In the data folder of this repository is a Mash distance matrix containing 776 ***Staphylococcus epidermidis*** genomes which will be used in the following example `grumps` analysis. 

### Step 1: Run `grumps` in `summary` mode to obtain an overview of the dataset
```sh
grumps -m summary ./data/Staphylococcus_epidermidis.tab_distmat.csv
```

In addition to a set of three files summarizing the distribution of values for each genome, the overall dataset, and the means of the dataset, a histogram of all the values in the dataset is also produced by this mode. 
![histogram](https://github.com/kalebabram/GRUMPS/blob/main/data/Staphylococcus_epidermidis.tab_distmat_summary_histogram.png)
Looking at the above histogram, there is a noticeable set of comparisons present above 0.2 (which is well above the Mash distance species boundary of 0.05) and is a clear indicator that this uncleaned dataset contains several outlier genomes. 

To address this issue, we will run `grumps` in `regular` mode with a cutoff of 0.05, the optional `sigma` filtering step applied, and we will allow `grumps` to create a clustered heatmap to visualize our cleaned dataset. 

### Step 2: Run `grumps` in `regular` mode using a cutoff of 0.05 with the optional `sigma` filtering step and output the clustered heatmap as a .png file
```sh
grumps -m regular -c 0.05 -s yes -p yes -f png -o ward ./data/Staphylococcus_epidermidis.tab_distmat.csv
```
**Note:** The above step is the equivalent of running `grumps -m regular ./data/Staphylococcus_epidermidis.tab_distmat.csv` as the command line options used in **Step 2** are the same as the default values for these options. 

The population structure of ***Staphylococcus epidermidis*** can then be observed in the clustered heatmap output by the command in **Step 2**.
![clustered_heatmap](https://github.com/kalebabram/GRUMPS/blob/main/data/Staphylococcus_epidermidis.tab_distmat_cleaned_regular_sigma_0.05_ward_heatmap.png)
As the maximum value contained in the clustered heatmap is below 0.05 and the population structure is clearly visible in the clustered heatmap, we can consider this dataset cleaned. We will now run **GRUMPS** in 'summary' mode again to obtain an updated summary of the now cleaned ***Staphylococcus epidermidis*** dataset. 

### Step 3: Run `grumps` in `summary` mode to obtain an overview of the cleaned dataset
```sh
grumps -m summary ./data/Staphylococcus_epidermidis.tab_distmat_cleaned_regular_sigma_0.05_ward_distmat.csv
```
In addition to a set of three files summarizing the distribution of values for each genome, the overall dataset, and the means of the dataset, a histogram of all the values in the dataset is also produced by this mode. 
![histogram_clean](https://github.com/kalebabram/GRUMPS/blob/main/data/Staphylococcus_epidermidis.tab_distmat_cleaned_regular_sigma_0.05_ward_distmat_summary_histogram.png)
Viewing the histogram for the cleaned dataset, we can see that there are no more comparisons above the species boundary of 0.05 as well as a similar topology to the histogram produced in **Step 1**.

Now that we have our final cleaned dataset and the summary statistics, we can use the Rscript `r-grumps` to produce the final heatmap for publication.

### Step 4: Run `r-grumps` to obtain the final clustered heatmap and grouping information
```sh
r-grumps -f ./data/Staphylococcus_epidermidis.tab_distmat_cleaned_regular_sigma_0.05_ward_distmat.csv -m heatmap -c 0.0125 -g ward.D2 
```
**Note:** The above step is the equivalent of running `r-grumps -f ./data/Staphylococcus_epidermidis.tab_distmat_cleaned_regular_sigma_0.05_ward_distmat.csv` as the command line options used in **Step 4** are the same as the default values for these options.

![r_clustered_heatmap](https://github.com/kalebabram/GRUMPS/blob/main/data/Staphylococcus_epidermidis.tab_distmat_cleaned_regular_sigma_0.05_ward_r_ward.D2_heatmap.png)
We can now take the clustered heatmap from **Step 2** and **Step 4** and open them with GIMP to create the final figure.

### Step 5: Post-processing using GIMP
To assist users in quickly creating publication ready figures from the output of **GRUMPS**, we recommend the following steps to create the final images which can be used either as a standalone figure or as panels within a figure.
* Open GIMP
* Open the Create a New Image dialogue box (File > New)
* Set width and height to 36 cm
* Click Advanced Options
* Set X and Y resolution to 600 pixels/in
* Change Fill with: to White and click OK
* Open the R heatmap as a new layer (File > Open as Layers)
* Crop this layer to content (Layer > Crop to Content)
* Move the R heatmap layer so that the bottom right corner is in the bottom right corner with no visible white pixels
* Open the Python heatmap as a new layer (File > Open as Layers)
* Use the Rectangle Selection Tool (default shortcut key: R) to draw a rectangular selection around the color scale of the Python heatmap
* Crop the Python heatmap layer to the selection (Layer > Crop to Selection)
* Crop the Python heatmap layer to content (Layer > Crop to Content)
* Scale the Python heatmap layer to either 756 pixels wide or 1564 pixels high without Interpolation (Layer > Scale Layer > Interpolation: None)
* If using the image as a panel, create a textbox (default shortcut key: T) containing the panel letter with bold Sans-Serif font size 300 and move the textbox so the upper left corner of the textbox is in the upper left corner of the image
* Move the color scale bar found in the Python heatmap layer to the upper left corner of the image (positioning is personal preference. If you are making a multi-panel figure, we recommend moving the color scale layer so the upper right hand corner of the color scale is touching the bottom left corner of the textbox)
* Save the xcf file before further modification so you have the original multilayer unscaled file if you need to make additional modifications without having to recreate the file

The resultant 36cm by 36cm 600 pixels/in figure can then be scaled to the appropriate size depending on the use.
* If the figure is standalone, scale the image to 18cm by 18cm without interpolation (Image > Scale Image > Interpolation: None)
* If the figure is going to be a quarter panel, scale the image to 9cm by 9cm without interpolation (Image > Scale Image > Interpolation: None) 
* If the figure is going to be a quarter panel with other **GRUMPS** generated heatmaps (as done in the **GRUMPS** whitepaper), we recommend scaling the image to 8.75cm by 8.75cm to ensure panels don't look cramped
