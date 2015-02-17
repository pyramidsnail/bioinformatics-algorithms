seq = raw_input().strip()
codon = {'UUU': 'F',
         'UUC': 'F',
         'UUA': 'L',
         'UUG': 'L',
         'UCU': 'S',
         'UCC': 'S',
         'UCA': 'S',
         'UCG': 'S',
         'UAU': 'Y',
         'UAC': 'Y',
         'UGU': 'C',
         'UGC': 'C',
         'UGG': 'W',
         'CUU': 'L',
         'CUC': 'L',
         'CUA': 'L',
         'CUG': 'L',
         'CCU': 'P',
         'CCC': 'P',
         'CCA': 'P',
         'CCG': 'P',
         'CAU': 'H',
         'CAC': 'H',
         'CAA': 'Q',
         'CAG': 'Q',
         'CGU': 'R',
         'CGG': 'R',
         'CGC': 'R',
         'CGA': 'R',
         'AUU': 'I',
         'AUC': 'I',
         'AUA': 'I',
         'AUG': 'M',
         'ACU': 'T',
         'ACC': 'T',
         'ACA': 'T',
         'ACG': 'T',
         'AAU': 'N',
         'AAC': 'N',
         'AAA': 'K',
         'AAG': 'K',
         'AGU': 'S',
         'AGC': 'S',
         'AGA': 'R',
         'AGG': 'R',
         'GUU': 'V',
         'GUC': 'V',
         'GUA': 'V',
         'GUG': 'V',
         'GCU': 'A',
         'GCC': 'A',
         'GCA': 'A',
         'GCG': 'A',
         'GCU': 'A',
         'GAU': 'D',
         'GAC': 'D',
         'GAA': 'E',
         'GAG': 'E',
         'GGU': 'G',
         'GGC': 'G',
         'GGA': 'G',
         'GGG': 'G'
         
    }

aa = ''
# for x in range(len(seq)):
#     if seq[x:x+3]=='AUG':
for i in range(0, len(seq),3):
    if seq[i:i+3] in codon:
        aa += codon[seq[i:i+3]]
    #         else:
    #             break
    # print aa
    # break
print aa
