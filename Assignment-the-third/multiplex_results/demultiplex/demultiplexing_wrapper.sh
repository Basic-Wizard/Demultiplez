#!/bin/bash

#SBATCH --partition=bgmp       ### Partition (like a queue in PBS)
#SBATCH --job-name=demultiplexing    ### Job Name
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --cpus-per-task=1     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp     ### Account used for job submission

 ./demultiplexing.py -i indexes.txt  -r1 ../../../shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -r2 ../../../shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz -r3 ../../../shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz -r4 ../../../shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -o demultiplex_summary.txt

