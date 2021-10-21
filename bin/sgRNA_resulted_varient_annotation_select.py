#Uploaded_variation	Location	Allele	Consequence	IMPACT	SYMBOL	Gene	Feature_type	Feature	BIOTYPE	EXON	INTRON	HGVSc	HGVSp	cDNA_position	CDS_position	Protein_position	Amino_acids	Codons	Existing_variation	DISTANCE	STRAND	FLAGS	SYMBOL_SOURCE	HGNC_ID	TSL	APPRIS	SIFT	PolyPhen	AF	CLIN_SIG	SOMATIC	PHENO	PUBMED	MOTIF_NAME	MOTIF_POS	HIGH_INF_POS	MOTIF_SCORE_CHANGE
#1_566860_A/G	1:566860-566860	G	non_coding_transcript_exon_variant	MODIFIER	hsa-mir-6723	ENSG00000237973	Transcript	ENST00000414273.1	unprocessed_pseudogene	1/1	-	-	-	407	-	-	-	-	-	-	1	-	miRBase	-	-	-	-	-	-	-	-	-	-	-	-	-	-
#1_566860_A/G	1:566860-566860	G	upstream_gene_variant	MODIFIER	RP5-857K21.11	ENSG00000198744	Transcript	ENST00000416718.2	unprocessed_pseudogene	-	-	-	-	-	-	-	-	-	-	2896	1	-	Clone_based_vega_gene	-	-	-	-	-	-	-	-	-	-	-	-	-	-


def varient_anntate_to_dict(filename):
	"""
	#Uploaded_variation     Location        Allele  Consequence     IMPACT  SYMBOL  Gene    Feature_type    Feature BIOTYPE EXON    INTRON  HGVSc   HGVSp      cDNA_position   CDS_position    Protein_position        Amino_acids     Codons  Existing_variation      DISTANCE        STRAND  FLAGS   SYMBOL_SOURCE      HGNC_ID TSL     APPRIS  SIFT    PolyPhen        AF      CLIN_SIG        SOMATIC PHENO   PUBMED  MOTIF_NAME      MOTIF_POS       HIGH_INF_POS       MOTIF_SCORE_CHANGE
	1_566860_A/G    1:566860-566860 G       non_coding_transcript_exon_variant      MODIFIER        hsa-mir-6723    ENSG00000237973 Transcript      ENST00000414273.1  unprocessed_pseudogene  1/1     -       -       -       407     -       -       -       -       -       -       1       -       miRBase    -       -       -       -       -       -       -       -       -       -       -       -       -       -
	1_566860_A/G    1:566860-566860 G       upstream_gene_variant   MODIFIER        RP5-857K21.11   ENSG00000198744 Transcript      ENST00000416718.2 unprocessed_pseudogene   -       -       -       -       -       -       -       -       -       -       2896    1       -       Clone_based_vega_gene      -       -       -       -       -       -       -       -       -       -       -       -       -       -
	"""
	f = open(filename,'r')
	outdict = {}
	for str_x in f:
		str_x = str_x.strip("\n")
		list_x = str_x.split("\t")
		if str_x[0]=="#":
			continue
		chrom = "chr"+list_x[1].split(":")[0]
		site = list_x[1].split("-")[1]
		sitename = ";".join([chrom,site])
		protein_sense = list_x[3]
		protein_sense = protein_sense
		transid = list_x[8].split(".")[0]
		geneid = list_x[6]
		try:
			outdict[sitename].append([geneid,transid,protein_sense])
		except:
			outdict[sitename] = [[geneid,transid,protein_sense]]
	return outdict

def annotation_select_file_read(filename,sense_dict,varient_type_dict):
	"""
	sgRNA   Gene    chrom   start   end     strand  guide   ENSG    ENST    Genename
	2bc130_AAC_4.4  2bc130_AAC_4    chr1    11083482        11083483        +       GAACTTTTGAAACCTTGTGT    ENSG00000120948 ENST00000240185 TARDBP
	2bc494_GAC_5.4  2bc494_GAC_5    chr1    38174060        38174061        +       GGACTTTTAATGGGCACTTC    ENSG00000134690 ENST00000373055 CDCA8
	"""
	f = open(filename,'r')
	outdict = {}
	for str_x in f:
		str_x = str_x.strip("\n")
		list_x = str_x.split("\t")
		if list_x[0] == "sgRNA":
			print(str_x+"\t"+"varient_annotation")
			continue
		sgRNA = list_x[0]
		chrom = list_x[2]
		start = list_x[3]
		end = list_x[4]
		geneid = list_x[7]
		#transid = list_x[8]
		#print(geneid,transid)
		sitename = ";".join([chrom,end])
		if sitename == "NA;NA":
			sense_annotation = "NA"
		else:
			sense_annotation_list = sense_dict[sitename]
			if sense_annotation_list == [] or geneid == "NA":
				sense_annotation = "NA"
			else:
				sense_annotation = sense_annotation_select_by_transid(sense_annotation_list,varient_type_dict)
		outdict[sgRNA] = sense_annotation
	return outdict

