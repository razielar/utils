#!/usr/bin/env python

### Written in Python.3.5:
import os, sys, re
import argparse 
import pandas as pd
import numpy as np
from random import randrange #generate a random integer

parser=argparse.ArgumentParser(description='Obtain matrix of: TPM, FPKM or Count from pipeline.db grape-nf')

parser.add_argument("-i", "--input",
                   help="pipeline.db obtained from grape-nf")
parser.add_argument("-o", "--output", default="output_grape.pipeline.tsv",
                    help="Name of the output file [default=%(default)s]")
parser.add_argument("-t", "--type", default="TPM",
                    help="What do you want: 'TPM', 'FPKM' or 'Count' [default=%(default)s]")

args=parser.parse_args()


##### ---- The script starts ----

# if len(sys.argv) < 3:
#     sys.exit("usage: python  generate.ExpressionMatrix.py  pipeline.db output.tsv")

pipeline_db=args.input
# pipeline_db=sys.argv[1]

file_path=[]
with open(pipeline_db, 'r') as pipeline_db:
    for i in pipeline_db:
        i = i.rstrip().split('\t')
        if re.search(r'GeneTxDir', i[4]): #Obtain the gene expression-matrix: 'GeneTxDir'
            tmp_file=i[2] #Obtain the file_path
            file_path.append(tmp_file)

#Read a random gene expression-matrix to obtain the gene_id            
random_int=randrange(0, len(file_path))
final_df=pd.read_csv(file_path[random_int], delimiter='\t')
final_df=final_df.loc[:,['gene_id']]

# expected_count
if args.type == "Count":
    args.type= "expected_count"

counter=0
for i in file_path:
    df_tmp=pd.read_csv(i, delimiter='\t')
    counter+=1
    df_tmp=df_tmp.loc[:,['gene_id', args.type]] #gene_id and gene-expression: 'TPM', 'FPKM' or 'Counts'
    exp_id=i.split('/')[-1].split('.')
    if len(exp_id) >= 4: # SampleID.replicate i.e. LWP.1, LWP.2, LWP.3, etc. 
        exp_id=i.split('/')[-1].split('.')[0:2]
        exp_id='.'.join(exp_id) #experiment id; pasted by a dot
    else: # Unique-Identifier e.g. SRA_number: SRR1197316, SRR1197460, SRR1197371, etc.  
        exp_id= exp_id[0]
    df_tmp=df_tmp.rename(columns= {args.type: exp_id})
    final_df=pd.merge(final_df, df_tmp, on='gene_id')
    print('{0}: {1}'.format(counter, exp_id))

# output_name=sys.argv[2]
output_name=args.output  

final_df.to_csv(output_name, sep='\t', index=False, header=True)

#Jupyter Notebook: /nfs/no_backup_isis/rg/ramador/D_me/RNA-seq/grape-nf-ERC/Python_scripts/generate.expression.df.ipynb
#Jupyter Notebook: /nfs/no_backup_isis/rg/ramador/D_me/RNA-seq/grape-nf-modENCODE/Python_scripts/Analyze.generate.ExpressionMatrix.py.ipynb 
