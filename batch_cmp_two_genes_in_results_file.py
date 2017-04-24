import pdb
import os
from argparse import ArgumentParser
import subprocess

pwd = os.path.dirname(__file__)
rsem_res_path = "/srv/gsfs0/projects/snyder/tejas/sirna/RSEM"
genes_ext = ".genes.results"
outdir = os.path.join(pwd,"plots")
if not os.path.isdir(outdir):
	os.mkdir(outdir)

description = "Calls generate_expression_plots.py in batch."
parser = ArgumentParser(description=description)
parser.add_argument('-c',"--control-sheet",default=os.path.join(pwd,"siRNA_controlSheet_2016-08-09_ja.txt"),help="Default is %(default)s.")
parser.add_argument('-s',"--submission-sheet",default=os.path.join(pwd,"sirna_submissionSheet_2016-08-09_ja.txt"),help="Default is %(default)s.")

args = parser.parse_args()

ctl_sheet = open(args.control_sheet,'r')
submis_sheet = open(args.submission_sheet,'r')

ctl_header = ctl_sheet.readline().strip("\n").split("\t") #header
submis_header = submis_sheet.readline().strip("\n").split("\t") #header
submis_sheet.readline() #control line?
submis_sheet.readline() #control line?

ctl_controlledby_fieldindex = ctl_header.index("controlled_by")
ctl_filepath_fieldindex = ctl_header.index("submitted_file_name")
ctl_gene_fieldindex = ctl_header.index("dataset")
ctl_dico = {} #keys are the value of the controlled_by column. Values are the gene name. 
for line in ctl_sheet:
	line = line.strip()
	if not line:
		continue
	line = line.split("\t")
	controlled_by = line[ctl_controlledby_fieldindex].strip()
	gene = line[ctl_gene_fieldindex].strip()
	if not gene:
		raise Exception("No control gene for line {line}.".format(line=line))
#	fastqfile = line[ctl_filepath_fieldindex].strip()
#	if not fastqfile:
#		raise Exception("No FASTQ file for control line {line}.".format(line=line))
	ctl_dico[controlled_by] = gene

submis_controlledby_fieldindex = submis_header.index("controlled_by")
submis_filepath_fieldindex = submis_header.index("submitted_file_name")
submis_gene_fieldindex = submis_header.index("dataset")

submis_dico = {}
for line in submis_sheet:
	line = line.strip()
	if not line:
		continue
	line =  line.split("\t")
	gene = line[submis_gene_fieldindex].strip().split("-")[-1]
	controlled_by = line[submis_controlledby_fieldindex].strip()
	fastqfile = line[submis_filepath_fieldindex].strip()
	if not fastqfile:
		raise Exception("No FASTQ file for sample line {line}.".format(line=line))
	if fastqfile.startswith("131205_LYNLEY_0382_BC36PYACXX_L8_CACTGT"):
		continue
	submis_dico[fastqfile] = {
		"sample_gene": gene,
		"control_gene": ctl_dico[controlled_by].split("-")[-1]
	}

genes_ext = ".genes.results"
outdir = os.path.join(pwd,"plots")
if not os.path.isdir(outdir):
	os.mkdir(outdir)
for samplefile in submis_dico:
	sample_rsem = os.path.basename(samplefile).split(".")[0]
	sample_rsem = sample_rsem.rstrip("_1_pf")
	sample_rsem = sample_rsem.rstrip("_2_pf") + genes_ext
	sample_rsem = os.path.join(rsem_res_path,sample_rsem)
	if not os.path.exists(sample_rsem):
		#raise Exception("Sample rsem file {sample_rsem} doesn't exist.".format(sample_rsem=sample_rsem))
		print("Sample rsem file {sample_rsem} doesn't exist.".format(sample_rsem=sample_rsem))
	sample_gene = submis_dico[samplefile]["sample_gene"]
	ctl_gene = submis_dico[samplefile]["control_gene"]
	print(sample_gene + " : " + ctl_gene)
	outfile = os.path.join(outdir,os.path.basename(sample_rsem) + ".plot.txt")
#	cmd = "python /srv/gsfs0/software/gbsc/encode/current/encode/sirna/cmp_two_genes_in_results_file.py -c {ctl_gene} -t {sample_gene} -r {sample_rsem} -o {outfile}".format(ctl_gene=ctl_gene,sample_gene=sample_gene,sample_rsem=sample_rsem,outfile=outfile)
#	popen = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#	stdout,stderr = popen.communicate()
#	retcode = popen.returncode
##	if retcode:
##		print("Command {cmd} failed with return code {retcode}. Stderr is {stderr}.".format(cmd=cmd,retcode=retcode,stderr=stderr))
#	