def result_write(mageck_file,result_file,sgRNA_annotation_dict):
	"""
	sgRNA   Gene    control_count   treatment_count control_mean    treat_mean      LFC     control_var     adj_var score   p.low   p.high  p.twosided	FDR      high_in_treatment       medium_LFC      CRCX4minus_counts_cutoff        CRCX4plus_counts_cutoff
	2bc2925_GAC_2.7 2bc2925_GAC_2   642.03/1235.1/257.98    1769.3/3189.5/721.99    642.03  1769.3  1.461   2.4963e+05      30113   6.4961  1       4.1217e-11 8.2433e-11      7.4825e-07      True    1.4624707429902415      True    True
	2bc14505_GAC_6.7        2bc14505_GAC_6  3590.6/3978/1921.4      1042.5/1366.5/976.81    3590.6  1042.5  -1.7832 1.4681e+06      1.9155e+05      5.8221     2.9055e-09      1       5.8109e-09      2.6373e-05      False   -1.5415383342186177     True    True
	"""
	f = open(mageck_file,'r')
	d = open(result_file,'a')
	for str_x in f:
		str_x = str_x.strip("\n")
		list_x = str_x.split("\t")
		if list_x[0] == "sgRNA":
			strwrite = str_x + "\t" + "varient_annotation" + "\n"
			d.write(strwrite)
			continue
		sgRNA = list_x[0]
		if sgRNA[0:2] == "NT":
			varient_annotation = "NA"
		else:
			varient_annotation = sgRNA_annotation_dict[sgRNA]
		strwrite = str_x + "\t" + varient_annotation + "\n"
		d.write(strwrite)
		
		

def sense_annotation_select_by_transid(sense_annotation_list,varient_type_dict):
	sense_annotation_list_geneid_select = [x for x in sense_annotation_list] #if x[0]==geneid]
	sense_annotation_list_type_make = [varient_type_dict[x[2]] for x in sense_annotation_list_geneid_select]
	#sense_annotation_list_sort_genetype = list_sort_by_given_list(listinput=sense_annotation_list_type_make,index=2,index_dict={"coding":1,"non_coding":2,"NMD_transcript":3,"miRNA":4})
	#sense_annotation_list_sort_position = list_sort_by_given_list(listinput=sense_annotation_list_sort_genetype,index=1,index_dict={"exon":1,"intron":2,"intergenic":3})
	
	varient_dict = {
	"3_prime_UTR_variant":1,
	"5_prime_UTR_variant":2,
	"synonymous_variant":3,
	"non_coding_transcript_exon_variant":4,
	"intron_variant":5,
	"missense_variant":6,
	"intergenic_variant":7,
	"start_lost":8,
	"stop_lost":9,
	"upstream_gene_variant":10,
	"downstream_gene_variant":11,
	"coding_sequence_variant":12,
	"stop_retained_variant":13,
	"splice_region_variant":14,
	"splice_donor_variant":15,
	"splice_acceptor_variant":16,
	"incomplete_terminal_codon_variant":17,
	"mature_miRNA_variant":18,
	"TF_binding_site_variant":19,
	"regulatory_region_variant":20
	}
	sense_annotation_list_sort_varient = list_sort_by_given_list(listinput=sense_annotation_list_type_make,index=0,index_dict=varient_dict)
	sense_annotation_list_sort_genetype = list_sort_by_given_list(listinput=sense_annotation_list_sort_varient,index=2,index_dict={"coding":1,"non_coding":2,"NMD_transcript":3,"miRNA":4})
	sense_annotation_list_sort_position = list_sort_by_given_list(listinput=sense_annotation_list_sort_genetype,index=1,index_dict={"exon":1,"intron":2,"intergenic":3})
	return sense_annotation_list_sort_position[0][0]
	


def list_sort_by_given_list(listinput,index,index_dict):
	outlist = []
	for x in listinput:
		value = index_dict[x[index]]
		outlist.append(x+[value])
	outlist.sort(key=lambda x:x[-1])
	outlist = [x[:-1] for x in outlist]
	return outlist

