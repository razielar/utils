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
                    help="Add type of analysis either 'gene', 'transcript' or 'exon' [default=%(default)s]", default="gene")

args=parser.parse_args()
output_name=args.output 

if args.type == "gene":

    print("\n")
    print("---- GTF analysis based on:",args.type,"----","\n")
    
    count=0
    final=[['Gene_ID', 'Gene_Name', 'Gene_Type', 'Length', 'Strand']]
    with open(args.input, 'r') as gtf:
        for i in gtf:
            i= i.rstrip().split('\t')
            if re.search(r'gene', i[2]):
                count += 1
                length=int(i[4])-(int(i[3])+1)+int(1)
                strand=i[6]
                gene_info=i[-1].split(';')[0:5]
                gene_name=[gene_info[i].strip().replace('"','').split(' ')[1] for i in range(len(gene_info))][0:2]
                gene_type=[gene_info[i].strip().replace('"', '').split(' ')[2] for i in range(len(gene_info)) if gene_info[i].startswith(' gene_type')]
                gene=gene_name+gene_type
                gene.extend([length, strand])
                final.append(gene)

    with open(output_name, 'w') as output:
        for i in final:
            output.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(i[0],i[1],i[2],i[3],i[4]))

elif args.type == "transcript":

    print("\n")
    print("---- GTF analysis based on:",args.type,"----","\n")
    
    count=0
    final=[['Gene_ID', 'Gene_Name', 'Transcript_ID', 'Transcript_Name' ,'Gene_Type', 'Length', 'Strand']]
    with open(args.input, 'r') as gtf:
        for i in gtf:
            i= i.rstrip().split('\t')
            if re.search(r'transcript', i[2]):
                count += 1
                length=int(i[4])-(int(i[3])+1)+int(1)
                strand=i[6]
                gene_info=i[-1].split(';')[0:5]
                gene_name=[gene_info[i].strip().replace('"','').split(' ')[1] for i in range(len(gene_info))][:-1]
                gene_type=[gene_info[i].strip().replace('"', '').split(' ')[2] for i in range(len(gene_info)) if gene_info[i].startswith(' gene_type')]
                gene=gene_name+gene_type
                gene.extend([length, strand])
                final.append(gene)
                
    with open(output_name, 'w') as output:
        for i in final:
            output.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))


elif args.type == "exon":

    print("\n")
    print("---- GTF analysis based on:",args.type,"----","\n")

    count=0
    final=[['Gene_ID', 'Gene_Name', 'Transcript_ID', 'Transcript_Name',
            'Gene_Type', 'Genomic_Feature', 'Length', 'Strand']]
    with open(args.input, 'r') as gtf:
        for i in gtf:
            i=i.strip().split('\t')
            if re.search(r'exon', i[2]):
                count += 1
                length=int(i[4])-(int(i[3])+1)+int(1)
                strand=i[6]
                feature=i[2]
                exon=i
                gene_info=i[-1].split(';')[0:5]
                gene_name=[gene_info[i].strip().replace('"','').split(' ')[1] for i in range(len(gene_info))][:-1]
                gene_type=[gene_info[i].strip().replace('"', '').split(' ')[2] for i in range(len(gene_info)) if gene_info[i].startswith(' gene_type')]
                gene=gene_name+gene_type
                gene.extend([feature,length, strand])
                final.append(gene)

    with open(output_name, 'w') as output:
        for i in final:
            output.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))




