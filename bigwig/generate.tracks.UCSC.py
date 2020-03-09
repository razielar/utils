#!/usr/bin/env python

### Generate UCSC tracks
import os
import sys
import re
import argparse

parser=argparse.ArgumentParser(description='Generate UCSC tracks for copy/paste')

parser.add_argument("-p", "--path",
                    help="folder where bigwigs are saved use 'pwd'")
parser.add_argument("-m", "--metadata",
                    help="metadata tsv file to obtain: Name[4] and ID[0]")
parser.add_argument("-s", "--strand", default=False,
                    help="True if stranded rna-seq having + and - strand; [default= %(default)s]")
parser.add_argument("-d", "--description", default="",
                    help="Add some initial description, like: Unique; [default= %(default)s]")
parser.add_argument("-o", "--output", default="output.generate.track.UCSC.txt",
                    help="output name; [default= %(default)s]")


args=parser.parse_args()

### --- Input:
path=args.path 
metadata=args.metadata
strand=args.strand
output=args.output
description=args.description
### --- 

### --- Analysis:

path=path.split('/')[5:] #pwd
insert_elements=['public-docs.crg.es','rguigo','Data', 'ramador']
path=insert_elements+path
path="/".join(path)

final=[]
with open(metadata, 'r') as metadata:
    for i in metadata:
        i=i.strip().split('\t')
        metadata=i[0]+" "+i[4]
        metadata=metadata.split(' ')
        if not re.search(r'NA', metadata[1]): #use only with description
            desired=metadata
            final.append(desired)

final=final[1:] #remove header

### --- Save Results:
with open(output, 'w') as result:
    for i,j in enumerate(final):
        if strand:
            fir="track type=bigWig name=\"Unique_{0}\" description=\"A bigWig file\"".format(j[1])
            bigwig_file="bigDataUrl=https://{0}/{1}.Unique.raw.bw".format(path,j[0])
            ucsc_file=fir+" "+bigwig_file
            print("{0}: {1}".format(i,ucsc_file))
            result.write("{0}\n".format(ucsc_file))
        else:
            fir="track type=bigWig name=\"Unique_{0}\" description=\"A bigWig file\"".format(j[1])
            bigwig_file="bigDataUrl=https://{0}/{1}.Unique.raw.bw".format(path,j[0])
            ucsc_file=fir+" "+bigwig_file
            print("{0}: {1}".format(i,ucsc_file))
            result.write("{0}\n".format(ucsc_file))
            





