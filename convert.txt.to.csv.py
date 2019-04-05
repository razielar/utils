
import sys, os, re
import numpy as np
import pandas as pd
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help= "By default the 'stdin' is the input file",
                   default= sys.stdin)
parser.add_argument("-o", "--output", default= "Output.txt.to.csv",
                   help= "Output file name, must have a 'csv' extension (e.g. What.ever.csv) [default= %(default)s]")
# parser.add_argument("-h", "--header", default= 'infer',
#                    help= "By default the column name is included: 'infer', but if there is no column name then 'None' [default= %(default)s]")


args= parser.parse_args()

input_txt= pd.read_csv(sys.stdin, sep= '\t', header= 'infer')

input_txt.to_csv(args.output , index= False, header= True)


# Jupyter notebook: /users/rg/ramador/D_me/RNA-seq/Conservation.Analysis/Synteny/D.me_D.pse_D.yak_D.sim/Synteny/Python_scripts


