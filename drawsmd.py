import sys
import time
import wave
import math
import json
import struct
import random
import Image



from smd import SMD

with open(sys.argv[1],'rb') as f:
    sseq=SMD(f)

maxtick=max([max([max([k[1][2] for k in j if k[0]=='note']+[0]) for j in i[1].values()])+i[0] for i in sseq.events.items()])

img = Image.new( 'RGB', (maxtick+10,2176), "white") # create a new black image
pix = img.load()

tracks=17
tick=-1
freq=[1]*tracks
amp=[1]*tracks
dur=[0]*tracks

sharps=[0,1,0,1,0,0,1,0,1,0,1,0]

for t in xrange(tracks):
    for n in xrange(128):
        if sharps[n%12]==1:
            for tk in xrange(maxtick):
                pix[tk,(128-n)+128*t]=(192,192,192)

for x in xrange(0,maxtick,8):
    for y in xrange(2176):
        pix[x,y]=(192,255,192)

for x in xrange(0,maxtick,12):
    for y in xrange(2176):
        pix[x,y]=(224,224,255)
for x in xrange(0,maxtick,24):
    for y in xrange(2176):
        pix[x,y]=(192,192,255)
for x in xrange(0,maxtick,48):
    for y in xrange(2176):
        pix[x,y]=(128,128,255)
for x in xrange(0,maxtick,192):
    for y in xrange(2176):
        pix[x,y]=(0,0,255)

for n in xrange(tracks-1):
    for tk in xrange(maxtick):
        pix[tk,128+128*n]=(255,0,0)




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
                        if dur[n]==5:
                            for tk in xrange((tick/8)*8,((tick/8)*8)+8):
                                pix[tk,(128-i[1][0])+128*n]=(0,0,0)
                        if dur[n]==17:
                            for tk in xrange((tick/8)*8,((tick/8)*8)+16):
                                pix[tk,(128-i[1][0])+128*n]=(0,0,0)
                        else:
                            for tk in xrange(tick,tick+i[1][2]):
                                pix[tk,(128-i[1][0])+128*n]=(0,0,0)
                    if i[0]=='tempo':
                        tempo=i[1][0]
img.save(sys.argv[2])
