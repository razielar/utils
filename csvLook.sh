#!/bin/bash

# Look csv files on the terminal
csvLook ()
{
    if [[ -f "$1" ]] && [[ "$1" == *.csv ]] ; then
	column -t -s ',' "$1" | less -S
    else
	echo "'$1' file not found"
    fi
}

