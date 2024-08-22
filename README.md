# `The role of the working memory storage component in a random-like series generation`

This is a repository for the manuscript on ['The role of the working memory storage component in a random-like series generation'](https://doi.org/10.1371/journal.pone.0296731). In two studies we investigated  In the repository, you will find data sets (raw and processed) and all scripts for data processing, analysis, and plotting the charts. This work was supported by funds from the Polish National Science Centre (project no. 2019/35/N/HS6/04318).

## The structure of the repository

The repository is organized as follows:

* [data](data) - it consists of a bunch of csv files and the [raw](data/raw) folder. In the latter, there are two folders with raw data from both studies and a json file with order conditions in Study 2. The csv files are listed below.
	- `study1_random_df.csv` -- preprocessed data from random generation task in Study 1; 
	- `study1_random_cmx.csv` -- data set with computed algorithmic complexity for Study 1;
	- `study1_compare_df.csv` -- randomness judgment results from Study 1;
	- `study1_demographics.csv` -- demographic data from *Prolofic*;
	- `study2_random_df.csv` -- preprocessed data from random generation task in Study 2; 
	- `study2_random_cmx.csv` -- data set with computed algorithmic complexity for Study 2;
	- `study2_wm_df.csv` -- working memory capacity test results from Study 2;
	- `study2_demographics.csv` -- demographic data from *Prolific*.
* [codebooks](codebooks) - it consists codebooks for all data in `txt` format. However, they are aggregated by the study. It means that for example codebook for Study 1 consists of variables description for both, raw and processed data.  
* [notebooks](notebooks) -  this folder is named after `R` notebooks because we performed all the statistical analysis using the `R` programming language. It consists of two files: `study1.Rmd` and `study2.Rmd`. Running them might require installing additional packages but all of them are listed in the first chunks of the code.
* [fig](fig) - it contains all pictures used in the method section in the png format.
* [scripts](scripts) - it contains a couple of `R` and a couple of `Python` scripts. `R` scripts serve for preprocessing the raw data from both studies. They should be run as the first ones. `Python` scripts compute algorithmic complexity for the results of random generation tasks from both studies.

## Main Dependencies

To rerun the analysis it is enough to use only `R` programming language. `study1.Rmd` and `study2.Rmd` are written in plain `RMarkdown` and processed data sets are already available in the repository with no need to run any of the scripts from the [scripts](scripts) folder. Therefore, the main dependencies are as follows:

* R >= 4.2.1 ([R-project](https://www.r-project.org)), however, it should work fine also with earlier versions of R;
* R packages are specified in the scripts and will install if needed, however, it is best to update them if they are not in their latest stable versions;
* RStudio >= 2022.07.1 ([RStudio](https://rstudio.com)) but it should work fine also with earlier versions.

However, to run `study1_compute_cmx.py` and `study2_compute_cmx.py` it is necessary to use `python3`. Therefore, we advise you to also have installed:

* Anaconda distribution of python3.8 ([Anaconda](https://www.anaconda.com))
* python modules specified in `requirenments.txt`


## Setup

Regardless of whether you want to perform only analysis from `study1.Rmd` and `study2.Rmd` or you would also like to run the code from the [scripts](scripts) folder we would recommend creating `R project`. It would make your life much easier and after that, you can run [notebooks](notebooks) without further delays. If you want to also execute the code from [scripts](scripts) please do as follows:

1. Install Anaconda distribution of python3.8 ([Anaconda](https://www.anaconda.com)). It is available for computers with Mac OS, Linux, and Windows for free.
2. Create a new virtual environment called `bdm`. You should execute in the Anaconda console (or Terminal) the following command:
    ```bash
    conda create -n bdm python=3.8
    ```
    Afterward, the prompt will ask about the installation of packages to which you should agree by pressing `Y` and 'enter' ('return' on Macs) afterward. Setting the environment might take a few minutes.
3. Activate the newly created environment by typing in the Anaconda console (or Terminal):
    ```bash
    conda activate bdm
    ``` 
4. Install required modules from `requirenments.txt`. Navigate in Anaconda console (or Terminal) to the folder with `requirenments.txt` and type: 
    ```bash
    pip install -r requirenments.txt
    ```
5. From the terminal execute all scripts from the [scripts](scripts) folder:
    ```bash
    Rscript scripts/study1_preprocess_data.R
    Rscript scripts/study2_preprocess_data.R
    python scripts/study1_compute_cmx.R
    python scripts/study2_compute_cmx.R
    ```

That's it.

