#!/usr/bin/env python 

### Move bigwig files to a specific path 
import os
import sys 
import re
import argparse

parser=argparse.ArgumentParser(description='Move bigWig files from pipeline.db grape-nf')

parser.add_argument("-i", "--input",
                    help="pipeline.db obtained from grape-nf")
parser.add_argument("-p", "--path",
                    help="folder where you want to move bigWig files")

args=parser.parse_args()

pipeline_db=args.input
path_destination=args.path 

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


# --- 1) Unique: combine strand and non-strand specific bigwigs
final_unique=dict_non_strand['unique']+dict_strand['unique']

for i,j in enumerate(final_unique):
    cmd="cp "+ j+ " "+ path_destination
    print("{0}: {1}".format(i,cmd))
    os.system(cmd)

# --- 2) Multiple: combine strand and non-strand specific bigwigs
path_destination=" /users/rg/ramador/public_html/dme/UCSC_tracks/grape-nf-dm6.29/multiple"
final_multiple=dict_non_strand['multiple']+dict_strand['multiple']

for i,j in enumerate(final_multiple):
    cmd="cp "+ j+ " "+ path_destination
    print("{0}: {1}".format(i, cmd))
    os.system(cmd)



