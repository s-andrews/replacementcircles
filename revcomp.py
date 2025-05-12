#!/usr/bin/env python3
import sys
import textwrap

def main():
    files = sys.argv[1:]

    for file in files:
        rcfile = file.replace(".fa","_rev.fa")
        if file == rcfile:
            raise Exception("Output same as input")
        reverse_fasta(file,rcfile)



def reverse_fasta(infile,outfile):
    print("Reversing",infile,"to",outfile)
    transtab = str.maketrans("gatc","ctag")
    with open(outfile,"wt", encoding="utf8") as out:
        for id,seq in read_fasta(infile):
            seq = seq[::-1]
            seq = seq.translate(transtab)
            #seq = "\n".join(textwrap.wrap(seq,width=50))
            print(f">{id}\n{seq.upper()}", file=out)



def read_fasta(file):
    seq = None
    id = None
    with open(file,"rt",encoding="utf8") as infh:
        for line in infh:
            if line.startswith(">"):
                if seq is not None:
                    yield (id,seq)

                id = line[1:].split()[0].strip()
                seq = ""
            else:
                seq += line.lower().strip()

        if seq is not None:
            yield(id,seq)

main()
