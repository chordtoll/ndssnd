import sys
import time
import wave
import math
import struct
import random

from smd import SMD

with open(sys.argv[1],'rb') as f:
    sseq=SMD(f)


n1='CCDDEFFGGAAB'
n2=' # #  # # # '

def n2n(n):
    return n1[n%12]+('#' if n2[n%12]=='#' else '')+str((n/12)-1)

nbt=[{} for i in xrange(32)]

for e in sorted(sseq.events.keys()):
    for i in xrange(32):
        if i in sseq.events[e].keys():
            nbt[i][e]=sseq.events[e][i]


for i in xrange(32):
    for e in sorted(nbt[i].keys()):
        print 'Track',str(i)+', tick',str(e)+':',
        evt=nbt[i][e]
        if evt[0][0]=='note':
            print n2n(evt[0][1][0])+' for '+str(evt[0][1][2])+' ticks',
        else:
            print evt
        print
