#!/usr/bin/env Rscript

###
#Nathaniel Watson
#nathankw@stanford.edu
###

library(argparse)
library(Hmisc) #imports minor.tick

description = "Creates a barplot depicting the differential expression of a gene or transcript between a control and treatment conditions."
parser = ArgumentParser(description=description)
parser$add_argument("--data-file",required=T,help="A file output by batch_cmp_two_rsem_results_files.py. This is a tab-delimited file with a header line having field names 1) gene_name, 2) control_dataset, 3) control_tpm, 4) treatment_dataset, 5) treatment_tpm. The next and final line contains the values for the defined fields.")
parser$add_argument("--outfile",required=T,help="The name of the JPEG output file containing a barplot.")

args = parser$parse_args()

data_file = args$data_file
outfile = args$outfile

t = read.table(data_file,header=T,sep="\t",as.is=T)
ctl_tpm = as.numeric(t$control_tpm)
treat_tpm = as.numeric(t$treatment_tpm)

#treat control as 100% transcription rate compared to knockdown in treatment
#scale control to 100%: 100 = x * ctl_tpm
OFFSET = 1
ctl_tpm = ctl_tpm + OFFSET
treat_tpm = treat_tpm + OFFSET

fold_change = treat_tpm/ctl_tpm
log2_fold_change = log2(fold_change)
jpeg(file=outfile,width=480,height=480)
#ylim_min_max = c(-20,20) #log2(1million) is ~20
#abs_fc = abs(log2_fold_change)
ymax = round(abs(log2_fold_change)) +1
ymin = -1 * ymax
ylims = c(ymin,ymax)
par("lab" = c(1,ymax*2,7),las=1,oma=c(6,0,0,0)) #las=1 means axis text is always horizontal. oma is four outer margin. 
subtext = paste(" Log base 2 fold change of the expression of the gene ",t$gene_name,sep="")
subtext = c(subtext," relative to the same gene in the control."," Expression values were quantified in Transcripts Per Million"," (TPM), and were generated using RSEM version 1.2.30."," The integer centered at the bar is the actual TPM value of the treatment gene."," See the RSEM Protocol document attached to the experiment that details the Snyder"," RSEM analysis.")
len_subtext = length(subtext)
bp = barplot(height=c(log2_fold_change),main=t$gene_name,ylim=ylims,ylab="log2(fold change)",names.arg=c("Treatment"),xlim=c(0,1),width=0.1)

minor.tick(nx=1,ny=2)
abline(h=0)
text(bp, 0, round(treat_tpm),cex=1,pos=3)
for (i in 1:len_subtext) {
	mtext(subtext[i],side=1,line=i-1,outer=T,adj=0)
}
dev.off()
