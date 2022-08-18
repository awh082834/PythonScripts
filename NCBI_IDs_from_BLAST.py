#!/usr/bin/python

import sys
import os.path
temp = 0
blastOut = sys.argv[1]
with open(blastOut,'r') as infile:
	for line in infile:
		lineArray = line.split()
		if lineArray and '>' in lineArray[0]:
			outfile = open('BlastAccessionNum.txt','a')
        	    	outfile.write(lineArray[0].strip('>') +"\n")
	            	outfile.close()