varient_type_dict = {
	"non_coding_transcript_exon_variant":["non_coding_transcript_exon_variant","exon","non_coding"],
	"upstream_gene_variant":["upstream_gene_variant","intron","coding"],
	"downstream_gene_variant":["downstream_gene_variant","intron","coding"],
	"intron_variant,non_coding_transcript_variant":["intron_variant","intron","non_coding"],
	"regulatory_region_variant":["regulatory_region_variant","intergenic","coding"],
	"5_prime_UTR_variant":["5_prime_UTR_variant","exon","coding"],
	"intron_variant":["intron_variant","intron","coding"],
	"missense_variant":["missense_variant","exon","coding"],
	"3_prime_UTR_variant":["3_prime_UTR_variant","exon","coding"],
	"3_prime_UTR_variant,NMD_transcript_variant":["3_prime_UTR_variant","exon","NMD_transcript"],
	"intron_variant,NMD_transcript_variant":["intron_variant","intron","NMD_transcript"],
	"intergenic_variant":["intergenic_variant","intergenic","non_coding"],
	"5_prime_UTR_variant,NMD_transcript_variant":["5_prime_UTR_variant","exon","NMD_transcript"],
	"TF_binding_site_variant":["TF_binding_site_variant","intergenic","coding"],
	"synonymous_variant":["synonymous_variant","exon","coding"],
	"missense_variant,NMD_transcript_variant":["missense_variant","exon","NMD_transcript"],
	"stop_lost":["stop_lost","exon","coding"],
	"splice_region_variant,intron_variant,non_coding_transcript_variant":["splice_region_variant","intron","non_coding"],
	"splice_region_variant,synonymous_variant":["synonymous_variant","exon","coding"],
	"splice_region_variant,non_coding_transcript_exon_variant":["non_coding_transcript_exon_variant","exon","non_coding"],
	"stop_retained_variant":["stop_retained_variant","exon","coding"],
	"splice_region_variant,intron_variant":["splice_region_variant","intron","coding"],
	"synonymous_variant,NMD_transcript_variant":["synonymous_variant","exon","NMD_transcript"],
	"missense_variant,splice_region_variant":["missense_variant","exon","coding"],
	"mature_miRNA_variant":["mature_miRNA_variant","exon","miRNA"],
	"incomplete_terminal_codon_variant,coding_sequence_variant":["incomplete_terminal_codon_variant","exon","coding"],
	"coding_sequence_variant,NMD_transcript_variant":["coding_sequence_variant","exon","NMD_transcript"],
	"splice_donor_variant,non_coding_transcript_variant":["splice_donor_variant","exon","non_coding"],
	"splice_region_variant,intron_variant,NMD_transcript_variant":["splice_region_variant","intron","NMD_transcript"],
	"splice_region_variant,5_prime_UTR_variant":["5_prime_UTR_variant","exon","coding"],
	"start_lost":["start_lost","exon","coding"],
	"missense_variant,splice_region_variant,NMD_transcript_variant":["missense_variant","exon","NMD_transcript"],
	"splice_acceptor_variant":["splice_acceptor_variant","exon","coding"],
	"start_lost,NMD_transcript_variant":["start_lost","exon","NMD_transcript"],
	"splice_region_variant,3_prime_UTR_variant,NMD_transcript_variant":["3_prime_UTR_variant","exon","NMD_transcript"],
	"splice_acceptor_variant,non_coding_transcript_variant":["splice_acceptor_variant","exon","non_coding"],
	"splice_acceptor_variant,NMD_transcript_variant":["splice_acceptor_variant","exon","NMD_transcript"],
	"stop_retained_variant,NMD_transcript_variant":["stop_retained_variant","exon","NMD_transcript"],
	"splice_region_variant,synonymous_variant,NMD_transcript_variant":["synonymous_variant","exon","NMD_transcript"],
	"stop_lost,NMD_transcript_variant":["stop_lost","exon","NMD_transcript"],
	"splice_donor_variant":["splice_donor_variant","exon","coding"],
	"splice_donor_variant,NMD_transcript_variant":["splice_donor_variant","exon","NMD_transcript"],
	"splice_region_variant,stop_retained_variant":["stop_retained_variant","exon","coding"],
	"splice_region_variant,3_prime_UTR_variant":["3_prime_UTR_variant","exon","coding"],
	"splice_region_variant,5_prime_UTR_variant,NMD_transcript_variant":["5_prime_UTR_variant","exon","NMD_transcript"],
	"coding_sequence_variant":["coding_sequence_variant","exon","coding"],
}


def make_args():
	import argparse
	parser = argparse.ArgumentParser(description='sgRNA resulted varient annotation select')
	parser.add_argument('--VEP_result_file', required=True, help="Ensembl Variant Effect Predictor result")
	parser.add_argument('--sgRNA_varient_file', required=True, help="sgRNA resulted varient")
	parser.add_argument('--mageck_result_file', required=True, help="mageck result with medium lfc")
	parser.add_argument('--output_file', required=True, help="result filename")
	args = parser.parse_args()
	return args


def main():
	args = make_args()
	VEP_result_file = args.VEP_result_file
	sgRNA_varient_file = args.sgRNA_varient_file
	mageck_result_file = args.mageck_result_file
	output_file = args.output_file

	varient_dict = varient_anntate_to_dict(filename=VEP_result_file)
	
	sgRNA_to_varient_type_dict = annotation_select_file_read(filename=sgRNA_varient_file,sense_dict=varient_dict,varient_type_dict=varient_type_dict)
	
	result_write(mageck_file = mageck_result_file,result_file = output_file,sgRNA_annotation_dict = sgRNA_to_varient_type_dict)
	
	
if __name__=="__main__":
	main()




