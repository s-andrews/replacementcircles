#!/usr/bin/env python3

# This script extracts the fasta hits from a previous search

import sys

def main():
    if len(sys.argv) != 4:
        print("Usage is extract_hits.py [search result] [input fasta] [output fasta]")
        sys.exit(1)

    result_file, input_file, output_file = sys.argv[1:]

    hit_ids = get_hit_ids(result_file)
    filter_file(input_file,hit_ids,output_file)


def filter_file(input, hits, output):

    with open(output,"wt", encoding="utf8") as out:
        for id,seq in read_fasta(input):
            if id in hits:
                print(">"+id,file=out)
                print(seq, file=out)


def get_hit_ids(file):

    ids = []

    with open(file,"rt",encoding="utf8") as infh:
        for line in infh:
            if line.strip():
                ids.append(line.strip().split()[0])


    return ids


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