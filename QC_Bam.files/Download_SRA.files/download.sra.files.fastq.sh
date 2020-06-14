#!/bin/bash

#$ -N sra
#$ -t 1:89
#$ -tc 2
#$ -q rg-el7
#$ -l virtual_free=16G,h_rt=24:00:00
#$ -m abe
#$ -M razielar.amador@crg.eu
#$ -cwd
#$ -e cluster_out/
#$ -o cluster_out/
#$ -pe smp 4

### 1) Read the file:
file=${SGE_TASK_ID}

file=$(grep -v Run sra.download.tsv | sed -n ${file}p | awk -F "\t" '{print $1}')
echo $file

### 2) Run the command:

module load SRA-Toolkit

fastq-dump --split-3 --gzip $file




