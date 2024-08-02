#!/usr/bin/env python3
import argparse
import sys


# This script takes in a fasta format file and writes out numbered subfiles
# each of which contains fewer than 1M reads so we can put them through the
# IMGT pipeline.

def main():
    options = get_options()

    if not options.fasta.endswith(".fa"):
        raise Exception("Input file name didn't end with .fa")

    basename = options.fasta[:-3]

    current_chunk = 1
    current_count = 0

    out = open(f"{options.outdir}/{basename}_{current_chunk:>03}.fa","wt",encoding="utf8")

    print("Processing chunk 1", file=sys.stderr)

    for id,seq in read_fasta(options.fasta):
        current_count += 1
        if current_count == options.maxseqs:
            out.close()
            current_chunk += 1
            print(f"Processing chunk {current_chunk}", file=sys.stderr)

            out = open(f"{options.outdir}/{basename}_{current_chunk:>03}.fa","wt",encoding="utf8")
            current_count = 1


        print(f">{id}", file=out)
        print(seq,file=out)

    
    out.close()



def read_fasta(file):
    with open(file,"rt",encoding="utf8") as infh:
        header = None
        seq = ""

        for line in infh:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    yield(header,seq)
                header = line[1:]
                seq = ""

            else:
                seq += line

    yield(header,seq)


def get_options():
    parser = argparse.ArgumentParser("Split fasta file into chunks")

    parser.add_argument("fasta", type=str, help="The input fasta file")
    parser.add_argument("--maxseqs", type=int, default=1000000, help="The maximum number of sequences per chunk (default 1,000,000)")
    parser.add_argument("--outdir",type=str, default=".", help="The output directory")

    options = parser.parse_args()

    return options


if __name__ == "__main__":
    main()