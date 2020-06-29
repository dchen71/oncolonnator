#!/usr/bin/env python3

# Module imports
import vcf
import pandas as pd
import argparse
import requests
import json
import os

# Function to do basic vcf manipulations
## https://pyvcf.readthedocs.io/en/latest/INTRO.html
## https://samtools.github.io/hts-specs/VCFv4.2.pdf

## goal 1 - move vcf file into pandas data frame
## goal 2 - parse out all releveant columns as list or dict for pandas
## goal 3 - get exac database api going and annotate relevant things for each entry
### /rest/variant/{chrome}-{pos}-{ref}-{var}
#### variant.allele_freq
#### consequence - get the list of this
##### get list and then manualy order by most deleterious and return that else None
#### variant.genes
#### variant.transcripts
## goal 4 - build pandas dataframe output
### chrom pos ref alt dp freq conseq gene transcript
## goal 5 - make output
## goal 6 - do some unit testing
## goal 7 - update documentation
## goal 8 - docker

def annotate_vcfs(input_vcf = None, output_file = 'output/parsed.csv'):
    """
    Parses and annotates a given vcf file using the ExAC variant database

    Keyword arguments: 
    input_vcf -- The path to the VCF file to annotate (default None)
    output_file -- The directory and file name to output a csv to (default output/parsed.csv)
    """
    # Read input or error out
    try:
      vcf_reader = vcf.Reader(open(input_vcf, 'r'))
    except:
      print("Error: Could not open input file")


    for record in vcf_reader:
      print(record)

    record.CHROM # chrom
    record.POS # Position
    record.REF # ref
    record.ALT #alt allele
    record.get_hets()[0].data.DP # Need to check if there are entries here otherwise make it NA in case

# GET request API calls to ExAC
## https://www.geeksforgeeks.org/get-post-requests-using-python/

if __name__ == "__main__":
    annotate_vcfs(input_vcf = "input/example.vcf", output_file = "output/parsed.csv")