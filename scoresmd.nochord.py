import re
import sys
import time
import wave
import math
import json
import copy
import struct
import random


trackinfo={
    82:{'ppqn':48,'tsig':[4,4],'minlen':6,'clef':{},'ign':[],'pre':{},'post':{},'stafftype':{}},
    #50:{'ppqn':48,'tsig':[4,4],'minlen':6,'clef':{12:'bass'},'ign':[4,13,14,15,16,17],'pre':{},'post':{},'stafftype':{}},
    32:{'ppqn':48,'tsig':[4,4],'minlen':6,'clef':{2:'bass',3:'bass',8:'bass'},'ign':[],'pre':{},'post':{},'stafftype':{}},
    16:{'ppqn':48,'tsig':[4,4],'minlen':6,'clef':{1:'bass',4:'bass',6:'"treble^8"'},'ign':[15],'pre':{},'post':{},'stafftype':{}},
    10:{'ppqn':32,'tsig':[3,4],'minlen':8,'clef':{1:'bass',6:'"treble^8"', 10:'"treble^8"'},'ign':[4,5,12,13,14,15,16],'pre':{},'post':{},'stafftype':{}},
    1:{'ppqn':32,'tsig':[3,4],'minlen':8,'clef':{2:'bass'},'ign':[],'pre':{},'post':{},'stafftype':{}},
    9:{'ppqn':32,'tsig':[12,8],'minlen':6,'clef':{},'ign':[],'pre':{},'post':{},'stafftype':{}}
}

dist=lambda x,i:((((i/2.0-abs(i/2.0-(x%i)))/i)**2))

from smd import SMD

with open(sys.argv[1],'rb') as f:
    sseq=SMD(f)

minlen=trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['minlen']
tsig=trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['tsig']
ppqn=trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['ppqn']
ppsn=ppqn
while ppsn/2==ppsn/2.0:
    #print ppsn
    ppsn/=2

maxtick=max([max([max([k[1][2] for k in j if k[0]=='note']+[0]) for j in i[1].values()])+i[0] for i in sseq.events.items()])
maxtick=maxtick+(ppqn*4)-maxtick%(ppqn*4)-1

tracks=17
tick=-1
dur=[0]*tracks
pnt=[0]*tracks
events=[[[] for j in xrange(max(sseq.events.keys()))] for i in xrange(12)]
sharps=[0,1,0,1,0,0,1,0,1,0,1,0]
notes='ccddeffggaab'
print '\\version "2.18.2"'
print '''\header {
  title = "%s"
}'''%(sys.argv[1],)
def p2s(freq):
    return notes[freq%12]+(','*((59-freq)/12) if freq<60 else '\''*((freq-48)/12))
def pn(freq,ndur,tie=False):
    if isinstance(freq, basestring):
        print freq+ndur+('~' if tie else '')
    else:
        print notes[freq%12]+(','*((59-freq)/12) if freq<60 else '\''*((freq-48)/12))+ndur+('~' if tie else '')

def draw_rest(t,dt):
    if dt==0:
        return
    if dt<ppsn:
        print '^"Caution: non-zero tiny rest (%i)"'%(dt,)
        return
    mmod=ppqn*4*tsig[0]/tsig[1]
    stm=t/mmod
    edm=(t+dt-1)/mmod
    stim=t%mmod
    if stim==0 and dt>mmod:
        mdurrd=int(dt/mmod)*mmod
        print 'R1*%i/%i*%i'%(tsig[0],tsig[1],dt/mmod)
        draw_rest(t+mdurrd,dt-mdurrd)
        return
    #print 't',t,'dt',dt,'m',stm,':',edm,'st',stim
    if edm!=stm:
        draw_rest(t,mmod-stim)
        draw_rest(t+mmod-stim,dt-mmod+stim)
        return
    if str(bin(dt/ppsn)).count('1')==1:
        print 'r'+str((ppqn*4)/dt)
        return
    lmbd=dt
    lmbd/=ppsn
    lmbd|=lmbd>>16
    lmbd|=lmbd>>8
    lmbd|=lmbd>>4
    lmbd|=lmbd>>2
    lmbd|=lmbd>>1
    lmbd^=lmbd>>1
    lmbd*=ppsn
    fnm=ppsn
    while fnm<lmbd:
        fnm*=2
        if t/(1.0*fnm)!=int(t/fnm):
            fnm/=2
            break
    if fnm>dt:
        print fnm,dt
        print 5/0
    draw_rest(t,fnm)
    draw_rest(t+fnm,dt-fnm)
    return
    print ' t',bin(t/ppsn),t
    print 'fn',bin(fnm/ppsn),fnm
    print 'dt',bin(dt/ppsn),dt
    print 'lm',bin(lmbd),lmbd
    print 'ed',bin((t+dt)/ppsn),t+dt
    print 5/0

