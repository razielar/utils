#!/bin/bash
#$ -N bamqc8642
#$ -t 1-35
#$ -tc 2
#$ -M iman.sadeghi@crg.es
#$ -m abe
#$ -q rg-el7 
#$ -pe smp 2
#$ -o /dev/null
#$ -e /dev/null
#define the directory as Task ID
Input=${SGE_TASK_ID}
#get each line of the input file as path
file=$(/bin/sed -n ${Input}p /users/rg/isadeghi/RNAseq_path/PRJNA318642/QC/dir.tsv |/bin/awk {'print $2'})
newname=$(/bin/sed -n ${Input}p /users/rg/isadeghi/RNAseq_path/PRJNA318642/QC/dir.tsv |/bin/awk {'print $1'})
mkdir /users/rg/isadeghi/RNAseq_path/PRJNA318642/QC/$newname
#--- move to local drive for a better performance
cd ~/tmp

#---Load qualimap module ---#
module load qualimap
#---Run qualimap bamqc ---#
qualimap bamqc --java-mem-size=4G \
	-bam $file \
	-gd HUMAN \
	-gff /users/rg/projects/references/Annotation/H.sapiens/gencode28/gencode.v28.primary_assembly.annotation.gtf \
	-outdir /users/rg/isadeghi/RNAseq_path/PRJNA318642/QC/$newname \
	-outfile ${newname}_bamqc.pdf \
	-outformat PDF \
	-p strand-specific-reverse


