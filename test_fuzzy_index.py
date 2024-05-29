#!/usr/bin/env python3
from find_replacement_circles import fuzzy_index
import timeit

# Basic search
assert(fuzzy_index("AAAAGAT","GAT")==4)

# Basic search fails
assert(fuzzy_index("AAAAGAT","GAG")==-1)

# Basic mismatch search
assert(fuzzy_index("AAAAGATG","GAGG",allowed_mismatches=1)==4)

# Start later
assert(fuzzy_index("GATAAAAGAT","GAT", initialpos=1)==7)
assert(fuzzy_index("GATAAAAGAT","GAT", initialpos=7)==7)
assert(fuzzy_index("GATAAAAGAT","GATGG", initialpos=8)==-1)

# Stop earlier
assert(fuzzy_index("AAAAAAGATAAAA","GAT", lastpos=6)==6)
assert(fuzzy_index("AAAAAAGATAAAA","GAT", lastpos=5)==-1)

# Amount of fuzziness
assert(fuzzy_index("AAAAGAT","AAAAGAT")==0)
assert(fuzzy_index("AAAAGAT","ATAAGAT")==-1)
assert(fuzzy_index("AAAAGAT","ATAAGAT", allowed_mismatches=1)==0)
assert(fuzzy_index("AAAAGAT","ATTAGAT", allowed_mismatches=1)==-1)
assert(fuzzy_index("AAAAGAT","ATTAGAT", allowed_mismatches=2)==0)


# Performance
print("Index",timeit.timeit(lambda: "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT".index("TTTTT"), number=100000))

print("FIndex",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT"), number=100000))

print("FIndex 1 mismatch",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", allowed_mismatches=1), number=100000))

print("FIndex 2 mismatch",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", allowed_mismatches=2), number=100000))

print("FIndex 2 mismatch Last=50",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", allowed_mismatches=2, lastpos=50), number=100000))

print("FIndex 2 mismatch Last=20",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", allowed_mismatches=2, lastpos=20), number=100000))

print("FIndex Initial=0",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=0), number=100000))
print("FIndex Initial=10",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=10), number=100000))
print("FIndex Initial=20",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=20), number=100000))
print("FIndex Initial=30",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=30), number=100000))
print("FIndex Initial=40",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=40), number=100000))
print("FIndex Initial=50",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=50), number=100000))
print("FIndex Initial=60",timeit.timeit(lambda: fuzzy_index("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATTTTT","TTTTT", initialpos=60), number=100000))


