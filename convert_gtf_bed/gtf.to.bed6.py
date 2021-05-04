import os
import sys
import re
import argparse

parser=argparse.ArgumentParser(description='Convert gtf file into bed6 file')

parser.add_argument("-g", "--gtf",
                    help="input gtf")
parser.add_argument("-o", "--output", default="output.bed6.bed",
                    help="output bed6 file; [default= %(default)s]")
parser.add_argument("-t", "--type", default="simple",
                    help="genomic feat either simple or verbose; [default= %(default)s]")


args=parser.parse_args()

def bed6_minimalInfo(input_gtf):
    final_minimal=[]
    with open(input_gtf, 'r') as gtf:
        for i in gtf:
            i=i.strip().split('\t')
            info=i[0:7]
            del info[1], info[4]            
            final_minimal.append(info)
    return final_minimal

def verbose_bed6info(input_gtf):
    final_verbose=[]
    with open(input_gtf, 'r') as gtf:
        for i in gtf:
            i=i.strip().split('\t')
            attribute=i[-1].split(';')[0].replace("gene_id \"", "").replace("\"", "")+"_"+i[2]
            info=i[0:7]
            del info[1], info[4], info[1]
            info.insert(1, attribute)
            final_verbose.append(info)
    return final_verbose

def save_results(info,output_name):
    with open(output_name, 'w') as out:
        for i in info:
            out.write(f'{i[0]}\t{i[2]}\t{i[3]}\t{i[1]}\t0\t{i[4]}\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    if args.type == "simple":
        bed_info=bed6_minimalInfo(input_gtf=args.gtf)
    elif args.type == "verbose":
        bed_info=verbose_bed6info(input_gtf=args.gtf)
    #save_results(info=bed_info, output_name=args.output)

