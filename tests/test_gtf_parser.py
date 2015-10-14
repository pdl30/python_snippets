#!/usr/bin/python

########################################################################
# 14 Oct 2015
# Patrick Lombard, Centre for Stem Stem Research
# Core Bioinformatics Group
# University of Cambridge
# All right reserved.
########################################################################

import pytest
import os
from python_snippets.gtf_parser import bed_to_gtf
import tempfile


def test_annotate_sam():
	bed1 = os.path.join(os.path.dirname(__file__), 'sample1.bed')
	bed2 = os.path.join(os.path.dirname(__file__), 'sample2.bed')
	fh1 = tempfile.NamedTemporaryFile(delete = False)
	fh2 = tempfile.NamedTemporaryFile(delete = False)
	bed_to_gtf(bed1, fh1)
	fh1.close()
	assert open(os.path.join(os.path.dirname(__file__), 'output1.gtf')).read() == open(fh1.name).read()
	bed_to_gtf(bed2, fh2)
	fh2.close()
	assert open(os.path.join(os.path.dirname(__file__), 'output2.gtf')).read() == open(fh2.name).read()
