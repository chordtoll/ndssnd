import sys

from swd import SWD

with open(sys.argv[1],'rb') as f:
    sseq=SWD(f)

print sseq
