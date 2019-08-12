### Written in Python.3.5:
import os
import sys
import re
import pandas as pd
import numpy as np
from random import randrange #generate a random integer

##### ---- The script starts ----

pipeline_db=sys.argv[1]

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

#We want the gene-expression in 'TPMs'
#We want the gene-expression in 'TPMs'
counter=0
for i in file_path:
    df_tmp=pd.read_csv(i, delimiter='\t')
    counter+=1
    df_tmp=df_tmp.loc[:,['gene_id', 'TPM']] #gene_id and gene-expression either 'TPMs' or 'Counts'
    exp_id=i.split('/')[-1].split('.')
    if len(exp_id) >= 4: # SampleID.replicate i.e. LWP.1, LWP.2, LWP.3, etc. 
        exp_id=i.split('/')[-1].split('.')[0:2]
        exp_id='.'.join(exp_id) #experiment id; pasted by a dot
    else: #unique identifier e.g. SRA_number: SRR1197316, SRR1197460, SRR1197371, etc.  
        exp_id= exp_id[0]
    df_tmp=df_tmp.rename(columns= {'TPM': exp_id})
    final_df=pd.merge(final_df, df_tmp, on='gene_id')
    print('{0}: {1}'.format(counter, exp_id))

output_name=sys.argv[2]

final_df.to_csv(output_name, sep='\t', index=False, header=True)

#Jupyter Notebook: /nfs/no_backup_isis/rg/ramador/D_me/RNA-seq/grape-nf-ERC/Python_scripts/generate.expression.df.ipynb