def getlm(lmbd,ppsn):
    lmbd/=ppsn
    lmbd|=lmbd>>16
    lmbd|=lmbd>>8
    lmbd|=lmbd>>4
    lmbd|=lmbd>>2
    lmbd|=lmbd>>1
    lmbd^=lmbd>>1
    lmbd*=ppsn
    return lmbd

def draw_note(t,dt,pitch,tie=False):
    mmod=ppqn*4*tsig[0]/tsig[1]
    stm=t/mmod
    edm=(t+dt-1)/mmod
    stim=t%mmod
    #print 't',t,'dt',dt,'m',stm,':',edm,'st',stim,'p',pitch
    if edm!=stm:
        draw_note(t,mmod-stim,pitch,True)
        draw_note(t+mmod-stim,dt-mmod+stim,pitch,tie)
        return
    if re.search('10+1',str(bin(dt/ppsn))):
        lm=getlm(dt,ppsn)
        draw_note(t,lm,pitch,True)
        draw_note(t+lm,dt-lm,pitch,tie)
        return
    ostart=(t/ppsn)&(-(t/ppsn))
    olen=(dt/ppsn)&(-(dt/ppsn))
    if ostart!=0 and olen/ostart>=4:
        pass#print 'splitting because orders'
        #print 5/0
    lmbd=dt
    lmbd=getlm(lmbd,ppsn)
    nd=str(bin(dt/ppsn)).count('1')-1
    if nd==3:
        pass#print str(bin(dt/ppsn))
        #print 5/0
    ndur=str((ppqn*4)/lmbd)+'.'*nd
    '''if ndur=='2..':
        print lmbd, ndur, t,dt
        print 5/0'''
    pn(pitch,ndur,tie)
    return
    '''print ' t',bin(t/ppsn),t
    print 'os',bin(ostart),ostart
    print 'dt',bin(dt/ppsn),dt
    print 'ol',bin(olen),olen
    print 'lm',bin(lmbd),lmbd
    print 'ed',bin((t+dt)/ppsn),t+dt
    print 5/0'''

def round(number, multiple):
   return number+multiple/2 - ((number+multiple/2) % multiple)

events={}

tick=-1
dur=[0]*tracks
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
                        if dur[n]>=minlen:
                            ri=copy.deepcopy(i)
                            ri[1][2]=round(ri[1][2],minlen)
                            rtick=int(round(tick,minlen))
                            if rtick in events:
                                if n in events[rtick]:
                                    events[rtick][n].append(ri)
                                else:
                                    events[rtick][n]=[ri]
                            else:
                                events[rtick]={n:[ri]}
                            
                            
'''                    if i[0]=='tempo':
                        tempo=i[1][0]'''


ssp=[set() for i in xrange(tracks)]
spl=[[] for i in xrange(tracks)]
for n in xrange(tracks):
    #print n
    tick=-1
    while True:
        tick+=1
        if tick>maxtick:
            break
        if tick in events:
            if n in events[tick]:
                stt=tick
                edt=tick
                ct=tick
                nnum=0
                seen=[]
                csp=set()
                while True:
                    try:
                        for i in [e for e in events[ct][n] if e not in seen]:
                            seen.append(i)
                            edt=max(edt,ct+i[1][2]-1)
                            nnum+=1
                            csp.add(ct)
                            csp.add(ct+i[1][2])
                            break
                        else:
                            ct+=1
                            if ct>edt:
                                break
                            else:
                                continue
                    except KeyError:
                        ct+=1
                        if ct>edt:
                            break
                        else:
                            continue
                if nnum>1:
                    ssp[n].update(csp)
                    spl[n].append([stt,edt])
                    t=edt+1
