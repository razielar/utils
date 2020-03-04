#!/usr/bin/env python 

### Move bigwig files to a specific path 

import os
import sys 
import re

os.chdir('/users/rg/ramador/D_me/RNA-seq/Pipelines/grape-nf-dm6-r6.29')

pipeline_db="pipeline.db"

#We are going to store unique and multiple bigWig files: 
keys=['multiple', 'unique']
dict_non_strand={i:[] for i in keys}
dict_strand={i:[] for i in keys}

with open(pipeline_db, 'r') as pipeline_db:
    for i in pipeline_db:
        i= i.strip().split('\t')
        if re.search(r'bigWig', i[3]): #select bigWig files
            bigwig=i
            if re.search(r'NONE', bigwig[6]): #non-strand specific
                non_strand=bigwig
                if re.search(r'MultipleRawSignal', non_strand[4]): #Multiple 
                    non_strand_multiple=non_strand[2]
                    dict_non_strand['multiple'].append(non_strand_multiple)
                elif re.search(r'^RawSignal', non_strand[4]): #Unique
                    non_strand_unique=non_strand[2]
                    dict_non_strand['unique'].append(non_strand_unique)
            if re.search(r'MATE2_SENSE', bigwig[6]): #strand-specific
                strand=bigwig
                if re.search(r'Multiple', strand[4]): #Multiple 
                    strand_multiple=strand[2]
                    dict_strand['multiple'].append(strand_multiple)
                elif re.search(r'^Plus|Minus', strand[4]): #Unique
                    strand_unique=strand[2]
                    dict_strand['unique'].append(strand_unique)

#Set the destination: 
path_destination=" /users/rg/ramador/public_html/dme/UCSC_tracks/grape-nf-dm6.29"

if not os.path.exists(path_destination):
    print("Doesn't exist")


#Combine strand and non-strand specific bigwigs 
final_ouput=non_strand_bw+strand_bw

for i in final_ouput:
    cmd="cp "+i+path_destination
    print(cmd)
    os.system(cmd)


