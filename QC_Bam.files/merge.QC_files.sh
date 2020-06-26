#!/bin/bash

path=$1 

cd ${path}/QC/

for i in `ls -d */`;
do cd $i

   ###---- 1) Picard CollectAlignmentSummaryMetrics: 
   tail -3 ${i%/}_metrics.txt | cut -f3-8,18-21 | column -t >${i%/}_metrics.tsv #_metrics.txt


   ###---- 2) Qualimap:
   sed -n 20,57p ${i%/}_bamqc.txt | grep -E 'reads|bases|rate|GC' | grep '=' | awk -F "= " '{print $2}' | sed 's/[a-z]//g' | sed 's/%//g' | sed 's/(.*)//g' | tr -d '[:blank:]'| tr '\n' '\t' | sed 's/,//g' | cut -f1,2,7,8,11,12 | column -t>${i%/}_bamqc.tsv #_bamqc.txt

   ###---- 3) Picard CollectGcBiasMetrics: 
   tail -3 ${i%/}_GC_summary.txt | awk '{for(i=4;i<=6;++i)printf  $i""FS ; print "\t"}'| column -t >${i%/}_GC_summary.tsv #_GC_summary.txt

   #--- Merge the output from the previous 3 commands: 
   paste *bamqc.tsv *GC_summary.tsv *metrics.tsv | column -t >${i%/}.qcData
   cp *qcData ../
   cd ../

done

###--- Concatenate the 'header' file with all *.qcData files 
cat header.txt *qcData | column -t > QC_details 

###----- Generate the file with the 'sample names'
ls *qcData | sed -e "1iSample" | sed 's/.qcData//g' > samples


###---mergin sample_id and QC data, and removing comma from file---###
paste samples QC_details | sed 's/,//g' | column -t>QC_Data.csv