nspl=[[] for i in xrange(tracks)]
for n in xrange(tracks):
    for e in spl[n]:
        if [i for i in xrange(e[0],e[1]+1) if i in events and n in events[i]]==[e[0]]:
            if list(set([i[1][2] for i in events[e[0]][n]]))==[e[1]-e[0]+1]:
                continue
        nspl[n].append(e)
spl=copy.deepcopy(nspl)
#print [sorted(list(i)) for i in ssp]
#print spl
while True:
    plen=sum([len(i) for i in spl])
    splt=[[] for i in xrange(tracks)]
    for n in xrange(tracks):
        mt=-1
        i=0
        while i<len(spl[n])-1:
            if spl[n][i][1]+1==spl[n][i+1][0]:
                splt[n].append([spl[n][i][0],spl[n][i+1][1]])
                i+=1
            else:
                splt[n].append(spl[n][i])
            i+=1
        if i==len(spl[n])-1:
            splt[n].append(spl[n][i])
    spl=copy.deepcopy(splt)
    if sum([len(i) for i in spl])==plen:
        break
#print spl[6]
#print [[i,events[i][6]] for i in xrange(maxtick) if i in events and 6 in events[i]]
for n in xrange(1,tracks):#[1,2,3,4,5,6,7,8,9,10]:
    for i in xrange(len(spl[n])-1):
        if spl[n][i][1]+1==spl[n][i+1][0]:
            print spl[n][i],spl[n][i+1]
            print 5/0
    if n in trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['ign']:
        continue
    try:
        print "\\new %sStaff  \\with {\ninstrumentName=#\"%i\"\n}\n{"%(trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['stafftype'][n],n)
    except KeyError:
        print "\\new Staff  \\with {\ninstrumentName=#\"%i\"\n}\n{"%(n,)
    print "\\compressFullBarRests"
    if n in trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['clef']:
        print '\\clef '+trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['clef'][n]
    print "\\time %i/%i"%(tsig[0],tsig[1])
    try:
        print trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['pre'][n]
    except KeyError:
        pass
    #print n
    tick=0
    #in_split=False
    split_start=-1
    split_end=-1
    while True:
        if tick>maxtick:
            break
        i0={i[0]:i[1] for i in spl[n]}
        if tick in i0:
            #print tick,i0[tick]
            assert (split_start==-1) == (split_end==-1)
            if split_start==-1 and split_end==-1:
                print '<<'
            else:
                print '\\\\'
            print '{%'+str(tick)
            split_start=tick
            split_end=i0[tick]
        if split_end!=-1 and tick==split_end+1:
            print '}%'+str(tick)
            if sum([len(events[t][n]) for t in xrange(split_start,split_end+1) if t in events and n in events[t]])>0:
                #print [(events[t][n]) for t in xrange(split_start,split_end+1) if t in events and n in events[t]]
                tick=split_start
                continue
            print '>>'
            split_start=-1
            split_end=-1
        dt=0
        while True:
            if tick+dt>maxtick:
                break
            try:
                note=events[tick+dt]
                note=note[n]
                assert len(note)>0
                break
            except KeyError as ex:
                dt+=1
                pass
            except AssertionError as ex:
                print ex,'a'
                dt+=1
                pass
        if tick<split_end and tick+dt>split_end:
            dt=split_end+1-tick
        draw_rest(tick,dt)
        tick+=dt
        if dt>0:
            continue
        #print tick
        #print events[tick][n]
        if split_start==-1 and split_end==-1:
            if len(events[tick][n])>1:
                pitches=[]
                for i in events[tick][n]:
                    pitches.append(i[1][0])
                pitch="<"+' '.join([p2s(i) for i in pitches])+">"
            else:
                pitch=events[tick][n][0][1][0]
            dt=events[tick][n][0][1][2]
            draw_note(tick,dt,pitch)
            del events[tick][n]
            if len(events[tick])==0:
                del events[tick]
        else:
            dt=events[tick][n][0][1][2]
            draw_note(tick,dt,events[tick][n][0][1][0])
            del events[tick][n][0]
            if len(events[tick][n])==0:
                del events[tick][n]
                if len(events[tick])==0:
                    del events[tick]
        tick+=dt
    try:
        print trackinfo[int(sys.argv[1].split('/')[-1][3:7])]['post'][n]
    except KeyError:
        pass
    print '}'

