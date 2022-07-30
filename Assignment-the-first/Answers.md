# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read 1 | 101 | -33 |
| 1294_S1_L008_R2_001.fastq.gz | index 1 | 8 | -33 |
| 1294_S1_L008_R3_001.fastq.gz | index 2 | 8 | -33 |
| 1294_S1_L008_R4_001.fastq.gz | read 2 | 101 | -33 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    ![r1_hist](https://user-images.githubusercontent.com/106283930/181871964-9635c112-47d8-4e9e-8745-a4913621dd4f.png)
    ![r2_hist](https://user-images.githubusercontent.com/106283930/181871966-9e995206-3339-4ba0-940d-f8d789e54d2c.png)
    ![r3_hist](https://user-images.githubusercontent.com/106283930/181871972-732d65ce-638a-482d-9512-b9bcd9804109.png)
    ![r4_hist](https://user-images.githubusercontent.com/106283930/181871975-3827866f-940c-44d7-875e-3e18e9abe411.png)

    2. Hard to say what the minimum quality score for this should be without knowing more about the job, I'd say 30 would be pretty good for both file types, one in a thousand bases at worst is pretty good, and for the indexes it would put at most 1 in a thousand indexes in the unmatched bin and have less than a 1 in a billion chance of being so incorrect as to appear as a different index. The minimum hamming distance in this index set is 3 so 3 of the bases would need to be wrong for it to be called as the wrong index but then it would also have to be the right positions of bases and they would all have to be exactly the right base

    3.  (base) [kraleigh@n278 2017_sequencing]$ zcat 1294_S1_L008_R2_001.fastq.gz | grep -A1 "@" | grep -v "^@" | grep -v "-" | grep "N" | wc -l
        
        3976613
        
        (base) [kraleigh@n278 2017_sequencing]$ zcat 1294_S1_L008_R3_001.fastq.gz | grep -A1 "@" | grep -v "^@" | grep -v "-" | grep "N" | wc -l
        
        3328051
    
## Part 2
1. Define the problem
 We need to open each file simultainiously and then isolate the first record of each file. then compare the indexes of the first record and sort it into one of 3 catagories: indexed, index hopped and unmatched. If the record is unmatched it can be sent to the unmatched FASTQ for each read with the unmatched indexes in the header. If the record shows an index hopped you will add it to the index hopped FASTQ file for each read. If the record fits into the indexed catagory you will need to add it to a FASTQ file for that index for each read or make a FASTQ file for that index for each read.
2. Describe output
you should have 48 indexed FASTQ files, 2 for each index (one per read), 2 index hopped FASTQ files, one for each read and 2 unmatched FASTQ files, one for each read. 
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
1. Description/doc string
demultiplexes multiplexed illumina reads and removes index hopped and unmatched reads 
2. Function headers (name and parameters) 
3. Test examples for individual functions
4. Return statement
