[![codecov](https://codecov.io/gh/dchen71/oncolonnator/branch/master/graph/badge.svg)](https://codecov.io/gh/dchen71/oncolonnator)

# Oncocolonnator

## Introduction

Oncolonnator is a variant annotation tool which annotates vcf files using the Broad Institute ExAC database to return variant information for all snps in a given file. This will take a given input vcf file and output a csv file containing basic vcf information and metadata from ExAC to be able to learn more about the variations in your dataset. Using this dataset, you should be able to get a better understanding about how the snps in a given sample or dataset can contribute to downstream problems and how frequently it can occur.  

## System Requirements

### Python

The python module dependencies are managed using `pipenv`. `pipenv` will manage all of the virtual environment and package depedencies needed to run this. Installation details can be found here:  

[Pipenv & Virtual Environments](https://pipenv-fork.readthedocs.io/en/latest/install.html)  

Although `pipenv` is not necessary, it is useful for automatically managing dependencies of package versions and python version. This was built using a specific version of python and package dependencies and may not necessarily work for you. Please inspect `Pipfile` and `Pipfile.lock` if you would like more information about the package versions that this was built on if you rather bring your own version of python or vitual environment.  

### Docker

Alternatively, you can build the dockerfile to run the script. Instructions for how to install docker for ubuntu 18.04 can be found here:  

[Install Docker on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)  

You can then build the container with the following command:  

    docker build . -t oncolonnator

### OS

This was built on Ubuntu 18.04 and Windows 10. Windows may run into a Python SSL error and the following link will help:  

[Windows: Python SSL certificate verify failed](https://stackoverflow.com/questions/52870795/windows-python-ssl-certificate-verify-failed)  

## How to run

### Basic Parameters  

`-h`: This is the help page and gives a description of these scripts  
`--input`: This is the parameter to pass which path is VCF file to parse  
`--output`: This is the parameter to pass the name and path of the csv file to output  

### Input

This is the typical vcf format used in genomic studies. More information about that this looks like can be found here:

[Variant Call Format](https://en.wikipedia.org/wiki/Variant_Call_Format)

### Output

This will output a csv file with the following columns:  

`CHROMOSOME`: The chromosome that this SNP is located on. This can be numeric or string.  
`POSITION`: This is where in the genome that this SNP is located. This is in base pairs(bp).  
`REF_ALLELE`: This is the reference allele.  
`ALT_ALLELE`: This is the alternate allele.  
`TOTAL_DEPTH`: This is the total number of reads supporting the SNP seen.  
`ALT_DEPTH`: This is the total number of reads supporting the alternative allele.  
`ALT_PERCENTAGE`: This is the percentage of alternate allele depth divided by the total depth.  
`ALLELE_FREQUENCY`: This is the allele frequency given by ExAC based on their own calculations.  
`WORST_CONSEQUENCE`: This is the worst consequence given for a specific alternate allele at a given position. This is preferentially give deleterious consequences followed by nonsynonomous and synonymous consequences.  
`GENES`: This is the list of genes that this SNP is located on.  
`TRANSCRIPTS`: This is the list of potential transcripts that this SNP may be a part of.  

### Pipenv / Python  

Pipenv builds an virtual environment based in the `Pipfile` and `Pipfile.lock` in the directory. You can run the script using pipenv or manually using your own virtual environment or python distribution. A example for running it via pipenv is shown below:  

    pipenv run python oncolonnator.py --input <INPUT_VCF> --output <OUTPUT_CSV>

`INPUT_VCF`: Path to the VCF file to parse  
`OUTPUT_CSV`: Path and file name for the output csv  

#### Pytest Test Suite  

    pipenv run python -m tests

This will run through the unit tests to ensure that the functions behave as expected.  

### Docker

#### Basic Run

    docker run --rm -v <INPUT_DIRECTORY>:input -v <OUTPUT_DIRECTORY>:output dchen71/oncolonnator:latest --input /input/<EXAMPLE_VCF_FILE> --output /output/<EXAMPLE_CSV_OUTPUT>

`INPUT_DIRECTORY`: Absolute directory of where the data you want to parse resides. This will map it to the `/input` folder in the docker container.  
`OUTPUT_DIRECTORY`: Absolute directory of where you want to output the data. This will map it to the `/output` folder in the docker container.  
`EXAMPLE_VCF_FILE`: The name of the VCF file you want to parse.  
`EXAMPLE_CSV_OUTPUT`: The name of the CSV file you want to output.  

## References  
[Variant Call Format](https://en.wikipedia.org/wiki/Variant_Call_Format)  
[ExAC Rest API](https://pic-sure.org/products/exac-restful-api)  
[Docker](https://www.docker.com/)  
[Pipenv](https://pipenv.pypa.io/en/latest/)  
[PyVCF](https://pyvcf.readthedocs.io/en/latest/)  