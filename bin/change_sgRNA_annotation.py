#sgRNA	Gene	control_count	treatment_count	control_mean	treat_mean	LFC	control_var	adj_var	score	p.low	p.high	p.twosided	FDR	high_in_treatment	low_lfc	medium_lfc	high_lfc	minus_count_cutoff	plus_count_cutoff	gene_annotation	m6A_annotation	varient_annotation	m6Asinglesite
#2bc2925_GAC_2.7	2bc2925_GAC_2	642.03/1235.1/257.98	1769.3/3189.5/721.99	642.03	1769.3	1.461	2.4963e+05	30113	6.4961	1	4.1217e-11	8.2433e-11	7.4825e-07	True	1.3686597650150256	1.4624707429902415	1.4847516133189824	True	True	ADM	chr11;10328400;10328500	3_prime_UTR_variant	chr11;10328255;10328256;+
#2bc14505_GAC_6.7	2bc14505_GAC_6	3590.6/3978/1921.4	1042.5/1366.5/976.81	3590.6	1042.5	-1.7832	1.4681e+06	1.9155e+05	5.8221	2.9055e-09	1	5.8109e-09	2.6373e-05	False	-1.7841585782674902	-1.5415383342186177	-0.976028064354796	True	True	SOX2	chr3;181430600;181430700	3_prime_UTR_variant	chr3;181431109;181431110;+
#2bc1788_GAC_5.5	2bc1788_GAC_5	263.95/470.57/1088.6	1251.6/1237.1/1117.4	470.57	1237.1	1.3925	2.1235e+05	21565	5.2195	1	8.9742e-08	1.7948e-07	0.00054306	True	0.03758737594113803	1.394440403646774	2.245397825859351	True	True	MLK4	chr1;233518200;233518300	missense_variant	chr1;233518353;233518354;+


def fileread(filename):
	f = open(filename,'r')
	for str_x in f:
		str_x = str_x.strip("\n")
		list_x = str_x.split("\t")
		if list_x[0]=="sgRNA":
			minus_count_cutoff_index = list_x.index("CRCX4minus_counts_cutoff")
			plus_count_cutoff_index = list_x.index("CRCX4plus_counts_cutoff")
			medium_lfc_index = list_x.index("medium_LFC")
			p_low_index = list_x.index("p.low")
			p_high_index = list_x.index("p.high")
			varient_annotation_index = list_x.index("varient_annotation")
			print("\t".join([str_x,"change_sgRNA","high_confidence_change_sgRNA"]))
			continue
		minus_count_cutoff = list_x[minus_count_cutoff_index]
		plus_count_cutoff = list_x[plus_count_cutoff_index]
		medium_lfc = list_x[medium_lfc_index]
		p_low = list_x[p_low_index]
		p_high = list_x[p_high_index]
		varient_annotation = list_x[varient_annotation_index]
		sgRNA = list_x[0]
		#print(minus_count_cutoff,plus_count_cutoff,medium_lfc,p_low,p_high,varient_annotation)
		if minus_count_cutoff == "False" or plus_count_cutoff == "False":
			change_type = "unchange"
			high_change_type = "unchange"
		#elif not sgRNA[0:3] == "2bc":
		#	change_type = "unchange"
		#	high_change_type = "unchange"
		else:
			if float(p_high)<=0.05 and float(medium_lfc)>=0.5849625:
				change_type = "CRCX+ enrichment"
			elif float(p_low)<=0.05 and float(medium_lfc)<=-0.5849625:
				change_type = "CRCX- enrichment"
			else:
				change_type = "unchange"
			
			if float(p_high)<=0.05 and float(medium_lfc)>=1 and (not varient_annotation=="missense_variant"):
				high_change_type = "CRCX+ enrichment(high confidence)"
			elif float(p_low)<=0.05 and float(medium_lfc)<=-1 and (not varient_annotation=="missense_variant"):
				high_change_type = "CRCX- enrichment(high confidence)"
			else:
				high_change_type = "unchange"
		print("\t".join([str_x,change_type,high_change_type]))
		
		
if __name__=="__main__":
	import sys
	fileread(sys.argv[1])
		







