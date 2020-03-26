#!/bin/bash

### Convert the rows into columns and count them 

awk 'BEGIN{FS=OFS=","
	 print "\n", "Row to Columns script:",  "\n", "----------------------", "\n"}

	{
		
		for(i=1; i<=NF; i++){

			print i, $i

			}

	} 

	END{print "\n", "End of the script", "\n", "-----------------", "\n"}' 









