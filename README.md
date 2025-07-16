#sgRNA design
=====
##STEP1 sequence abstract for sgRNA design
---
    sequence around single base m6A site abstract by bedtools getfasta
##STEP2 PAM sequence design
---
    python sgRNA_design.py
    

#sgRNA analysis pipeline
=====

##STEP1 constant sequences of flanking sgRNA sequences
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

##STEP2 MAGeCK count
---
    mageck count -l m6A_base_editing_lib_modify.csv -n H1_ABE_m6A_modify --sample-label CXCR4minus_Rep1,CXCR4minus_Rep2,CXCR4minus_Rep3,CXCR4plus_Rep1,CXCR4plus_Rpe2,CXCR4plus_Rpe3 --fastq CXCR4minus_Rep1.fastq CXCR4minus_Rep2.fastq CXCR4minus_Rep3.fastq CXCR4plus_Rep1.fastq CXCR4plus_Rpe2.fastq CXCR4plus_Rpe3.fastq

##STEP3 MAGeCK test
---
    mageck test -k H1_ABE_m6A_modify.count.txt -t CXCR4plus_Rep1,CXCR4plus_Rpe2,CXCR4plus_Rpe3 -c CXCR4minus_Rep1,CXCR4minus_Rep2,CXCR4minus_Rep3 -n H1_ABE_m6A_modify_change

##STEP4 medium log2-foldchange count and min counts cutoff
---
    python medium_log2foldchange.py --mageck_test_sgrna_summary_result H1_ABE_m6A_modify_change.sgrna_summary.txt --mageck_count_normalized_result H1_ABE_m6A_modify.count_normalized.txt --min_depth 200 --output_file H1_ABE_m6A_modify_change.sgrna_summary_with_medium_lfc.txt

##STEP5 sgRNA induced mutations predict
---
    (1): sgRNA induced mutations predict by VEP (Ensembl Variant Effect Predictor)
    (2): python sgRNA_resulted_varient_annotation_select.py --VEP_result_file ABE_mutation_predict.txt --sgRNA_varient_file H1_ABE_modify_annotation_select.txt --mageck_result_file  H1_ABE_m6A_modify_change.sgrna_summary_with_medium_lfc.txt --output_file H1_ABE_m6A_modify_change.sgrna_summary_with_varient_annotation.txt

##STEP6 define change sgRNA between CXCR4+ and CXCR4-
---
    python change_sgRNA_annotation.py H1_ABE_m6A_modify_change.sgrna_summary_with_varient_annotation.txt >> H1_ABE_m6A_modify_change.sgrna_summary_with_change_sgRNA_define.txt

# Citing m6A-isoSC-seq

If you use m6A-isoSC-seq in your research, please cite:
"Ren Z, He J, Huang X, et al. Isoform characterization of m6A in single cells identifies its role in RNA surveillance. Nat Commun. 2025;16(1):5828.(doi:10.1038/s41467-025-60869-0)".


#Contact
---
Zhijun Ren renzhj@mail2.sysu.edu.cn  
Jinkai Wang wangjk@mail.sysu.edu.cn  
    
  

