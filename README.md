sgRNA analysis pipeline
===
# STEP1 constant sequences of flanking sgRNA sequences
'''
##cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_minus_Rep1_end.fastq CXCR4_minus_Rep1.fastq\n
##cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_minus_Rep2_end.fastq CXCR4_minus_Rep2.fastq\n
##cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_minus_Rep3_end.fastq CXCR4_minus_Rep3.fastq\n
##cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_plus_Rep1_end.fastq CXCR4_plus_Rep1.fastq 
##cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_plus_Rpe2_end.fastq CXCR4_plus_Rpe2.fastq 
##cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_plus_Rpe3_end.fastq CXCR4_plus_Rpe3.fastq 
'''
'''
##cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_minus_Rep1_start.fastq CXCR4_minus_Rep1_end.fastq 
##cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_minus_Rep2_start.fastq CXCR4_minus_Rep2_end.fastq 
##cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_minus_Rep3_start.fastq CXCR4_minus_Rep3_end.fastq 
##cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_plus_Rep1_start.fastq CXCR4_plus_Rep1_end.fastq 
##cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_plus_Rpe2_start.fastq CXCR4_plus_Rpe2_end.fastq 
##cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_plus_Rpe3_start.fastq CXCR4_plus_Rpe3_end.fastq 
'''
# SETP2 MAGeCK 
  
  

