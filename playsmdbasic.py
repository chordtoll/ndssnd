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
#print sseq


#with open("tracks.json",'r') as f:
#    tracknums=json.load(f)
    
tn=xrange(17)
try:
    tn=tracknums[sys.argv[1].split('/')[-1]]
except:
    pass

SAMPLE_LEN=44160*15*60
noise_output = wave.open(sys.argv[2], 'w')
noise_output.setparams((2, 2, 44160, 0, 'NONE', 'not compressed'))

values = []

def ntofreq(n):
    return 440.0*2.0**((n-69)/12.0)
tracks=17


print tn

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
                    for n in tn:
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
print 20
