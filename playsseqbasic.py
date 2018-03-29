import sys
import time
import wave
import math
import struct
import random

from sseq import SSEQ

with open(sys.argv[1],'rb') as f:
    sseq=SSEQ(f)

SAMPLE_LEN=44160*15*60
noise_output = wave.open(sys.argv[2], 'w')
noise_output.setparams((2, 2, 44160, 0, 'NONE', 'not compressed'))

values = []

def ntofreq(n):
    return 440.0*2.0**((n-69)/12.0)
tracks=16
def generator():
    tick=0
    samplecounter=0
    tickcounter=0
    tempo=120
    freq=[1]*tracks
    amp=[1]*tracks
    dur=[0]*tracks
    sin=[0]*tracks
    tte=[0]*tracks
    tln=[0]*tracks
    while True:
        for n in xrange(tracks):
            sin[n]+=freq[n]*math.pi/44160
            if tte[n]>0:
                tte[n]-=1
            tln[n]+=1
        samplecounter+=1
        if samplecounter==184:
            samplecounter=0
            tickcounter+=tempo
            if tickcounter>240:
                tickcounter-=240
                tick+=1
                if tick%50==0:
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
                                    tte[n]=dur[n]*240/tempo*184
                                    amp[n]=i[1][1]/128.0
                                    sin[n]=0
                                    tln[n]=0
                                if i[0]=='tempo':
                                    tempo=i[1][0]
        yield sum([0.032767*amp[n]*(min(tte[n],1000)*min(tln[n],1000))*math.sin(sin[n]) for n in xrange(tracks)])/tracks

def generator():
    tick=-1
    samplecounter=0
    tickcounter=0
    tempo=120
    freq=[1]*tracks
    amp=[1]*tracks
    dur=[0]*tracks
    sinticks=0
    while True:
        sinticks+=1
        samplecounter+=1
        if samplecounter==234:
            samplecounter=0
            tickcounter+=tempo
            if tickcounter>240:
                tickcounter-=240
                tick+=1
                if tick%10==0:
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
                                if i[0]=='tempo':
                                    tempo=i[1][0]
                                    print tick,tempo
        yield sum([32767.0*amp[n]*((freq[n]*sinticks/44160)%1) for n in xrange(tracks)])/tracks
        

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
