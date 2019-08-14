#!/bin/bash
#$ -N qc-files
#$ -t 1
#$ -tc 1
#$ -q short-sl7
#$ -o /dev/null
#$ -e /dev/null
Input=${SGE_TASK_ID}
path=$(/bin/sed -n ${Input}p /users/rg/isadeghi/RNAseq_path/dir2.tsv | /bin/awk '{print $1}')

cd ${path}/QC/

for i in `ls -d */`;
do cd $i
#---extracting from aliment metrics
tail -3 ${i%/}_metrics.txt | cut -f3-8,18-21|column -t >${i%/}_metrics.tsv


###----Extracting rows from Bamqc report---###
sed -n 20,57p ${i%/}_bamqc.txt | grep -E 'reads|bases|rate|GC' | grep '=' | awk -F "= " '{print $2}' | sed 's/[a-z]//g' | sed 's/%//g' | sed 's/(.*)//g'| tr -d '[:blank:]'| tr '\n' '\t' | sed 's/,//g'|cut -f1-4,7-8 | column -t>${i%/}_bamqc.tsv
 
###----Extracting columns from Picard GC summary---###
  tail -3 ${i%/}_GC_summary.txt | awk '{for(i=4;i<=6;++i)printf  $i""FS ; print "\t"}'| column -t >${i%/}_GC_summary.tsv

#---Merging QC data for samples
paste *bamqc.tsv *GC_summary.tsv *metrics.tsv | column -t >${i%/}.qcData
cp *qcData ../
cd ../
done

###--- Merging "header" and QC files---###
cat header *qcData | column -t> QC_details

###-----Adding sample names to the files---
ls *qcData | sed -e "1iSample" | sed 's/.qcData//g' >samples 


###---mergin sample_id and QC data, and removing comma from file---###
paste samples QC_details | sed 's/,//g' | column -t>QC_Data.csv
