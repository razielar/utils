# # Synthenic conservation
# ## Synthenic conservation between *D_me* and *D_pse*, *D_yak* and *D_sim*
# ### March 11th 2019

#Libraries: 

import sys, re, os


# ## Functions:

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
                if row1 == row2[1]: #Column_2 from OrthoParalogs output
                    mylist.append(row2[4]) #myID_N
                    matched=matched+1
                    found=1
                    break
            if string=='D_yak':
                if row1== row2[2]: #D_yak
                    mylist.append(row2[4])
                    matched=matched+1
                    found=1
                    break
            if string=='D_sim': #D_sim
                if row1== row2[3]: #Column_4 from OrthoParalogs output
                    mylist.append(row2[4])
                    matched=matched+1
                    found=1
                    break
                    
        if found == 0:
            nonmatched=nonmatched+1
            if nonMatch == 'yes':
                mylist.append(row1)
        found=0
        
    print("number of matched IDs for",string,": " ,matched)
    print("number of NON matched IDs for",string,": " ,nonmatched)
    print("number of candidate lncRNA",string,": " ,lncRNA,"\n")
    return mylist


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


def comparingDict(sp1, sp2):
    
    """This function returns a list that compares dictionaries from dictionaryOfClusters() for two species;
    if the number of shared genes is >= minOverlap, lncRNA are stored in myHomologs list"""
    
    if sp1 =='D_me':
        dict1= dictionaryOfClusters(Dme_idx, DmeList)
    if sp1 =='D_pse':
        dict1= dictionaryOfClusters(Dpse_idx, DpseList)
    if sp1=='D_yak':
        dict1= dictionaryOfClusters(Dyak_idx, DyakList)
    if sp1=='D_sim':
        dict1= dictionaryOfClusters(Dsim_idx, DsimList)
        
    if sp2 =='D_me':
        dict2= dictionaryOfClusters(Dme_idx, DmeList)
    if sp2 =='D_pse':
        dict2= dictionaryOfClusters(Dpse_idx, DpseList)
    if sp2=='D_yak':
        dict2= dictionaryOfClusters(Dyak_idx, DyakList)
    if sp2=='D_sim':
        dict2= dictionaryOfClusters(Dsim_idx, DsimList)
            
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


########################################################################## Start the script: ############################################################################

os.chdir('/users/rg/ramador/D_me/RNA-seq/Conservation.Analysis/Synteny/Synthenic_Drosophila_species/D.me_D.pse_D.yak_D.sim/Synteny/')

in1= 'Gene_list/dme_geneorder.list.txt'
in2= 'Gene_list/dpse.gene.order.list.txt'
in3= 'Gene_list/dyak.gene.order.list.txt' 
in4= 'Gene_list/dsim.gene.order.list.txt' 
in5= 'Orthologs.Using.control.txt'

genesNearby= int(3)     # considered genes located nearby a given lncRNA
minOverlap= int(3)      # minimum number of total shared genes
minSideOverlap= int(1)  # minimum shared genes at each side
nonMatch = 'yes'
temp= open('tmp_files/Synteny.3.3.1.tmp.txt', 'w')

# in1= sys.argv[1] #gene order list for sp1
# in2= sys.argv[2] #gene order list for sp2
# in3= sys.argv[3] #gene order list for sp3
# in4= sys.argv[4] #gene order list for sp4
# in5= sys.argv[5] #orthology file
# out= open(sys.argv[6] , 'w') #out file
# genesNearby= int(sys.argv[7])
# minOverlap= int(sys.argv[8])
# minSideOverlap= int(sys.argv[9])
# nonMatch = sys.argv[10]
# temp= open('temp', 'w')


##### 1) Apply the first function

DmeList=recodeList(in1, in5, 'D_me')

DpseList= recodeList(in2, in5, 'D_pse')

DyakList= recodeList(in3, in5, 'D_yak')

DsimList= recodeList(in4, in5, 'D_sim')

##### 2) Save a temporary file: 

for i in DmeList:
    temp.write("%s\tD_mel\n" %(i))

for i in DpseList:
    temp.write("%s\tD_pse\n" %(i))

for i in DyakList:
    temp.write("%s\tD_yak\n" %(i))

for i in DsimList:
    temp.write("%s\tD_sim\n" %(i))


##### 3) Obtain the location of lncRNAs: 

Dme_idx= [ i for i, item in enumerate(DmeList) if item.startswith('lncRNA_') ]
Dpse_idx= [i for i, item in enumerate(DpseList) if item.startswith('lncRNA_') ]
Dyak_idx= [i for i, item in enumerate(DyakList) if item.startswith('lncRNA_') ]
Dsim_idx= [i for i, item in enumerate(DsimList) if item.startswith('lncRNA_') ]


##### 4) Syntheny analysis 

out= open('Results/Synteny_3.3.1.txt' , 'w') #out file

#Find Synteny among Genomes

### 1:

for x in comparingDict('D_me','D_pse'):
    out.write('D_me\tD_pse\t%s\n'% ('\t'.join(x)))

for x in comparingDict('D_me', 'D_yak'):
    out.write('D_me\tD_yak\t%s\n'% ('\t'.join(x)))

for x in comparingDict('D_me', 'D_sim'):
    out.write('D_me\tD_sim\t%s\n'% ('\t'.join(x)))
    
### 2:

for x in comparingDict('D_pse','D_me'):
    out.write('D_pse\tD_me\t%s\n'% ('\t'.join(x)))

for x in comparingDict('D_yak', 'D_me'):
    out.write('D_yak\tD_me\t%s\n'% ('\t'.join(x)))
    
for x in comparingDict('D_sim', 'D_me'):
    out.write('D_sim\tD_me\t%s\n'% ('\t'.join(x)))


#################################################### END
