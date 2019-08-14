#!/bin/bash

#$ -N bamQC
#$ -t 1-84 
#$ -tc 2
#$ -M raziel.amador@crg.es
#$ -m abe
#$ -q rg-el7
#$ -l virtual_free=16G,h_rt=24:00:00
#$ -cwd
#$ -pe smp 4
#$ -o cluster_out/
#$ -e cluster_out/

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


