import sys
sys.path.insert(0, '..') # Dirty fix to import cross folders
from oncolonnator import get_exac_variant, get_variant_annotation, annotate_vcfs
import pytest
import os

class TestOncolonnator:
    def test_get_exac_variant_success(self):
        """
        Test ExAC variant API using example information
        """
        sample1 = get_exac_variant(chromosome = 14, position = 21853913, ref = 'T', alt = 'C')
        assert(sample1 == [4.6048996131884326e-05, 
        	['synonymous_variant', 'non_coding_transcript_exon_variant'], 
        	['ENSG00000100888'], 
        	['ENST00000430710', 'ENST00000399982', 'ENST00000557364', 'ENST00000557727']])

    def test_get_exac_variant_failure_on_pos(self):
        """
        Test ExAC variant 404 on fake position
        """
        sample1 = get_exac_variant(chromosome = 14, position = 'robot', ref = 'T', alt = 'Z')
        assert(sample1 == "failure")

    def test_get_exac_variant_failure_on_allele(self):
        """
        Test ExAC variant using unknown alternate alleles
        """
        sample1 = get_exac_variant(chromosome = 14, position = 100, ref = 'T', alt = 'thisisafakeallele')
        assert(sample1 == [None, None, None, None])

    def test_get_variant_annotation(self):
        """
        Test ExAC parser returns correct information
        """
        snp1 = get_variant_annotation(chromosome = 14, position = 21853913, ref = 'T', alt = 'C')
        assert(snp1 == [4.6048996131884326e-05,'non_coding_transcript_exon_variant', ['ENSG00000100888'], ['ENST00000430710', 'ENST00000399982', 'ENST00000557364', 'ENST00000557727']])

    def test_annotate_vcfs(self):
        """
        Test end to end annotation function
        """
        pass