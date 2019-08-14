#!/bin/bash
#$ -N pic30
#$ -t 1-36
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
path=$(/bin/sed -n ${Input}p /users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/dir.tsv |/bin/awk {'print $3'})
file=$(/bin/sed -n ${Input}p /users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/dir.tsv |/bin/awk {'print $2'})
sample=$(/bin/sed -n ${Input}p /users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/dir.tsv |/bin/awk {'print $1'})

#---make directories for each sample
mkdir /users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/$sample
cd ~/tmp
#---picard summury metrics
module load picard/2.6.0-Java-1.8.0_162
java -jar $EBROOTPICARD/picard.jar CollectAlignmentSummaryMetrics \
      I=$file \
      O=/users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/${sample}/${sample}_metrics.txt \
      R=/nfs/users2/rg/projects/references/Genome/H.sapiens/GRCh38/GRCh38.primary_assembly.genome.fa
#---Run picard GCBias_metrics
module load picard/2.6.0-Java-1.8.0_162
java -jar $EBROOTPICARD/picard.jar CollectGcBiasMetrics \
        I=$file \
        O=/users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/${sample}/${sample}_GC_metrics.txt \
        CHART=/users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/${sample}/${sample}_GC_metrics.pdf \
        R=/nfs/users2/rg/projects/references/Genome/H.sapiens/GRCh38/GRCh38.primary_assembly.genome.fa \
        S=/users/rg/isadeghi/RNAseq_path/PRJNA235930/QC/${sample}/${sample}_GC_summary.txt


