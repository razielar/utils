#!/bin/bash 

#$ -N intersect_exon
#$ -t 1-810
#$ -tc 20
#$ -q rg-el7
#$ -l virtual_free=16G,h_rt=24:00:00
#$ -cwd
#$ -pe smp 4
#$ -o cluster_out/
#$ -e cluster_out/

#Job array: 
Input=${SGE_TASK_ID}

# Create log folder
mkdir cluster_out/

# Create reuslt folder:
mkdir Results/

#Files
bed_file=/nfs/users2/rg/ramador/D_me/Data/Bed_files/dm6_r6.29/mRNAs_and_lncRNAs_exons/Results/GeneID.TranscriptID.Exons.16412.genes.bed
lncRNA_mRNA=/nfs/users2/rg/ramador/D_me/RNA-seq/Genomic_Location_lncRNAs/dm6_r6.29/cleanSpurious_lncRNAs_genome_wide/Data/genic.exonic.all.pairs.no.header.tsv

lncRNA=$(sed -n ${Input}p $lncRNA_mRNA | awk -F "\t" {'print $1'})
mRNA=$(sed -n ${Input}p $lncRNA_mRNA | awk -F "\t" {'print $3'} )

echo $lncRNA
echo $mRNA

#Generate tmp bed files: 
grep $lncRNA $bed_file > ${lncRNA}_${Input}.bed
grep $mRNA $bed_file > ${mRNA}_${Input}.bed

# Bed tools version v2.27 
module load BEDTools

# #Bed tools process: 
bedtools intersect -a ${lncRNA}_${Input}.bed  -b ${mRNA}_${Input}.bed -wo > ${lncRNA}_${Input}_intersect.bed

rm ${lncRNA}_${Input}.bed
rm ${mRNA}_${Input}.bed


mv ${lncRNA}_${Input}_intersect.bed Results/



