#!/usr/bin/env python

import argparse
import os
import sys
import subprocess

description = "Calls cmp_two_rsem_results_files.py in batch."

parser = argparse.ArgumentParser(description=description,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-i",required=True,help="""The tab-delimited input file identifying the sample and control RSEM gene/isoform result files to compare against each other for the gene/isoform of interest. The fields are
	1) sample RSEM results file name,
	2) control RSEM results file name,
	3) gene/isoform id or name. 

	Note that in field 3, the values should all be IDs or names, not a mixture of both.	
	Lines beginning with a '#' will be skipped.""")
parser.add_argument("-o",required=True,help="The output directory.")
parser.add_argument("-r",required=True,help="The directory containing all of the RSEM result files (*.genes.results, *.isoforms.results).")
parser.add_argument("-c","--continue-on",action="store_true",help="Presence of this option indicates to continue on instead of raise an Exception if either the sample or the control RSEM file doesn't exist. In this case, only an error message will be written to stderr instead of an Exception killing the program flow.")
parser.add_argument("--by-name",action="store_true",help="Presence of this option means that the values specified in column 3 of -i is a gene or transcript name, compared to an ID. They should all be names or IDs in this column, not a mix of both.")

args = parser.parse_args()
infile = args.i
outdir = args.o
continue_on = args.continue_on
rsem_results_folder = args.r
by_name = args.by_name

RSEM_GENE_QUANT_SUFFIX = ".genes.results"
fh = open(infile,"r")
header = fh.readline()
for line in fh:
	if line.startswith("#"):
		continue
	line = line.strip("\n")
	if not line:
		continue
	line = line.split("\t")
	sample_rsem = line[0].strip()
	ctl_rsem = line[1].strip()
	feature = line[3].strip()
	outfile = os.path.join(outdir,os.path.basename(sample_rsem) + "_rawplot_" + feature + ".txt")
	

	cmd = "python /srv/gsfs0/software/gbsc/encode/current/encode/sirna/CreatePlots/cmp_two_rsem_results_files.py -c {ctl_rsem} -s {sample_rsem} -f {feature} -o {outfile} --by-name {by_name}".format(ctl_rsem=ctl_rsem,sample_rsem=sample_rsem,feature=feature,outfile=outfile,by_name=by_name)
	popen = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = popen.communicate()
	retcode = popen.returncode
	if retcode:
		print("Command {cmd} failed with return code {retcode}. Stdout is {stdout}.\n Stderr is {stderr}.".format(cmd=cmd,retcode=retcode,stdout=stdout,stderr=stderr))
