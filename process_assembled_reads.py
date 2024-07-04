#!/usr/bin/env python3
import sys
import gzip


def main():

    file = sys.argv[1]

    # We'll handle input files which are either gzipped or not
    outfile = file.replace(".fastq.gz","_filtered.fa")
    outfile = file.replace(".fastq","_filtered.fa")

    print("Outfile",outfile)

    seen = {}
    rejects = {
        "numi": 0,
        "nolinker":0,
        "dup": 0,
        "good": 0
    }

    infh = None

    if file.lower().endswith(gz):
        infh = gzip.open(file,"rt",encoding="utf8")
    else:
        infh = open(file,"rt",encoding="utf8")

    for header in infh:
        header = header.strip()
        seq = infh.readline().strip()
        infh.readline()
        qual = infh.readline().strip()

        # Get the UMI
        umi = seq[:12]

        # Add the sequence length to the umi to generate more diversity
        umi += str(len(seq))

        if "N" in umi:
            rejects["numi"] += 1
            continue

        seq = seq[12:]

        if seq.startswith("CTGCTCCT"):
            seq = seq[8:]
        elif seq.startswith("GACTCGT"):
            seq = seq[7:]
        else:
            rejects["nolinker"] += 1
            continue

        phred = average_quality(qual)

        if umi in seen:
            rejects["dup"] += 1
            if seen[umi]["phred"] < phred:
                seen[umi] = {"id":header[1:],"seq":seq,"phred":phred}

        else:
            rejects["good"] += 1
            seen[umi] = {"id":header[1:],"seq":seq,"phred":phred}

    infh.close()

    for reason in rejects.keys():
        print(reason,rejects[reason])

    with open(outfile,"wt", encoding="utf8") as out:
        for seq in seen.values():
            print(">"+seq["id"], file=out)
            print(seq["seq"], file=out)



def average_quality(qual):
    phredsum = 0

    for letter in qual:
        phred = ord(letter) - 33
        phredsum += phred


    return phredsum/len(qual)



main()
