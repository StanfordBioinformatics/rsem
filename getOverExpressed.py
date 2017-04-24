#!/usr/bin/env python

import argparse
import glob
import os

###
#Nathaniel Watson
#nathankw@stanford.edu
###

over_expr_fn = "over_expressed.txt"
under_expr_fn = "under_expressed.txt"

description = "Given a directory of raw plot files generated from cmp_two_rsem_results_files.py, creates two files in the current directory called {o} and {u}. The format of these two files is 1) filename, 2)control TPM, and 3) treatment TPM.".format(o=over_expr_fn,u=under_expr_fn)
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-d",required=True,help="The directory containing raw plot files generated from cmp_two_rsem_results_files.py. It is assumed that each ends with .txt.")

args = parser.parse_args()
raw_plots_dir = args.d

under = open(under_expr_fn,'w')
over = open(over_expr_fn,'w')
for i in glob.glob(os.path.join(raw_plots_dir,"*.txt")):
	fname = os.path.basename(i)
	fh = open(i,'r')
	fh.readline() #header
	line = fh.readline().strip().split("\t")
	ctl_tpm = float(line[2])
	treat_tpm = float(line[4])
	if ctl_tpm <= treat_tpm:
		over.write(fname + "\t" + str(ctl_tpm) + "\t" + str(treat_tpm) + "\n")
	else:
		under.write(fname + "\t" + str(ctl_tpm) + "\t" + str(treat_tpm) + "\n")
		#print("{ctl_tpm} : {treat_tpm}".format(ctl_tpm=ctl_tpm,treat_tpm=treat_tpm))
under.close()
over.close()
