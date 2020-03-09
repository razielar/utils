#!/usr/bin/env python


# # Final analysis: Orthology relationship in *D_me*
# ## Script to create a file including all orthology relationship for the 4 fly species 
# ### February 19th 2019
# Written in **Python 3.5.4** <br>
# D.melanogaster comparing: D. sechelia (close), D. persimilis (halfway) and D. willistoni (far away)

#Libraries: 
import re, sys

##### 1) Input data:

file_gene_list = open(sys.argv[1] , 'r') #Gene_list
in2 = sys.argv[2] #Orthologs list
out= open(sys.argv[3], 'w') #Output
out.write('D_me\tD_sechelia\tD_persimilis\tD_willistoni\tmyID\n')

##### 2) Analyze the gene list:

gene_list = []
for i in file_gene_list.readlines():
    gene_list.append(i.rstrip())

##### 3) Grab the genes from the other fly species:

dictOrt={}
new=0; sec=0; per=0; wil=0
ort= {'sec': [], 'per': [], 'wil': []} #temporary directory
for i in open(in2, 'r').readlines():
    i = i.rstrip().split('\t')
    if re.search(r'FBgn', i[0]):
        key= i[0]
        if not key in dictOrt:
            dictOrt[key]= ort
            new= 1
        if re.search(r'Dsec', i[6]): #Grab this specie
            dictOrt[key]['sec'].append(i[5]) #Take the Gene_ID
            sec= 1
        if re.search(r'Dper', i[6]):
            dictOrt[key]['per'].append(i[5])
            per= 1
        if re.search(r'Dwil', i[6]):
            dictOrt[key]['wil'].append(i[5])
            wil=1
        if new == 1:
            if sec == 0:
                dictOrt[key]['sec'].append('na')
            if per == 0:
                dictOrt[key]['per'].append('na')
            if wil == 0:
                dictOrt[key]['wil'].append('na')
            ort= {'sec': [], 'per': [], 'wil': []}
            new=0; sec=0; per=0; wil=0

if sec == 0: 
    dictOrt[key]['sec'].append('na')
if per == 0:
    dictOrt[key]['per'].append('na')
if wil == 0:
    dictOrt[key]['wil'].append('na')

##### 4) Print the Paralogs

myID=1
for x in gene_list:
    for key, j in dictOrt.items():
        if x == key:
            length= [len(j['sec']), len(j['per']), len(j['wil'])]
            mymax= max(length)
            i= 0
            while i < mymax:
                try:
                    sec= j['sec'][i]
                except IndexError:
                    pass
                try:
                    per= j['per'][i]
                except IndexError:
                    pass
                try:
                    wil= j['wil'][i]
                except IndexError:
                    pass
                out.write('%s\t%s\t%s\t%s\tmyID%s\n' % (key, sec, per, wil, myID))
                i= i+1
            myID= myID+1


#####
