#!/usr/bin/env python

import argparse
import bioinfo as bio
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="isolate header files in a FASTA file")
    parser.add_argument("-i", "--indexes", help="Indexes file", type=str, required = True)
    parser.add_argument("-r1", "--read1_bio", help="read 1 fastq file biological read", type=str, required = True)
    parser.add_argument("-r2", "--read2_index", help="read 2 fastq file index read", type=str, required = True)
    parser.add_argument("-r3", "--read3_index", help="read 3 fastq file index read", type=str, required = True)
    parser.add_argument("-r4", "--read4_bio", help="read 4 fastq file biological read", type=str, required = True)
    parser.add_argument("-o", "--output_file", help="prints the summary of results from demultiplexing", type=str, required = True)
    return parser.parse_args()

parameters = get_args()
i = parameters.indexes
r1 = parameters.read1_bio
r2 = parameters.read2_index
r3 = parameters.read3_index
r4 = parameters.read4_bio
o = parameters.output_file

indexes = []
r1_storage = []
r2_storage = []
r3_storage = []
r4_storage = []
r1indexed_files={}
r2indexed_files={}
unmatched_total = 0
hopped_total = 0
indexed_total = 0
indexed = {}
hopped = {}



with open(i,"r") as fin:   #opens the file as fh
    for n,line in enumerate (fin):     #starts a for loop for each line in file f 
        line = line.strip('\n') 
        line = line.split("\t")
        indexes.append(line[4])
    indexes.pop(0)


for index in indexes:
    a = ("r1indexed/" + "r1" + index + "_" + index + ".fq" + ".gz")
    b = ("r2indexed/" + "r2" + index + "_" + index + ".fq" + ".gz")
    r1indexed_files[index] = gzip.open (a, "wt")
    r2indexed_files[index] = gzip.open (b, "wt")



Leslie_count = 0
with gzip.open (r1, "rt") as r1in, gzip.open (r2, "rt") as r2in, gzip.open (r3, "rt") as r3in, gzip.open (r4, "rt") as r4in, gzip.open ("r1unmatched.fq.gz", "wt") as r1unmatched, gzip.open ("r2unmatched.fq.gz", "wt") as r2unmatched, gzip.open ("r1index_hopped.fq.gz", "wt") as r1index_hopped, gzip.open ("r2index_hopped.fq.gz", "wt") as r2index_hopped:
    while True:     #starts a for loop for each line in file f 
        Leslie_count += 1
        r1_storage=[r1in.readline().strip(),r1in.readline().strip(),r1in.readline().strip(),r1in.readline().strip()]
        # print("r1", r1_storage)
        if r1_storage==["","","",""]:
            break
        r2_storage=[r2in.readline().strip(),r2in.readline().strip(),r2in.readline().strip(),r2in.readline().strip()]
        # print("r2" , r2_storage)
        r3_storage=[r3in.readline().strip(),r3in.readline().strip(),r3in.readline().strip(),r3in.readline().strip()]
        # print("r3" , r3_storage)
        r4_storage=[r4in.readline().strip(),r4in.readline().strip(),r4in.readline().strip(),r4in.readline().strip()]
        # print("r4" , r4_storage)
        # print (r2_storage[1], bio.rev_comp(r3_storage[1]))
        i1 = r2_storage[1]
        i1_phredscores = r2_storage [3]
        i2 = bio.rev_comp(r3_storage[1])
        i2_phredscores = r3_storage [3]

        r1header = r1_storage[0]
        r2header = r4_storage[0]

        r1seq =r1_storage[1]
        r2seq = r4_storage[1]

        r1thirdline = r1_storage[2]
        r2thirdline = r4_storage[2]

        r1phred_score = r1_storage[3]
        r2phred_score = r4_storage[3]

        # r1phred_scores = []
        # for scores in i1_phredscores:
        #     r1phred_scores.append(bio.convert_phred (scores))
        # print (r1phred_scores)

        # r2phred_scores = []
        # for scores in i2_phredscores:
        #     r2phred_scores.append(bio.convert_phred (scores))
        # print (r2phred_scores)

        if "N" in i1 or "N" in i2:
            # print ("unmatched")
            unmatched_total += 1
            for items in r1_storage:
                print(items, file=r1unmatched)
            for items in r4_storage:
                print (items,file=r2unmatched)
        elif i1 in indexes and i2 in indexes:
            if i1 == i2:
                indexed_total+=1
                if (i1,i2) in indexed:
                    indexed[i1,i2] += 1
                    print(r1header, i1,i2, file=r1indexed_files[i1])
                    print(r1seq, file=r1indexed_files[i1])
                    print(r1thirdline, file=r1indexed_files[i1])
                    print(r1phred_score, file=r1indexed_files[i1])
                    print(r2header, i1,i2, file=r2indexed_files[i1])
                    print(r2seq, file=r2indexed_files[i1])
                    print(r2thirdline, file=r2indexed_files[i1])
                    print(r2phred_score, file=r2indexed_files[i1])
                else:
                    indexed[i1,i2] = 1
                # print('indexed')
                #for items in r1_storage:
                    print(r1header, i1,i2, file=r1indexed_files[i1])
                    print(r1seq, file=r1indexed_files[i1])
                    print(r1thirdline, file=r1indexed_files[i1])
                    print(r1phred_score, file=r1indexed_files[i1])
                    print(r2header, i1,i2, file=r2indexed_files[i1])
                    print(r2seq, file=r2indexed_files[i1])
                    print(r2thirdline, file=r2indexed_files[i1])
                    print(r2phred_score, file=r2indexed_files[i1])
            else:
                hopped_total+=1
                if (i1,i2) in hopped:
                    hopped[(i1,i2)] += 1
                else:
                    hopped[(i1,i2)] = 1
                print(r1header, i1,i2, file=r1index_hopped)
                print(r1seq, file=r1index_hopped)
                print(r1thirdline, file=r1index_hopped)
                print(r1phred_score, file=r1index_hopped)
                print(r2header, i1,i2, file=r2index_hopped)
                print(r2seq, file=r2index_hopped)
                print(r2thirdline, file=r2index_hopped)
                print(r2phred_score, file=r2index_hopped)
                # print ("index hopped")
                # for items in r1_storage:
                #     print(items, file=r1index_hopped)
                # for items in r4_storage:
                #     print (items,file=r2index_hopped)

with open (o,"w") as fout:
    print ("Demultiplexing Summary Report", file = fout)
    print ("\n","total index hops", "\t", "total indexed reads", "\t", "total unmatched reads",file = fout)
    print (hopped_total, "\t", indexed_total, "\t", unmatched_total,file = fout)
    print ("\n","total reads per index",file = fout)
    for index in indexed:    
        print (str((index[0], index[1])).replace("'","").replace(" ",""),indexed[index],file = fout)
    print ("\n", "index hops",file = fout)
    for hop in hopped:    
        print (str((hop[0], hop[1])).replace("'","").replace(" ",""),hopped[hop],file = fout)
    index_perc = {}
    for index in indexed:
        index_perc[index] = ((indexed[index])/indexed_total)*100
    print ("\n", "percentage of reads per index pair",file= fout)
    for perc in index_perc:
        print (str(perc).replace("'","").replace(" ",""), index_perc[perc], "%",  file = fout) 