#!/bin/awk -f 

##Print a specific interval of fields: 

BEGIN {FS="\t"}
{
    s=""

    for (i=start; i<=end; i++){ 

	s= s $i "\t"
    }

    print s 
}
