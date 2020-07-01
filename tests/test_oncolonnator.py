import sys
sys.path.insert(0, '..') # Dirty fix to import cross folders
from oncolonnator import *
import pytest
import os

class TestOncolonnator:
    def test_get_exac_variant_success(self):
        """
        Test ExAC variant API using example information
        """

    def test_get_exac_variant_failure(self):
        """
        Test ExAC variant 404 on fake input
        """
        pass

    def test_get_variant_annotation(self):
        """
        Test ExAC parser returns correct information
        """
        pass

    def test_annotate_vcfs(self):
        """
        Test end to end annotation function
        """
        pass