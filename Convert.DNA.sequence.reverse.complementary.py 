#!/usr/bin/env python

### This script uses Python3

########## Libraries: biopython 1.72

from Bio import SeqIO
from Bio.Seq import Seq
import sys
import argparse

##########

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help= "By default the 'stdin' is the input file", default= sys.stdin)
parser.add_argument("-o", "--output", default = "Output.reverse_complement.fasta",
    help= 'Output file name, must have a fasta extension (e.g. What.ever.fasta) [default= %(default)s]')

args = parser.parse_args()

########## Reverse complementary file:

reverse_complementary_file = ( i.reverse_complement(id=i.id, description= "reverse_complement") \
    for i in SeqIO.parse( args.input , "fasta"))

SeqIO.write(reverse_complementary_file, args.output , "fasta")
