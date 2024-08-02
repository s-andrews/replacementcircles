#!/usr/bin/env python3
import sys
import gzip
import argparse


def main():

    options = get_options()

    seen = {}
    rejects = {
        "numi": 0,
        "nolinker":0,
        "dup": 0,
        "good": 0
    }

    infh = None

    if options.seqfile.lower().endswith("gz"):
        infh = gzip.open(options.seqfile,"rt",encoding="utf8")
    else:
        infh = open(options.seqfile,"rt",encoding="utf8")

    out = open(options.outfile,"wt", encoding="utf8")

    for header in infh:
        header = header.strip()
        seq = infh.readline().strip()
        infh.readline()
        qual = infh.readline().strip()

        # Get the UMI
        umi = seq[:12]

        # Add the sequence length to the umi to generate more diversity
        umi_seqlen = len(seq)

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

        keepingIt = True
        if umi in seen:
            # We could have seen this before.  We now need to check the lengths of 
            # the hits and we'll only keep it if ours is more than 4bp different

            for seenlength in seen[umi]:
                if abs(seenlength-umi_seqlen < 4):
                    keepingIt = False
                    break

        if not keepingIt:
            rejects["dup"] += 1
        else:
            rejects["good"] += 1
            if not umi in seen:
                seen[umi] = set()

            if not umi_seqlen in seen[umi]:
                seen[umi].add(umi_seqlen)

            print(">"+header[1:], file=out)
            print(seq, file=out)


    infh.close()
    out.close()

    for reason in rejects.keys():
        print(reason,rejects[reason])



def get_options():

    parser = argparse.ArgumentParser("Preprocess and deduplicate assembled VDJ sequences")
    parser.add_argument("seqfile",type=str,help="FastQ format sequence file to process")
    parser.add_argument("outfile",type=str,help="Output file for processed data")

    options = parser.parse_args()


    return options



if __name__ == "__main__":
    main()
