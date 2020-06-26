#!/bin/bash

#$ -N bamQC
#$ -t 1-84 
#$ -tc 2
#$ -q rg-el7
#$ -l virtual_free=16G,h_rt=24:00:00
#$ -cwd
#$ -pe smp 4
#$ -o cluster_out/
#$ -e cluster_out/

# Job array:
Input=${SGE_TASK_ID}

# Create 'cluster_out': 
mkdir cluster_out

#--- Take bam file and sample name ---#
file=$(sed -n ${Input}p input_bamQC.tsv | awk {'print $3'}) #bam_file
newname=$(sed -n ${Input}p input_bamQC.tsv | awk {'print $1'}) #sample_name

# Generate the specific sample folder: 
mkdir -p  QC/$newname

#--- GTF file ---#
gtf=/nfs/users2/rg/projects/references/Annotation/D.melanogaster/dmel_r6.29/mRNA_ncRNA/ucsc.dmel-all-r6.29.mRNA.nRNA.190.length.selection.type.sorted.no.Overlapping.Sorted.gtf

#--- Load qualimap module ---#
module load qualimap

#--- Run qualimap bamqc ---# 
qualimap bamqc --java-mem-size=4G \
        -bam $file \
        -gff $gtf \
        -outdir QC/$newname \
        -outfile ${newname}_bamqc.pdf \
        -outformat PDF

# --- Rename genome_results.txt to sample_name_bamqc.txt ---# 
mv QC/$newname/genome_results.txt QC/$newname/${newname}_bamqc.txt



