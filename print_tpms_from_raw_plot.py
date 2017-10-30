#!/bin/env python

###
#Nathaniel Watson
#2017-10-30
#nathankw@stanford.edu
###

import argparse

description = "Given a text file output by cmp_two_rsem_results_files.py, which is used to create the percent knockdown plot, the control and treatment TPM fields are extracted and printed to stdout. The control field is first, followed by a tab character, follewed by the treatment."
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-i","--infile",required=True,help="The text file output by cmp_two_rsem_results_files.py, which contains the TPM for the control and the sample.")
args = parser.parse_args()

infile = args.infile
fh = open(infile,'r')
header = fh.readline().strip().split("\t")
#The header should be in the format
# ["feature" "control_dataset" "control_tpm" "treatment_dataset" "treatment_tpm"]

ctl_tpm_index = header.index("control_tpm")
treat_tpm_index = header.index("treatment_tpm")

data_line = fh.readline().strip("\n").split("\t")
print(data_line[ctl_tpm_index] + "\t" + data_line[treat_tpm_index])
fh.close()


