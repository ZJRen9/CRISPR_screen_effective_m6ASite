sgRNA analysis pipeline
=====

STEP1 constant sequences of flanking sgRNA sequences
---

    cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_minus_Rep1_end.fastq CXCR4_minus_Rep1.fastq
    cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_minus_Rep2_end.fastq CXCR4_minus_Rep2.fastq
    cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_minus_Rep3_end.fastq CXCR4_minus_Rep3.fastq
    cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_plus_Rep1_end.fastq CXCR4_plus_Rep1.fastq
    cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_plus_Rpe2_end.fastq CXCR4_plus_Rpe2.fastq
    cutadapt -j 6 -q 10 -g GGACGAAACACCG -o CXCR4_plus_Rpe3_end.fastq CXCR4_plus_Rpe3.fastq
    
    
    cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_minus_Rep1_start.fastq CXCR4_minus_Rep1_end.fastq
    cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_minus_Rep2_start.fastq CXCR4_minus_Rep2_end.fastq
    cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_minus_Rep3_start.fastq CXCR4_minus_Rep3_end.fastq
    cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_plus_Rep1_start.fastq CXCR4_plus_Rep1_end.fastq
    cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_plus_Rpe2_start.fastq CXCR4_plus_Rpe2_end.fastq
    cutadapt -j 6 -q 10 -a GTTTTAGAGCTAG -o CXCR4_plus_Rpe3_start.fastq CXCR4_plus_Rpe3_end.fastq

STEP2 MAGeCK count
---
    mageck count -l m6A_base_editing_lib_modify.csv -n H1_ABE_m6A_modify --sample-label CXCR4minus_Rep1,CXCR4minus_Rep2,CXCR4minus_Rep3,CXCR4plus_Rep1,CXCR4plus_Rpe2,CXCR4plus_Rpe3 --fastq CXCR4minus_Rep1.fastq CXCR4minus_Rep2.fastq CXCR4minus_Rep3.fastq CXCR4plus_Rep1.fastq CXCR4plus_Rpe2.fastq CXCR4plus_Rpe3.fastq

STEP3 MAGeCK test
---
    mageck test -k H1_ABE_m6A_modify.count.txt -t CXCR4plus_Rep1,CXCR4plus_Rpe2,CXCR4plus_Rpe3 -c CXCR4minus_Rep1,CXCR4minus_Rep2,CXCR4minus_Rep3 -n H1_ABE_m6A_modify_change

STEP4 medium log2-foldchange count and min counts cutoff
---
    python medium_log2foldchange.py --mageck_test_sgrna_summary_result H1_ABE_m6A_modify_change.sgrna_summary.txt --mageck_count_normalized_result H1_ABE_m6A_modify.count_normalized.txt --min_depth 200 --output_file H1_ABE_m6A_modify_change.sgrna_summary_with_medium_lfc.txt
  

