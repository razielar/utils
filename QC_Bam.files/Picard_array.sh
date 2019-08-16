#!/bin/bash

#$ -N Picard
#$ -t 1-84 
#$ -tc 2
#$ -q rg-el7
#$ -l virtual_free=16G,h_rt=24:00:00
#$ -cwd
#$ -pe smp 4
#$ -o cluster_out/
#$ -e cluster_out/

#Job array:
Input=${SGE_TASK_ID}

#Get each line of the input file as path
path=$(sed -n ${Input}p input_bamQC.tsv | awk {'print $2'})
file=$(sed -n ${Input}p input_bamQC.tsv | awk {'print $3'})
sample=$(sed -n ${Input}p input_bamQC.tsv | awk {'print $1'})
dme_genome=/users/rg/projects/references/Genome/D.melanogaster/dm6/dm6.fa

#---make directories for each sample: Not run this because it's was already created by bamqc_array.sh
# mkdir  -p  QC/$sample
# cd ~/tmp

#---picard summury metrics
module load picard/2.6.0-Java-1.8.0_162
java -jar $EBROOTPICARD/picard.jar CollectAlignmentSummaryMetrics \
      I=$file \
      O=QC/${sample}/${sample}_metrics.txt \
      R=$dme_genome

#---picard GCBias_metrics
module load picard/2.6.0-Java-1.8.0_162
java -jar $EBROOTPICARD/picard.jar CollectGcBiasMetrics \
        I=$file \
        O=QC/${sample}/${sample}_GC_metrics.txt \
        CHART=QC/${sample}/${sample}_GC_metrics.pdf \
        R=$dme_genome \
        S=QC/${sample}/${sample}_GC_summary.txt
