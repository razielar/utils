
# coding: utf-8

# # Obtain the promoters of lncRNAs 
# ## September 16th 2019
# ## Using a bed file obtain a window of 50, 100 and 200 bp

# In[1]:


import sys
import os


# In[2]:


os.chdir("/nfs/users2/rg/ramador/D_me/Data/Bed_files")


# In[20]:


bed_file= "lncRNA_DGE_0h/lncRNA.up.0h.bed"
window= 50

final_bed=[]
with open(bed_file, 'r') as bed_file:
    for i in bed_file:
        i = i.rstrip().split('\t')
        #Obtain the window
        var_1= int(i[1])-window
        var_2= int(i[1])+window
        i[1]= var_1
        i[2]=var_2
        final_bed.append(i)

## Save the results: 
output_name= "promoters.txt"


with open(output_name, 'w') as output:
    for i in final_bed:
        output.write("{0}\t{1}\t{2}\t{3}\n".format(i[0], i[1], i[2], i[3]))

