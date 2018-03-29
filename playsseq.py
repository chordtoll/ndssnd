import os
import sys
import time
import wave
import math
import json
import struct
import random

from sseq import SSEQ
from sbnk import SBNK

with open(os.path.join('sdat','sseq',sys.argv[1]),'rb') as f:
    sseq=SSEQ(f)
with open(os.path.join('sdat','sseqmeta',sys.argv[1]),'rb') as f:
    sseqmeta=json.load(f)
print sseqmeta
sseqmeta['bnk']=1305
with open(os.path.join('sdat','sbnk','num',str(sseqmeta['bnk']))) as f:
    sbnk=SBNK(f)
with open(os.path.join('sdat','sbnkmeta','num',str(sseqmeta['bnk']))) as f:
    sbnkmeta=json.load(f)
print sbnkmeta
sbnk.wavs=sbnkmeta['wa']

SAMPLE_LEN=44160*15*60
noise_output = wave.open(sys.argv[2], 'w')
noise_output.setparams((2, 2, 44160, 0, 'NONE', 'not compressed'))

values = []

def ntofreq(n):
    return 440.0*2.0**((n-69)/12.0)
tracks=1

def generator():
    tick=-1
    samplecounter=0
    tickcounter=0
    tempo=120
    freq=[1]*tracks
    amp=[1]*tracks
    dur=[0]*tracks
    instrument=[None]*tracks
    noteiter=[None]*tracks
    nt=0
    while True:
        nt+=1
        samplecounter+=1
        if samplecounter==234:
            samplecounter=0
            tickcounter+=tempo
            if tickcounter>240:
                tickcounter-=240
                tick+=1
                print sys.argv[1],tick,'/',max(sseq.events.keys())
                if tick>max(sseq.events.keys()) and sum(dur)==0:
                    yield None
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
                                    freq[n]=ntofreq(i[1][0])
                                    dur[n]=i[1][2]
                                    amp[n]=i[1][1]/128.0
                                    noteiter[n]=instrument[n].iter(i[1][0],freq[n],dur[n],amp[n])
                                if i[0]=='tempo':
                                    tempo=i[1][0]
                                if i[0]=='instrument':
                                    assert (i[1][0]==0)
                                    instrument[n]=sbnk.Ins[i[1][1]]
                #print noteiter
        if nt>44160*40:
            yield sum([noteiter[n].next() for n in xrange(tracks) if noteiter[n] is not None])/tracks
        else:
            sum([noteiter[n].next() for n in xrange(tracks) if noteiter[n] is not None])/tracks
        

f=440
g=generator()
for i in range(0, SAMPLE_LEN):
        value = g.next()#32767.0*math.sin(f*i*math.pi/22080)#random.randint(-32767, 32767)
        if value is None:
            break
        packed_value = struct.pack('h', value)
        values.append(packed_value)
        values.append(packed_value)

value_str = ''.join(values)
noise_output.writeframes(value_str)

noise_output.close()

generator()
