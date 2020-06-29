#!/usr/bin/env python3

# Module imports
import vcf
import pandas as pd
import argparse
import requests
import json
import os


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

def get_variant_annotation(chromosome = 14, position = 21853913, ref = 'T', alt = 'C'):
    """
    Get variant annotation from ExAC for a given chromosome/position/ref/alt

    Keyword arguments:
    chromosome(int, string) - Chromosome of variation
    position(int) -- Position of variation(bp)
    ref(string) -- Reference allele ()
    alt(string or list of strings) -- Alternative alleles

    Return:

    """
    base_url = "http://exac.hms.harvard.edu/rest/variant/" # Base variant ExAC API

    # sending get request and saving the response as response object 
    r = requests.get(url = base_url + "-".join([str(chromosome), str(position), ref, alt])) 
      
    # extracting data in json format 
    data = r.json() 

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

    # Pull CHROM, POS, REF, ALT, DP if available from input
    vcf_metrics = [[record.CHROM, record.POS, record.REF, record.ALT, 
        sum([sum([i.data.DP for i in record.get_hom_refs()]), 
            sum([i.data.DP for i in record.get_hom_alts()]), 
            sum([i.data.DP for i in record.get_hets()])])] 
        for record in vcf_reader]

    # Convert to dataframe
    vcf_df = pd.DataFrame(vcf_metrics, columns = ['CHROM', "POS", "REF","ALT","DP"])




# GET request API calls to ExAC
## https://www.geeksforgeeks.org/get-post-requests-using-python/

if __name__ == "__main__":
    annotate_vcfs(input_vcf = "input/example.vcf", output_file = "output/parsed.csv")