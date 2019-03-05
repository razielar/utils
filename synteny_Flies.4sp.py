
# coding: utf-8

# # Synthenic-Families
# ## Synteny conservation among D_me and D_ana, D_pse and D_wil
# ### March 5th 2019
# ### Written in Python 3.5.4

# In[2]:


#Libraries: 

import sys, re, os


# ## Functions:

# In[3]:


def recodeList(file1, file2, string):
    
    """This function returns a list with the gene order of a given sp were geneIDs were renamed to myID
    to allow direct comparisson between species (genes with no homology are also included!)
    Ex: ['myID1', 'FBgn00xxxx' 'myID2', 'myID3', 'myID4', 'myID5','lncRNA_FBgn00xxxxx', 'myID6', ...]"""
     
    mylist = []
    matched=0; nonmatched=0; found=0; lncRNA=0
    for row1 in open(file1, 'r'):  #Ordered Gene_list 
        row1 = row1.rstrip()
        if re.search(r'lncRNA_', row1): #lncRNA_ is the tag that you want to classify according to synteny
            mylist.append(row1)
            found=1
            lncRNA=lncRNA+1
        for row2 in open(file2 , 'r').readlines(): #OrthoParalogs output: Flybase_orthoParalogs.py
            row2= row2.rstrip().split("\t")
            if string == 'D_me': #D_melanogaster
                if row1 == row2[0]: #Column_1 from OrthoParalogs output 
                    mylist.append(row2[4]) #myID_N
                    matched=matched+1
                    found=1
                    break
            if string == 'D_pse': #D_pse
                if row1 == row2[2]: #Column_3 from OrthoParalogs output
                    mylist.append(row2[4]) #myID_N
                    matched=matched+1
                    found=1
                    break
#             if string=='cbren':
#                 if row1== row2[3]:
#                     mylist.append(row2[4])
#                     matched=matched+1
#                     found=1
#                     break
#             if string=='crem':
#                 if row1== row2[1]:
#                     mylist.append(row2[4])
#                     matched=matched+1
#                     found=1
#                     break
                    
        if found == 0:
            nonmatched=nonmatched+1
            if nonMatch == 'yes':
                mylist.append(row1)
        found=0
        
    print("number of matched IDs for",string,": " ,matched)
    print("number of NON matched IDs for",string,": " ,nonmatched)
    print("number of candidate lncRNA",string,": " ,lncRNA,"\n")
    return mylist


# In[6]:


def dictionaryOfClusters(myidx,mylist):
    
    """This function returns a dictionary; for each lncRNA (key) stores the number of nearby renamed geneID
    indicated by the user. myidx= positions in myList for each lncRNA; myList= renamed gene order"""
  
    mydict={}
    for idx in myidx:
        key=mylist[idx]
        val={'left':[], 'right':[], 'all':[]}
        if not key in mydict:
            mydict[key]=val
        i=1
        while i <= genesNearby: #considered genes located nearby a given lncRNA
            try:
                if idx-i >=0:                 
                    mydict[key]['left'].append(mylist[idx-i])
                    mydict[key]['all'].append(mylist[idx-i])
                mydict[key]['right'].append(mylist[idx+i])                                   
                mydict[key]['all'].append(mylist[idx+i])
            except IndexError:
                pass
            i=i+1
            
    return mydict


# In[ ]:


def comparingDict(sp1, sp2):
    
    """This function returns a list that compares dictionaries from dictionaryOfClusters() for two species;
    if the number of shared genes is >= minOverlap, lncRNA are stored in myHomologs list"""
    
    if sp1 =='D_me':
        dict1= dictionaryOfClusters(Dme_idx, DmeList)
    if sp1 =='D_pse':
        dict1= dictionaryOfClusters(Dpse_idx, DpseList)
#     if sp1=='cbren':
#         dict1= dictionaryOfClusters(cbren_idx,cbrenList)
#     if sp1=='crem':
#         dict1= dictionaryOfClusters(crem_idx,cremList)
    if sp2 =='D_me':
        dict2= dictionaryOfClusters(Dme_idx, DmeList)
    if sp2 =='D_pse':
        dict2= dictionaryOfClusters(Dpse_idx, DpseList)
#     if sp2=='cbren':
#         dict2= dictionaryOfClusters(cbren_idx,cbrenList)
#     if sp2=='crem':
#         dict2= dictionaryOfClusters(crem_idx,cremList)
    myHomologs=[]
    homologFound='false'
    for key1, val1 in dict1.items():
        print(key1, val1)
        for key2, val2 in dict2.items():
            if len(set(dict1[key1]['all']).intersection(dict2[key2]['all'])) >= minOverlap: #In this case 3
            #at least one of the two lncRNA share genes in the left and the right side    
            #forces that both lncRNA share genes in the left and the right side    
                if len(set(dict1[key1]['right']).intersection(dict2[key2]['right'])) >= minSideOverlap: #case 1
                    if len(set(dict1[key1]['left']).intersection(dict2[key2]['left'])) >= minSideOverlap: 
                        homologFound='true'
                if len(set(dict1[key1]['right']).intersection(dict2[key2]['left'])) >=minSideOverlap:
                    if len(set(dict1[key1]['left']).intersection(dict2[key2]['right'])) >=minSideOverlap:
                        homologFound='true'
                if homologFound=='true':             
                        mytup=(key1,key2) 
                        myHomologs.append(mytup)
                        homologFound='false'
    return myHomologs


# ## Start the script: 

# ### Input files:

# In[ ]:


in1= sys.argv[1] #gene order list for sp1
in2= sys.argv[2] #gene order list for sp2
in5= sys.argv[3] #orthology file
out= open(sys.argv[4] , 'w') #out file

genesNearby= int(sys.argv[5])
minOverlap= int(sys.argv[6])
minSideOverlap= int(sys.argv[7])
nonMatch = sys.argv[8]
temp= open('temp', 'w')


# ### Apply the functions with *D_me*

# In[ ]:


#D_melanogaster

DmeList=recodeList(in1, in5, 'D_me')

for i in DmeList:
    temp.write("%s\tD_mel\n" %(i))
    


# **Enumerate:** allows us to loop over something and have an **automatic counter**. <br>
# In this case *i* is the counter. 

# In[ ]:


#We want the position of the lncRNAs: 
#i is the counter and it's printed

Dme_idx= [ i for i, item in enumerate(DmeList) if item.startswith('lncRNA_') ]


# ### Apply the functions with D_pse

# In[ ]:


DpseList= recodeList(in2, in5, 'D_pse')

for i in DpseList:
    temp.write('%s\tD_pse\n' %(i))

Dpse_idx= [i for i, item in enumerate(DpseList) if item.startswith('lncRNA_') ]


# ### Synteny analysis

# In[ ]:


#Find Synteny among Genomes

for x in comparingDict('D_me','D_pse'):
    out.write('D_me\tD_pse\t%s\n'% ('\t'.join(x)))

for x in comparingDict('D_pse','D_me'):
    out.write('D_pse\tD_me\t%s\n'% ('\t'.join(x)))

