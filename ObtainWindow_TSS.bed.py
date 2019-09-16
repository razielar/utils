import sys, os

if len(sys.argv) < 4:
    sys.exit("usage: python ObtainWindow_TSS.bed.py bed_file.bed window output.tsv")

### --- Parameters ---
bed_file= sys.argv[1]
window= sys.argv[2]
output_name= sys.argv[3]
### --- Parameters ---

### Starts:

final_bed=[]
with open(bed_file, 'r') as bed_file:
    for i in bed_file:
        i = i.rstrip().split('\t')
        #Obtain the window
        var_1= int(i[1])-int(window)
        var_2= int(i[1])+int(window)
        i[1]= var_1
        i[2]=var_2
        final_bed.append(i)

### Write the output:

with open(output_name, 'w') as output:
    for i in final_bed:
        output.write("{0}\t{1}\t{2}\t{3}\n".format(i[0], i[1], i[2], i[3]))
