### Move bigwig files to a specific path 

import os
import sys 
import re

os.chdir('/users/rg/ramador/D_me/RNA-seq/Pipelines/grape-nf-dm6-r6.29')

pipeline_db="pipeline.db"

non_strand_bw=[]
strand_bw=[]
with open(pipeline_db, 'r') as pipeline_db:
    for i in pipeline_db:
        i= i.rstrip().split('\t')
        if re.search(r'bigWig', i[3]): #select bigWig files
            bigwig=i
            if re.search(r'NONE', bigwig[6]): #non-strand specific
                non_strand=bigwig
                if re.search(r'MultipleRawSignal', non_strand[4]): #Multiple 
                    tmp_non_strand=non_strand[2]
                    non_strand_bw.append(tmp_non_strand)
            if re.search(r'MATE2_SENSE', bigwig[6]): #strand-specific
                strand=bigwig
                if re.search(r'Multiple', strand[4]): #Multiple 
                    tmp_strand=strand[2]
                    strand_bw.append(tmp_strand)
            

#Set the destination: 
path_destination=" /users/rg/ramador/public_html/dme/UCSC_tracks/grape-nf-dm6.29"

#Combine strand and non-strand specific bigwigs 
final_ouput=non_strand_bw+strand_bw

for i in final_ouput:
    cmd="cp "+i+path_destination
    print(cmd)
    os.system(cmd)


