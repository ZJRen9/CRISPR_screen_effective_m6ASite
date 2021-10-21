import math

def normalized_file_read(filename,min_depth):
	"""
	sgRNA  Gene    CXCR4minus_Rep1 CXCR4minus_Rep2 CXCR4minus_Rep3 CXCR4plus_Rep1  CXCR4plus_Rpe2  CXCR4plus_Rpe3
	2bc21324.1_AAC_1.6 2bc21324.1_AAC_1    606.3649219714634   633.4234688470073   732.1788790341978   839.6157272360799   806.8623021022981	449.9815512364863
	2bc6873_AAC_5.6    2bc6873_AAC_5   1896.3765696950672  1173.4191188789619  1617.4302430126797  2063.180729739492   2174.343043301006   1299.3849288514268
	2bc11228.0_AAC_6.8 2bc11228.0_AAC_6    1836.9290283253158  1621.7012220007275  1342.3279448960293  1156.2208243813518  1471.6234026280758  1467.2432153800937
	
	"""
	f = open(filename,'r')
	outdict = {}
	for str_x in f:
		str_x = str_x.strip("\n")
		list_x = str_x.split("\t")
		if list_x[0] == "sgRNA":
			#print("\t".join(list_x+["low_lfc","medium_lfc","high_lfc","minus_count_cutoff","plus_count_cutoff"]))
			continue
		sgRNA_name = list_x[0]
		CXCR4minus_Rep1 = float(list_x[2])
		CXCR4minus_Rep2 = float(list_x[3])
		CXCR4minus_Rep3 = float(list_x[4])
		CXCR4plus_Rep1 = float(list_x[5])
		CXCR4plus_Rep2 = float(list_x[6])
		CXCR4plus_Rep3 = float(list_x[7])
		minus_list = [CXCR4minus_Rep1,CXCR4minus_Rep2,CXCR4minus_Rep3]
		plus_list = [CXCR4plus_Rep1,CXCR4plus_Rep2,CXCR4plus_Rep3]
		LFC_list = lfc_count(minus_list,plus_list)
		LFC_list = [str(x) for x in LFC_list]
		medium_LFC = LFC_list[1]
		minus_cutoff = mean_count_cutoff(minus_list,cutoff_value = min_depth)
		plus_cutoff = mean_count_cutoff(plus_list,cutoff_value = min_depth)
		outdict[sgRNA_name] = "\t".join([medium_LFC,minus_cutoff,plus_cutoff])
	return outdict
		#print("\t".join(list_x+LFC_list) + "\t" + minus_cutoff + "\t" + plus_cutoff)

def result_write(filename,medium_lfc_dict,output_file):
	"""
	sgRNA   Gene    control_count   treatment_count control_mean    treat_mean      LFC     control_var     adj_var score   p.low   p.high  p.twosidedFDR      high_in_treatment
	2bc2925_GAC_2.7 2bc2925_GAC_2   642.03/1235.1/257.98    1769.3/3189.5/721.99    642.03  1769.3  1.461   2.4963e+05      30113   6.4961  1       4.1217e-11 8.2433e-11      7.4825e-07      True
	2bc14505_GAC_6.7        2bc14505_GAC_6  3590.6/3978/1921.4      1042.5/1366.5/976.81    3590.6  1042.5  -1.7832 1.4681e+06      1.9155e+05      5.8221     2.9055e-09      1       5.8109e-09      2.6373e-05      False
	2bc1788_GAC_5.5 2bc1788_GAC_5   263.95/470.57/1088.6    1251.6/1237.1/1117.4    470.57  1237.1  1.3925  2.1235e+05      21565   5.2195  1       8.9742e-08 1.7948e-07      0.00054306      True
	"""	
	f = open(filename,'r')
	d = open(output_file,'a')
	for str_x in f:
		str_x = str_x.strip("\n")
		list_x = str_x.split("\t")
		if list_x[0] == "sgRNA":
			str2write = "\t".join([str_x,"medium_LFC","CRCX4minus_counts_cutoff","CRCX4plus_counts_cutoff"]) + "\n"
			d.write(str2write)
			continue
		sgRNA_name = list_x[0]
		value = medium_lfc_dict[sgRNA_name]
		str2write = "\t".join([str_x,value]) + "\n"
		d.write(str2write)


def lfc_count(minus_list,plus_list):
	LFC_list = []
	for i in range(len(minus_list)):
		value_minus = minus_list[i]
		value_plus = plus_list[i]
		try:
			LFC = math.log2(value_plus/value_minus)
			LFC_list.append(LFC)
		except:
			LFC = 0
			LFC_list.append(LFC)
	LFC_list.sort()
	return LFC_list

def mean_count_cutoff(minus_list,cutoff_value):
	mean_counts = sum(minus_list)/len(minus_list) 
	if mean_counts < cutoff_value:
		return "False"
	else:
		return "True"

def make_args():
	import argparse
	parser = argparse.ArgumentParser(description='medium log2-foldchange calculate and min counts cutoff')
	parser.add_argument('--mageck_test_sgrna_summary_result', required=True, help="mageck_test_sgrna_summary_result")
	parser.add_argument('--mageck_count_normalized_result', required=True, help="mageck_count_normalized_result")
	parser.add_argument('--min_depth', required=True, help="min_depth")
	parser.add_argument('--output_file', required=True, help="result_file")
	args = parser.parse_args()
	return args

def main():
	args = make_args()
	mageck_test_sgrna_summary_result = args.mageck_test_sgrna_summary_result
	mageck_count_normalized_result = args.mageck_count_normalized_result
	min_depth = int(args.min_depth)
	output_file = args.output_file

	medium_lfc_dict = normalized_file_read(filename=mageck_count_normalized_result,min_depth=min_depth)
	result_write(filename=mageck_test_sgrna_summary_result,medium_lfc_dict=medium_lfc_dict,output_file=output_file)

	
if __name__=="__main__":
	main()










