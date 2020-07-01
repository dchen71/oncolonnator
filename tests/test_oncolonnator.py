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

    def test_annotate_vcfs(self, tmp_path):
        """
        Test end to end annotation function
        """
        # Create test vcf file
        tmp_dir = tmp_path
        file1 = tmp_dir / "test.csv"
        file1.write_text("1	931393	.	G	T	2.17938e-13	.	AB=0;ABP=0;AC=0;AF=0;AN=6;AO=95;CIGAR=1X;DP=4124;DPB=4124;DPRA=0.999031;EPP=9.61615;EPPR=316.776;GTI=0;LEN=1;MEANALT=1;MQM=59.7579;MQMR=65.2274;NS=2;NUMALT=1;ODDS=591.29;PAIRED=0.989474;PAIREDR=0.966741;PAO=0;PQA=0;PQR=0;PRO=0;QA=3774;QR=160284;RO=4029;RPL=51;RPP=4.13032;RPPR=101.278;RPR=44;RUN=1;SAF=40;SAP=8.15326;SAR=55;SRF=1663;SRP=269.369;SRR=2366;TYPE=snp	GT:GQ:DP:DPR:RO:QR:AO:QA	0/0/0:132.995:2063:2063,0:2063:82063:0:0	0/0/0:132.995:2061:2061,95:1966:78221:95:3774")
        
        annotate_vcfs(file1, str(tmp_dir/"output.csv"))

        assert(os.path.exists(tmp_dir/"output.csv"))
        assert(os.stat(tmp_dir/"output.csv").st_size > 0)

