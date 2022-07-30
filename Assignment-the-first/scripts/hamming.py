#!/usr/bin/env python

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="isolate header files in a FASTA file")
    parser.add_argument("-f", "--input-file", help="file to run", type=str, required = True)
    parser.add_argument("-o", "--output-file", help="output file", type=str, required = True)
    return parser.parse_args()

parameters = get_args()
f = parameters.input_file
o = parameters.output_file

indexes = []
hammings = {}
total = 0
minh = 8
with open(f,"r") as fin, open(o,"w") as fout :   #opens the file as fh
    for n,line in enumerate (fin):     #starts a for loop for each line in file f 
        line = line.strip('\n') 
        line = line.split("\t")
        indexes.append(line[4])
    indexes.pop(0)
    for i in range(0,len(indexes)):
        for j in range(i+1,len(indexes)):
            for k in range (8):
                if indexes[i][k] != indexes[j][k]:
                    total+=1                    
            if total in hammings:
                hammings[total] += (((indexes[i],indexes[j])))
                total = 0
            else:
                hammings[total] = ((indexes[i],indexes[j]))
                total = 0
    for items in sorted(hammings):
        print (items, file=fout)
        print (hammings[items], file=fout)