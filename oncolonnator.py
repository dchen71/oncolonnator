#!/usr/bin/env python3

"""
oncolonnator.py
Oncolonnator does basic parsing of VCF files. This script will parse the basic information from VCF files as well as pull annotation metadata from the Harvard ExAC API servers.
This will take in a single vcf input and output a csv file with the chromosome, position, alleles, genes, transcripts, and consequence of mutation.
"""

# Module imports
import vcf
import pandas as pd
import argparse
import requests
import json
import os



def create_parser():
    """
    Arg parser to be able to pass in inputs and outputs as parameters

    Keyword arguments:
    --input - String input for the location of the VCF file
    --output - File name path to the parsed output CSV file

    Return:
    parser(ArgumentParser) - ArguemntParser object containing inputs and outputs 
    """
    parser = argparse.ArgumentParser(description = 'Annotate VCF file for ExAC Variant annotations and output a csv file at a given location')
    parser.add_argument('--input', default='input/example_input.vcf', type=str, help='Path to input VCF file')
    parser.add_argument('--output', default='output/parsed.csv', type=str, help='Path to output CSV file')
    return(parser)


# TODO - Switch to class based methods for VCF variants/ExAC data
# TODO - File extension check input for vcf using os module

def get_variant_annotation(chromosome = 14, position = 21853913, ref = 'T', alt = 'C'):
    """
    Get variant annotation from ExAC for a given chromosome/position/ref/alt

    Keyword arguments:
    chromosome(int, string) - Chromosome of variation
    position(int) -- Position of variation(bp)
    ref(string) -- Reference allele
    alt(string or list of strings) -- Alternative alleles

    Return:
    annotation(list) - List of lists of strings containing allele frequency, worst possible annotation, gene location, and potential transcripts
    """
    # List based on synonymous, nonsynonymous, deleterious
    ranked_annotations = [None, 'synonymous_variant', 'intron_variant', 'non_coding_transcript_exon_variant', '3_prime_UTR_variant', '5_prime_UTR_variant', 
    'stop_retained_variant', 'splice_acceptor_variant', 'splice_donor_variant', 'splice_region_variant', 'initiator_codon_variant',  'missense_variant','stop_lost', 'stop_gained']

    # Type check alternate allele for looping as string or list of strings
    if isinstance(alt, str):
        annotation = get_exac_variant(chromosome, position, ref, alt)

        # TODO - Deal with slicing error when None
        if annotation[1] is not None:
            annotation[1] = ranked_annotations[max(ranked_annotations.index(i) for i in annotation[1] if i is not None)] # Argmax the worst annotation rank
    elif isinstance(alt, list):
        annotation = []
        # TODO - Check if rate limited API otherwise switch to list comprehension, map or multiprocessing
        for alternate_allele in alt:
            annotation.append(get_exac_variant(chromosome, position, ref, alternate_allele))

        # TODO - use all to check for None and compress into single list for indels
        ## Seems like all variations of indels return nothing
        if(len(annotation) == 1):
            ## TODO - Deal with slicing error when None
            if annotation[0] is not None and annotation[0][1] is not None and annotation[0][1]:
                annotation[0][1] = ranked_annotations[max(ranked_annotations.index(i) for i in annotation[0][1] if i is not None)] # Argmax the worst annotation rank 
    else:
        raise Exception("Alternative Allele not string or list") # Total failure on weird typed input

    return(annotation)

def get_exac_variant(chromosome = 14, position = 21853913, ref = 'T', alt = 'C'):
    """
    Pulls variant information from ExAC based on given chromosome, base pair starting position, reference allele and alternate allele

    Keyword arguments:
    chromosome(int, string) - Chromosome of variation
    position(int) -- Position of variation(bp)
    ref(string) -- Reference allele
    alt(string or list of strings) -- Alternative alleles

    Return:
    annotation(list) - List of strings containing allele frequency, worst possible annotation, gene location, and potential transcripts
    """
    base_url = "http://exac.hms.harvard.edu/rest/variant/" # Base variant ExAC API
    
    # Get request to Variant API
    r = requests.get(url = base_url + "-".join([str(chromosome), str(position), str(ref), str(alt)])) 
    
    # Check for 404 failed endpoint and on failure
    ## TODO - Better response on endpoint failure
    if r.status_code == 404:
        return('failure') # Silent error

    # Convert response to json
    data = r.json() 

    ## TODO - Potentially memoise and cache json based on inputs

    # Get relevant information from ExAC
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

def annotate_vcfs(input_vcf = None, output_file = 'output/parsed.csv'):
    """
    Parses and annotates a given vcf file using the ExAC variant database

    Keyword arguments: 
    input_vcf(str) -- The path to the VCF file to annotate (default None)
    output_file(str) -- The directory and file name to output a csv to (default output/parsed.csv)
    """
    print("Progress 0%: Reading VCF file")
    
    # Read input or error out
    try:
      vcf_reader = vcf.Reader(open(input_vcf, 'r'))
    except:
      raise Exception("Error: Could not open input file")

    # TODO - Cache results based on if same input

    print("Progress 10%: Parsing VCF File")

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

    print("Progress 30%: Annotating VCF from ExAC")

    # Get annotations from ExAC
    annotations = []
    for row in vcf_df.itertuples():
      annotations.append(get_variant_annotation(row[1], row[2], row[3], row[4]))

    # Update dataframe with annotations
    vcf_df['ALLELE_FREQ'] = [i[0][0] for i in annotations] # Allele frequency
    vcf_df['WORST_CONSEQUENCE'] = [i[0][1] for i in annotations] # Worst SNP consequence
    vcf_df['GENES'] = [i[0][2] for i in annotations] # Potential gene location
    vcf_df['TRANSCRIPTS'] = [i[0][3] for i in annotations] # Potential variant transcripts

    print("Progress 90%: Saving file")

    vcf_df.to_csv(output_file, index = False)

    print("Progress 100% - File saved at " + output_file)



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    annotate_vcfs(input_vcf = args.input, output_file = args.output)