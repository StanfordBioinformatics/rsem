#!/usr/bin/env Rscript

###
#Nathaniel Watson
#nathankw@stanford.edu
###

library(argparse)
#library(Hmisc)

description = "Creates a barplot depicting the differential expression of a gene or transcript between a control and treatment conditions."
parser = ArgumentParser(description=description)
parser$add_argument("--data-file",required=T,help="A file output by batch_cmp_two_rsem_results_files.py. This is a tab-delimited file with a header line having field names 1) feature, 2) control_dataset, 3) control_tpm, 4) treatment_dataset, 5) treatment_tpm. The next and final line contains the values for the defined fields.") 
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

scale = 100.0/ctl_tpm

scaled_ctl_tpm = 100
scaled_treat_tpm = scale * treat_tpm

ctl_treat_tpm = c(ctl_tpm,treat_tpm)
scaled_ctl_treat_tpm = c(scaled_ctl_tpm,scaled_treat_tpm)


jpeg(file=outfile)
#jpeg(file=outfile,width=480,height=480)
ymax = scaled_ctl_tpm
ymin = 0
ylims = c(ymin,ymax)
par("lab" = c(1,round(ymax/5),7),las=1,oma=c(6,0,0,0)) #las=1 means axis text is always horizontal.
subtext = paste(" Percent expression of ",t$feature," relative to the its expression in the control.",sep="")
subtext = c(subtext," Expression values were quantified in Transcripts Per Million (TPM), and were", " generated using RSEM version 1.2.30. The integer centered on each bar provides"," the actual TPM value. See the RSEM Protocol document attached to the"," experiment that details the Snyder RSEM analysis.")
len_subtext = length(subtext)
bp = barplot(height=c(scaled_ctl_treat_tpm),main=t$feature,ylim=ylims,ylab="Knockdown Expression (%) Relative to Control",names.arg=c("Control","Treatment"),xlim=c(0,1),width=0.2)

#minor.tick(nx=1,ny=2) #need to library(Hmisc) to use minor.tick().
text(bp,0,round(ctl_treat_tpm),cex=1,pos=3) #add the actual TPM expression values at bottom of bars
for (i in 1:len_subtext) {
	mtext(subtext[i],side=1,line=i-1,outer=T,adj=0)
}
dev.off()
