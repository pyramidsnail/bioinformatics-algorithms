from Bio import SeqIO

f = open("gc.txt", "r")
dic = {}
for record in SeqIO.parse(f, "fasta"):
    C_count = record.seq.count('C') 
    G_count = record.seq.count('G')
    length = len(record.seq)
    dic[record.name] = float(C_count+G_count)/length
max_value = 0
max_key = ""
for key, value in dic.iteritems():
    if value > max_value:
        max_key = key
        max_value = value
print max_key
print max_value*100
