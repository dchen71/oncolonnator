# Oncocolonnator

## Introduction

Oncolonnator is a variant annotation tool which annotates vcf files using the Broad Institute ExAC database to return variant information for all snps. This will take a given input vcf file and output a csv file containing basic vcf information and metadata from ExAC to be able to learn more about the variations in your dataset.



## Requirements

The python module dependencies are managed using `pipenv`. `pipenv` will manage all of the virtual environment and package depedencies needed to run this. Installation details can be found here:  

[Pipenv & Virtual Environments](https://pipenv-fork.readthedocs.io/en/latest/install.html)  

Alternatively, you can build the dockerfile to run the script.

[Install Docker on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04) 

## How to run

### Pipenv / Python

### Docker

#### Basic Run

    docker run -v <INPUT_DIRECTORY>:input -v <OUTPUT_DIRECTORY>:output dchen71/oncolonnator:latest --input /input/<EXAMPLE_VCF_FILE> --output /output/<EXAMPLE_CSV_OUTPUT>

`INPUT_DIRECTORY`: Absolute directory of where the data you want to parse resides. This will map it to the `/input` folder in the docker container.  
`OUTPUT_DIRECTORY`: Absolute directory of where you want to output the data. This will map it to the `/output` folder in the docker container.  
`EXAMPLE_VCF_FILE`: The name of the VCF file you want to parse.  
`EXAMPLE_CSV_OUTPUT`: The name of the CSV file you want to output.  

## References  
(Variant Call Format)[https://en.wikipedia.org/wiki/Variant_Call_Format]  
(ExAC Rest API)[https://pic-sure.org/products/exac-restful-api]  