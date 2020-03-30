
# coding: utf-8

# # Final analysis of maf files
# ## You obtain the number of species, specie names and number of sequences aligned
# ### March 8th 2019

# In[9]:


#Libraries: 

import re, os, sys
from Bio import AlignIO
import numpy as np
import pandas as pd


# In[10]:


def Select_highest_score(MAF_file):
    
    """This function outputs an integer that select the highest score of a maf file"""
    
    total_score= []
    with open(MAF_file, 'r') as MAF_file:
        for i in MAF_file.readlines():
            i= i.rstrip().split('\t')
            if re.search(r'score=', i[0]):
                score= [float(j.split('=')[1]) for j in i]
                total_score.append(score)
    max_index= total_score.index(max(total_score))
    
    return int(max_index)


# In[11]:


def Obtain_NumberName_sp_Aligseq(maf_file):
    
    """This function returns a list that contains the number, name of species and the number of
    aligned sequences"""
    
    Max_Index= Select_highest_score(MAF_file= maf_file)
    
    iteratior=-1
    Iterator=[]; Number_species=[]; Aligned_bases=[]; Specie_names=[]
    for MAF_file in AlignIO.parse(maf_file, 'maf'):
        number_species=[]; aligned_bases= []; specie_names= []
        iteratior += 1
        Iterator.append(iteratior)
        
        for j in MAF_file:
            tmp_num_species= j.annotations['start']
            tmp_aligned_bases= j.annotations['size']
            tmp_species_name= j.id
            tmp_species_name= tmp_species_name.split('.')[0]
            tmp_species_name= re.sub('\d', '', tmp_species_name)
            number_species.append(tmp_num_species)
            aligned_bases.append(tmp_aligned_bases)
            specie_names.append(tmp_species_name)
        
        number_species= len(number_species)
        aligned_bases= np.average( [float(i) for i in aligned_bases]) #Aligned bases: mean
        specie_names= specie_names[1:]
        specie_names.insert(0, 'D_me')
        na_numAd= 27-number_species #Multiple alignment with 27 species
        specie_names= specie_names+['na']*na_numAd
        
        Number_species.append(number_species)
        Aligned_bases.append(aligned_bases)
        Specie_names.append(specie_names)
        
    np_species= np.array(Specie_names)
    Final_np= np.column_stack((Iterator, Number_species, Aligned_bases, np_species))
    Final_np= Final_np[ Max_Index ,:]
    Final_np= Final_np.tolist()
    
    return Final_np


# ## Start the script

# In[12]:


os.chdir('/users/rg/ramador/D_me/RNA-seq/Conservation.Analysis/Alignment_files/217_lncRNA_DGE/')

FINAL_OUT=[]
tmp= 0
for folder in os.listdir('Results_2/'):
    folder_path= 'Results_2/'+folder+'/'
    for file in os.listdir(folder_path):
        file_path= folder_path+file
        file_output= Obtain_NumberName_sp_Aligseq(file_path)
        tmp += 1
        FINAL_OUT.append(file_output)

pd_Final= pd.DataFrame(np.array(FINAL_OUT).reshape(len(FINAL_OUT), 30))


# In[28]:


##### Match the Gene_ID: 

Gene_ID= []
for folder in os.listdir('Results_2/'):
    folder_path= 'Results_2/'+folder+'/'
    for file in os.listdir(folder_path):
        file_path= folder_path+file
        file_path= file_path.split('/')[-1]
        file_path= file_path.split('_')[0]
        Gene_ID.append(file_path)
        

Gene_ID= pd.DataFrame(np.array(Gene_ID).reshape(len(Gene_ID), 1))


# In[34]:



pd_Final= pd.concat([Gene_ID.reset_index(drop= True), pd_Final], axis= 1)

#Save the results: 
pd_Final.to_csv('Table_OUTPUT/Alignments.output.table', sep= '\t', header=False, index= False)


# In[227]:


tmp


# ## END

# In[ ]:











# In[218]:


os.chdir('/users/rg/ramador/D_me/RNA-seq/Conservation.Analysis/Alignment_files/217_lncRNA_DGE/')

tmp= 0
for folder in os.listdir('Results_2/'):
    folder_path= 'Results_2/'+folder+'/'
    for file in os.listdir(folder_path):
        file_path= folder_path+file
        tmp += 1
        print("{}\t{}".format(tmp, file_path))

