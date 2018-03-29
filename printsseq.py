import sys

from sseq import SSEQ

with open(sys.argv[1],'rb') as f:
    sseq=SSEQ(f)
    for i in sorted(sseq.events.keys()):
        print i,sseq.events[i]
