# PAM
PAM = {}
PAM["NGG"] = ['AGG', 'TGG', 'CGG', 'GGG']

# Base_editor[name] = [PAM_type, window_start, window_end, gRNA_length]
Base_editor = {}
Base_editor["BE3-Cas9"] = ['NGG', 4, 8, 20]

file = 'hg19_m6A_sequence_-30-+30.txt'
seq_file = open(file, 'r')
count = len(open(file, 'r').readlines())
header = ['m6A_site', 'chromsome', 'start', 'end', 'strand', 'sequence']

_str = []
for i in range(count):
    Input = seq_file.readline()
    line_split = Input.split('\t')
    m6A_site = line_split[0]
    chromsome = line_split[1]
    start = line_split[2]
    end = line_split[3]
    strand = line_split[4]
    sequence = line_split[5].strip()
    gRNA_list = {}
    for editor in Base_editor.keys():
        editor_info = Base_editor[editor]
        editor_PAM = editor_info[0]
        window_start = editor_info[1]
        window_end = editor_info[2]
        gRNA_length = editor_info[3]
        if sequence[31] == "C":
            PAM_len = len(editor_PAM)
            window_length = window_end - window_start + 1
            checkseq = sequence[
                       31 + gRNA_length - window_end + 1: 31 + gRNA_length - window_end + 1 + window_length + PAM_len]
            gRNA_list[editor] = ""
            for i in range(window_length):
                if checkseq[i: i + PAM_len] in PAM[editor_PAM]:
                    editing_position = window_end - i
                    gRNA_sequence = sequence[31 - editing_position + 1: 31 - editing_position + 1 + gRNA_length]
                    gRNA_list[editor] = gRNA_list[editor] + ',' + gRNA_sequence
                    if strand == '+':
                        start2 = str(int(line_split[2]) + 31 - editing_position)
                        end2 = str(int(start2) + gRNA_length)
                    else:
                        end2 = str(int(line_split[3]) - (31 - editing_position + 1))
                        start2 = str(int(end2) - gRNA_length)
                    gRNA_name = line_split[0] + '.' + str(editing_position)
                    count_C = str(gRNA_sequence[window_start - 1: window_end].count('C'))
                    _str.append('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format\
                                    (chromsome, start2, end2, gRNA_name, count_C, strand, gRNA_sequence))
l = open('BE_position.bed', 'w')
l.writelines(_str)
l.close()