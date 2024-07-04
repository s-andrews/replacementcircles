VDJ Replacement Circle Detection
================================

The software here does the processing and analysis of VDJ-Seq amplicon data to detect non-canonical splicing events.


Introduction
------------


Input Data
----------

The input to this pipeline is a fastq format file of complete VDJ segments.  If you are happy to use long single reads then you can start from those, but more commonly these will start as paried reads which will need to be assembled into a single contiguous sequence.

The structure of the reads will be

1. A 12bp UMI sequence
2. A standard linker with sequence of either ```CTGCTCCT``` or ```GACTCGT```
3. The remaining VDJ sequence

The pipeline consists of the following steps

1. [Optional] Assembly of paired reads to single contigs
2. Processing to deduplicate sequences and remove UMI and linker sequences
3. Detection of non-canonical V-sequence combinations
4. [Optional] Extraction of hit sequences for further study


Running the pipeline
--------------------

### [Optional] Sequence Assembly
You can assemble the paired sequences using any suitable program.  We used [PEAR](https://cme.h-its.org/exelixis/web/software/pear/) for this purpose, for example:

```
pear -j 5 -f sample_R1.fastq.gz -r sample_R2.fastq.gz -o sample_joined
```

Which would create a file called ```sample_joined.assembled.fastq``` which can progress to the next step.


### Read Processing
The next step would be to process the reads to identify and remove linker sequences and UMIs and to deduplicate the data based on a combination of UMI sequence and read length.  Where multiple reads share the same UMI and length, the one with the highest average base call accuracy is retained.

```
process_assembled_reads.py sample_joined.assembled.fastq sample_joined.processed.fa
```

As well as creating the output fasta file it will also show you the number of reads which were processed and rejected.

```
numi 5647
nolinker 1517501
dup 13875888
good 2007723
```

* ```numi``` means that the UMI sequence contained one or more uncalled bases
* ```nolinker``` means that neither of the two expected linker sequences was found at the start of the read
* ```dup``` means the number of reads which had an exact UMI + sequence length match to another read
* ```good``` is the number of valid reads retained in the output file


### Replacement Circle Detection
Next we can take the filtered reads and search for unexpected VDJ combinations.  The search is based on a set of expected germline V1/V2 sequence pairs.  We supply a suitable dataset for mouse V sequences in the ```v_sequences.txt``` file.  If you wish to use another species, or customise these sequences then you can create your own file with similar formatting.

Most of the sequences in your database will have a standard V1/V2 germline combination, ie the two sequences will be the expected pairs for one V region.  Many V sequences are highly similar, so the program makes every effort to detect possible germline combinations and rejects those sequences.  Only sequences which are not possible germline matches are reported.

The process for searching is as follows:

1. The sequences is searched against the V1 sequences allowing (by default) 1bp mismatch until a match is found.  If no match is found the sequence is rejected.
2. If a match is found the corresponding V2 sequence is searched, allowing up to 3 mismatches (by default).  If it is found the sequence is rejected as germline.
3. If no match is found then the remaining V2 sequences are searched until a match is found.  If no match is found the sequence is rejected.
4. If a V2 match is found then the corresponding V1 sequences is searched allowing up to 3 mismatches.  If that is found then the sequence is rejected as germline.
5. If no match was found to the V1 then the non-canonical V1/V2 pair is reported.

Because of the high degree of similarity between V1 and V2 sequences (some are completely identical), the reported pairing may not be the only one which is compatible with the sequence, but other matches would also not be germline compatible, and would be highly similar (within 1bp) of the reported pairs.

The search can be run with:

```
find_replacement_circles --threads 10 --vfile v_sequences.txt sample_joined.processed.fa sample_joined.processed_hits.txt
```

The output file is a tab delimited text file with the following columns:

1. ```READ_ID``` The ID of the sequence read  
2. ```VSEQ1``` The name of the V1 sequence
3. ```VSEQ2``` The name of the V2 sequence
4. ```VSEQ1_END``` The position in the read at which the V1 sequence ends
5. ```VSEQ2_START``` The position in the read at which the V2 sequence started
6. ```DISTANCE``` The number of bases between the end of V1 and the start of V2            

In addition the program will write out some stats to stdout.  You will see warnings about duplicated V sequences in your v sequence file, and you will get a progress message each time 1000 reads have been processed.

```
hits 13
seq_too_short 20828
germline 746194
nov1 523476
nov2 561255
too_short 0
too_long 204
total_seqs 1620321
Saving results to sample_joined.processed_hits.txt
```

The values here represent:

1. ```hits``` the number of reported non-canonical pairings
2. ```seq_too_short``` the read length was shorter than the sum of the shortest V1, shortest V2 and minimum separating length
3. ```sgermline``` a match was found to a compatible pair of V1/V2 sequences
4. ```nov1``` no match was found to any V1 sequence with the specified number of allowed mismatches (```--mismatches```)
5. ```nov2``` no match was found to any V2 sequence with the specified number of allowed mismatches (```--mismatches```)
6. ```too_short``` the distance between the end of V1 and the start of V2 was less than the distance specified by ```--mindist```
7. ```too_long``` the distance between the end of V1 and the start of V2 was more than the distance specified by ```--maxdist```
8. ```total_seqs``` the total number of sequences in the input file

### [Optional] Sequence extraction

If you wish to extract the subset of hit sequences from the processed fasta file then you can use the ```extract_hits.py``` script to do this

```
extract_hits.py sample_joined.processed_hits.txt sample_joined.processed.fa sample_joined.processed_hits.fa
```



