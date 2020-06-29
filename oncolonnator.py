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

def annotate_vcfs(input_vcf, output_file):
    try:
      vcf_reader = vcf.Reader(open(input_vcf, 'r'))
    except:
      print("Error: Could not open input file")

# GET request API calls to ExAC
## https://www.geeksforgeeks.org/get-post-requests-using-python/

if __name__ == "__main__":
    annotate_vcfs("input/example.vcf")