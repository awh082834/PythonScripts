#!/usr/bin/python

import sys
import os.path
#Assembly Filename
assemFile = sys.argv[1]
#Name of Contig: In the case of UniCycler, it would be 1, 2, 3, etc..
contigName = sys.argv[2]
#Name of output file
outfileName = sys.argv[3]
headerFound = False
secondHeaderFound = False
header = ">"+contigName
try:
    with open(assemFile, 'r') as infile:
        lines = infile.readlines()
        #If the user wants all contigs other than the first, presumably
        #chromosomal contig, this flag will grab all of them and 
        #add them to a new file.
        if contigName == "all":
            for line in lines:
                if secondHeaderFound:
                    outfile.write(line)
                #Looks for the second contig as that is the second
                #smallest, excluding the largest, the chromosomal contig
                if ">2" in line:
                    secondHeaderFound = True
                    outfile = open(outfileName, 'a')
                    outfile.write(line)
        else:
            for line in lines:
                if not headerFound:
                    #Checks for the header marker, and if the contig name
                    #matches. Opens the outfile, and writes the contig to it.
                    if header in line:
                        headerFound = True
                        outfile = open(outfileName,'a')
                        outfile.write(line)

                #if header has been found, subsequent lines will
                #be of the contig requested, so if > is not in the 
                #line, the line is added to the out file
                elif headerFound and ">" not in line:
                    outfile.write(line)
                
                #if header has been found, but a > is found again,
                #the loop has encountered a new contig, so it will 
                #not be added to the new file.
                elif headerFound and ">" in line:
                    outfile.close()
                    headerFound = False
except:
        #will return this if the assembly file does not exist
        print("Assembly File does not exist")    