
import os
import sys
import re
import pandas as pd
import numpy as np
from random import randrange #generate a random integer 

pipeline_db= 'pipeline.db'

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
counter=0
for i in file_path:
    df_tmp=pd.read_csv(i, delimiter='\t')
    counter+=1
    df_tmp=df_tmp.loc[:,['gene_id', 'TPM']] #gene_id and gene-expression in 'TPMs'
    exp_id=i.split('/')[-1].split('.')[0:2]
    exp_id='.'.join(exp_id) #experiment id; pasted by a dot
    df_tmp=df_tmp.rename(columns= {'TPM': exp_id})
    final_df=pd.merge(final_df, df_tmp, on='gene_id')
    print('{0}: {1}'.format(counter, exp_id))

