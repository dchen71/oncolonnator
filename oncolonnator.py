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
    

    # Type check alternate allele for looping
    if isinstance(alt, str):
        annotation = get_exac_variant(chromosome, position, ref, alt)
    elif isinstance(alt, list):
        annotation = []
        for alternate_allele in alt:
            annotation.append(get_exac_variant(chromosome, position, ref, alt))
    else:
        raise Exception("Alternative Allele not string or list") # Total failure on weird input

    return(annotation)

def get_exac_variant(chromosome = 14, position = 21853913, ref = 'T', alt = 'C'):
    base_url = "http://exac.hms.harvard.edu/rest/variant/" # Base variant ExAC API
    
    # Get request to Variant API
    r = requests.get(url = base_url + "-".join([str(chromosome), str(position), ref, alt])) 
    
    # Check for 404 failed endpoint and on failure
    if r.status_code == 404:
        return('failure') # Silent error

    # Convert response to json
    data = r.json() 

    # Get relevant information
    try:
      allele_freq = data['variant']['allele_freq']
    except:
      allele_freq = None
    variant_consequences = list(data['consequence']) if data['consequence'] is not None else None # List of ExAC consequences for variant
    try:
        genes = data['variant']['genes']
    except:
        genes = None
    try:
       transcripts = data['variant']['transcripts']
    except:
       transcripts = None

    return([allele_freq, variant_consequences, genes, transcripts])
    
    # Calculate the worst consequence



def annotate_vcfs(input_vcf = None, output_file = 'output/parsed.csv'):
    """
    Parses and annotates a given vcf file using the ExAC variant database

    Keyword arguments: 
    input_vcf(str) -- The path to the VCF file to annotate (default None)
    output_file(str) -- The directory and file name to output a csv to (default output/parsed.csv)
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
            sum([i.data.DP for i in record.get_hets()])]),
        sum([i.data.DP for i in record.get_hom_alts()])] 
        for record in vcf_reader]

    # Convert to dataframe
    vcf_df = pd.DataFrame(vcf_metrics, columns = ['CHROMOSOME', "POSITION", "REF_ALLELE","ALT_ALLELE","TOTAL_DEPTH", "ALT_DEPTH"])
    vcf_df["ALT_PERCENTAGE"] = vcf_df["ALT_DEPTH"]/vcf_df["TOTAL_DEPTH"] * 100.0 # Get percentage of alternative depth / total depth for percentage of supporrt of variant




# GET request API calls to ExAC
## https://www.geeksforgeeks.org/get-post-requests-using-python/

if __name__ == "__main__":
    annotate_vcfs(input_vcf = "input/example.vcf", output_file = "output/parsed.csv")