#!/usr/bin/env python

import os, sys, re
import argparse

# GTF files: 1-based; formula= end-start+1
# Bed files: 0-based
# http://genome.ucsc.edu/blog/the-ucsc-genome-browser-coordinate-counting-systems/

parser=argparse.ArgumentParser(description='Retrieve gene information from a gtf file')

parser.add_argument("-i", "--input",
                    help="The GTF file is the input")
parser.add_argument("-o", "--output", default="Gtf.analysis.tsv",
                    help="Output file name [default=%(default)s]")
parser.add_argument("-t", "--type",
                    help="Add type of analysis either Gene or Transcript [default=%(default)s]", default="Gene")

args=parser.parse_args()

if args.type == "Gene":
    count=0
    final=[['Gene_ID', 'Gene_Name', 'Gene_Type', 'Length', 'Strand']]
    with open(args.input, 'r') as gtf:
        for i in gtf:
            i= i.rstrip().split('\t')
            if re.search(r'gene', i[2]):
                count += 1
                length=int(i[4])-(int(i[3])+1)
                strand=i[6]
                gene_info=i[-1].split(';')[0:5]
                gene_name=[gene_info[i].strip().replace('"','').split(' ')[1] for i in range(len(gene_info))][0:2]
                gene_type=[gene_info[i].strip().replace('"', '').split(' ')[2] for i in range(len(gene_info)) if gene_info[i].startswith(' gene_type')]
                gene=gene_name+gene_type
                gene.extend([length, strand])
                final.append(gene)

output_name=args.output 

with open(output_name, 'w') as output:
    for i in final:
        output.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(i[0],i[1],i[2],i[3],i[4]))

