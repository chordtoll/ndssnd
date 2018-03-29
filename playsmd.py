import sys
import time
import wave
import math
import json
import struct
import random



from smd import SMD

with open(sys.argv[1],'rb') as f:
    sseq=SMD(f)

maxtick=max([max([max([k[1][2] for k in j if k[0]=='note']+[0]) for j in i[1].values()])+i[0] for i in sseq.events.items()])

tracks=17
tick=-1
freq=[1]*tracks
amp=[1]*tracks
dur=[0]*tracks

sharps=[0,1,0,1,0,0,1,0,1,0,1,0]
notes='ccddeffggaab'
print '\\version "2.18.2" \n{'
while True:
    tick+=1
    if tick>max(sseq.events.keys()) and sum(dur)==0:
        break
    for i in xrange(tracks):
        if dur[i]==0:
            amp[i]=0
        else:
            dur[i]-=1
    if tick in sseq.events:
        for n in xrange(tracks):
            if n in sseq.events[tick]:
                for i in sseq.events[tick][n]:
                    if i[0]=='note':
                        freq[n]=i[1][0]
                        dur[n]=i[1][2]
                        amp[n]=i[1][1]/128.0
                        print 'note',i[1][0],i[1][2]
                        print notes[i[1][0]%12]+(','*((59-i[1][0])/12) if i[1][0]<60 else '\''*((i[1][0]-48)/12))
                    if i[0]=='tempo':
                        tempo=i[1][0]
print "}"
