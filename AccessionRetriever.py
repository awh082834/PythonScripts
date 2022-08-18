#!/usr/bin/python

import sys
import os.path

isolateFile = sys.argv[1]
temp = isolateFile.split('-results')
isolateNum = temp[0].split('/')[2]
inLine = False
print "Now on: " + str(isolateNum)
exists = os.path.exists('PlasmidList.txt')
with open(isolateFile,'r') as infile:
    if exists==False:
        print "PlasmidList does not exist, will create it"

    for line in infile:
        if 'PLASMID CLUSTER' in line:
            inLine = True
            plasmidLine = infile.next()
            splitLine = plasmidLine.split("\t")
            accessionNum = str(splitLine[5].split(" ")[0])
            accessionNum = accessionNum.replace(">","")
            outfile = open('PlasmidList.txt','a')
            outfile.write(isolateNum+ "\t" + accessionNum +"\n")
            outfile.close()
    print "done"
