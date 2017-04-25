#!/bin/bash -eu 
set -o pipefail

###
#Nathaniel Watson
#nathankw@stanford.edu
###

module load r/3.3.1
module load python/2.7.9

function help {
	echo "Description:"
	echo " Calls plot_perc_change.r in batch . Given a directory of raw plot files created by cmp_two_rsem_results_files.py, for "
	echo " each .txt file in the directory it will create a bar graph and save it as a JPEG in a subdirectory of -p called Barplots."
	echo
  echo "Args:"
	echo " -p The path to the directory containing the files to make plots out of. These would have been created using create_plot_raw_files.py"
	echo " -h Shows this help text."
	exit
}

plots_dir=
while getopts "p:h" opt
do
  case $opt in  
    p) plots_dir=${OPTARG}
       ;;  
    h) help
       ;;  
  esac
done

if [[ ${#@} -eq 0 ]]
then
  help
fi

if [[ -z ${plots_dir} ]]
then
	help
fi

bargraphs_dir=${plots_dir}/Barplots
if ! [[ -d $bargraphs_dir ]]
then
	mkdir $bargraphs_dir
fi

for i in ${plots_dir}/*.txt
do 
	filename=$(basename $i)
	outfile=${bargraphs_dir}/${filename%.txt}.jpeg
	echo $filename
	Rscript plot_perc_change.r --data-file $i --outfile $outfile
done
