from datatypes import *
from ndsfileheader import NDSFileHeader

class SSEQ():
    def __init__(self,f):
        self.file=NDSFileHeader(f)
        self.type=st(f,4)
        self.nSize=u32(f)
        self.nDataOffset=u32(f)
        self.events={}
        self.trackoffsets=[-1]*16
        callstack=[]
        curtrack=0
        curtick=0
        while True:
            stat=u8(f)
            if stat==0xFE:
                n=u16(f)
                self.tracksused=[((n&(1<<i))!=0) for i in xrange(16)]
                #print 'Tracks used:',self.tracksused
            elif stat==0x93:
                tn=u8(f)
                tad=u24(f)
                self.trackoffsets[tn]=tad
                #print 'Track',tn,'is at',hex(tad)
            elif stat==0xC7:
                poly=u8(f)==0
                #print 'Track',curtrack,'is','poly' if poly else 'mono'
            elif stat==0xE1:
                tempo=u16(f)
                self.addevent(curtrack,curtick,['tempo',[tempo]])
                #print 'Track',curtrack,'tempo is',tempo,curtick
            elif stat<0x80:
                vel=u8(f)
                dur=var(f)
                self.addevent(curtrack,curtick,['note',[stat,vel,dur]])
                #curtick+=dur
                #print 'Track',curtrack,'note',stat,'volume',vel,'for',dur,'ticks'
            elif stat==0x80:
                dur=var(f)
                curtick+=dur
                #print 'Track',curtrack,'rest for',dur,'ticks'
            elif stat==0x81:
                n=var(f)
                bank=n/256
                prog=n%256
                self.addevent(curtrack,curtick,['instrument',[bank,prog]])
                #print 'Track',curtrack,'bank',bank,'program',prog
            elif stat==0x94:
                addr=u24(f)
                #print 'Track',curtrack,'jump',hex(addr)
            elif stat==0x95:
                addr=u24(f)
                callstack.append(f.tell())
                f.seek(self.nDataOffset+addr)
                #print 'Track',curtrack,'call',hex(addr)
            elif stat==0xA1:
                ssb=u8(f)
                if ssb>=0xb0 and ssb<=0xbd:
                    u8(f)
                    n=u8(f)
                else:
                    n=u8(f)
                #print 'Track',curtrack,'A1',n
            elif stat==0xC0:
                n=u8(f)
                #print 'Track',curtrack,'pan is',n
            elif stat==0xC1:
                n=u8(f)
                #print 'Track',curtrack,'volume is',n
            elif stat==0xC4:
                n=u8(f)
                #print 'Track',curtrack,'pitch bend',n
            elif stat==0xC5:
                n=u8(f)
                #print 'Track',curtrack,'pitch bend range is',n
            elif stat==0xC6:
                n=u8(f)
                #print 'Track',curtrack,'priority is',n
            elif stat==0xCA:
                on=u8(f)==0
                #print 'Track',curtrack,'modulation depth is','on' if on else 'off'
            elif stat==0xCB:
                n=u8(f)
                #print 'Track',curtrack,'modulation speed is',n
            elif stat==0xCC:
                n=u8(f)
                #print 'Track',curtrack,'modulation type is',n
            elif stat==0xCD:
                n=u8(f)
                #print 'Track',curtrack,'modulation range is',n
            elif stat==0xCE:
                n=u8(f)
                #print 'Track',curtrack,'portamento is',n
            elif stat==0xCF:
                n=u8(f)
                #print 'Track',curtrack,'portamento time is',n
            elif stat==0xD5:
                n=u8(f)
                #print 'Track',curtrack,'expression is',n
            elif stat==0xE0:
                n=u16(f)
                #print 'Track',curtrack,'modulation delay is',n
            elif stat==0xFD:
                f.seek(callstack.pop())
                #print 'Track',curtrack,'return'
            elif stat==0xFF:
                dur=var(f)
                #print 'Track',curtrack,'end'
                curtrack+=1
                try:
                    while self.tracksused[curtrack]==False:
                        curtrack+=1
                except IndexError:
                    break
                f.seek(self.nDataOffset+self.trackoffsets[curtrack])
                curtick=0
            else:
                raise ValueError(str(hex(stat)))
    def addevent(self,track,tick,event):
        if tick in self.events:
            if track in self.events[tick]:
                self.events[tick][track].append(event)
            else:
                self.events[tick][track]=[event]
        else:
            self.events[tick]={track:[event]}
        
