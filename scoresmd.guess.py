import sys
import time
import wave
import math
import json
import struct
import random

dist=lambda x,i:((((i/2.0-abs(i/2.0-(x%i)))/i)**2))

from smd import SMD

with open(sys.argv[1],'rb') as f:
    sseq=SMD(f)

maxtick=max([max([max([k[1][2] for k in j if k[0]=='note']+[0]) for j in i[1].values()])+i[0] for i in sseq.events.items()])

tracks=17
tick=-1
dur=[0]*tracks
pnt=[0]*tracks
events=[[[] for j in xrange(max(sseq.events.keys()))] for i in xrange(12)]
sharps=[0,1,0,1,0,0,1,0,1,0,1,0]
notes='ccddeffggaab'
print '\\version "2.18.2"'
def pn(freq,ndur,tie=''):
    print notes[freq%12]+(','*((59-freq)/12) if freq<60 else '\''*((freq-48)/12))+ndur+tie

h=[0]*192

tick=-1
dur=[0]*tracks
print "\\new Staff {"
while True:
    tick+=1
    if tick>max(sseq.events.keys()) and sum(dur)==0:
        break
    for i in xrange(tracks):
        if dur[i]!=0:
            dur[i]-=1
    if tick in sseq.events:
        for n in xrange(tracks):
            if n in sseq.events[tick]:
                for i in sseq.events[tick][n]:
                    if i[0]=='note':
                        dur[n]=i[1][2]
                        if dur[n]>6:
                            for nl in xrange(1,192):
                                h[nl]+=dist(tick,nl)
                                h[nl]+=dist(tick+dur[n],nl)
                            
                            
                    if i[0]=='tempo':
                        tempo=i[1][0]
print "}"


"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import matplotlib.pyplot as plt

plt.plot(range(len(h))[6:65],[1.0/i if i!=0 else 0 for i in h[6:65]])
plt.savefig('out/'+(sys.argv[1].split('/')[-1])+'.png', bbox_inches='tight')

