#!/usr/bin/python

import sys
import os.path
#Assembly Filename
assemFile = sys.argv[1]
#Name of output file
outfileName = "IsolatedContigs.fasta"
notFirstContig = False
try:
    with open(assemFile, 'r') as infile:
        lines = infile.readlines()

        #Tracks overall contig number
        ContigNum = 0

        #Tracks circular contig number
        circContigNum = 0
        for line in lines:

            #Checks for header identifier
            if '>' in line:
                ContigNum += 1

                #If the contig is circular and not the first contig 
                #(This assumes that the first circular contig is the chromosomal sequence, we are looking for MGEs or plasmids.)
                if 'circular=true' in line and  ContigNum != 1:

                    #Will only count circular contigs other than circular chromosomal sequence
                    circContigNum += 1

                    #Flags that program is past the first contig
                    notFirstContig = True
                    
                    #Begins writing to output fasta
                    outfile = open(outfileName,'a')
                    outfile.write(line)
                    
            elif notFirstContig == True:
                outfile.write(line)
        outfile.close()
        print(str(circContigNum) + " contig(s) have been found to be circularized and were isolated from main chromosomal sequence or rest of assembly. \nThese were output to IsolatedContigs.fasta")
except:
    print("Assembly file does not exist.")