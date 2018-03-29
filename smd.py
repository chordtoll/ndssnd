from datatypes import *
from ndsfileheader import NDSFileHeader

class SMD():
    def __init__(self,f):
        self.label=st(f,4)
        self.unk7=u32(f)
        self.flen=u32(f)
        self.version=u16(f)
        self.unk1=u8(f)
        self.unk2=u8(f)
        self.unk3=u32(f)
        self.unk4=u32(f)
        self.createtime=[u16(f),u8(f),u8(f),u8(f),u8(f),u8(f),u8(f)]
        self.fname=st(f,16)
        self.unk5=u32(f)
        self.unk6=u32(f)
        self.unk8=u32(f)
        self.unk9=u32(f)
        self.song=SONG(f)
        self.trks=[]
        for i in xrange(self.song.nbtrks):
            self.trks.append(TRK(f))
        self.events={}
        for j,i in enumerate(self.trks):
            for e in i.events:
                self.addevent(j,e[0],e[1])
    def addevent(self,track,tick,event):
        if tick in self.events:
            if track in self.events[tick]:
                self.events[tick][track].append(event)
            else:
                self.events[tick][track]=[event]
        else:
            self.events[tick]={track:[event]}
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SONG():
    def __init__(self,f):
        self.label=st(f,4)
        assert(self.label=="song")
        self.unk1=u32(f)
        self.unk2=u32(f)
        self.unk3=u32(f)
        self.unk4=u16(f)
        self.tpqn=u16(f)
        #print self.tpqn
        self.unk5=u16(f)
        self.nbtrks=u8(f)
        self.nbchans=u8(f)
        self.unk6=u32(f)
        self.unk7=u32(f)
        self.unk8=u32(f)
        self.unk9=u32(f)
        self.unk10=u16(f)
        self.unk11=u16(f)
        self.unk12=u32(f)
        self.unkpad=st(f,16)

resttab=[96,  72,  64,  48,  36,  32,  24,  18,  16,  12,   9,   8,  6,   4,   3,   2]
restnam=['1/2','3/8','1/3','1/4','3/16','1/6','1/8','3/32','1/12','1/16','3/64','1/24','1/32','3/128','1/48','1/64']

class TRK():
    def __init__(self,f):
        self.label=st(f,4)
        assert(self.label=="trk\x20")
        self.param1=u32(f)
        self.param2=u32(f)
        self.chunklen=u32(f)
        curloc=f.tell()
        self.trkid=u8(f)
        self.chanid=u8(f)
        self.unk1=u8(f)
        self.unk2=u8(f)
        self.events=[]
        curtick=0
        curoct=0
        prevdur=0
        prevpause=0
        nvol=255
        nexpr=255
        while True:
            event=u8(f)
            if event<0x80:
                npel=u8(f)
                octmod=(npel>>4)&0x3
                curoct+=octmod-2
                parlen=npel>>6
                note=npel&0x0F
                dur=0
                if parlen==0:
                    dur=prevdur
                else:
                    for i in xrange(parlen):
                        dur=dur<<8
                        dur|=u8(f)
                prevdur=dur
                self.events.append([curtick,['note',[12*(curoct)+note,(nvol*nexpr)/256,dur]]])
                #print hex(event)+':Track',self.trkid,'note',12*(curoct+1)+note,'for',dur,"at tick",curtick
                #curtick+=dur
            elif event<0x90:
                #print hex(event)+':Track',self.trkid,'rest',restnam[event-0x80],"at tick",curtick
                curtick+=resttab[event-0x80]
            elif event==0x90:
                expr=prevpause
                #print hex(event)+':Track',self.trkid,'pause',expr,"at tick",curtick
                prevpause=expr
                curtick+=expr
            elif event==0x91:
                expr=prevpause+s8(f)
                #print hex(event)+':Track',self.trkid,'pause',expr,"at tick",curtick
                prevpause=expr
                curtick+=expr
            elif event==0x92:
                expr=u8(f)
                #print hex(event)+':Track',self.trkid,'pause',expr,"at tick",curtick
                prevpause=expr
                curtick+=expr
            elif event==0x93:
                expr=u16(f)
                #print hex(event)+':Track',self.trkid,'pause',expr,"at tick",curtick
                prevpause=expr
                curtick+=expr
            elif event==0x98:
                #print hex(event)+':Track',self.trkid,'EOT',"at tick",curtick
                break
            elif event==0x99:
                pass
                #print hex(event)+':Track',self.trkid,'loops at',"at tick",curtick
            elif event==0x9C:
                expr=u8(f)
            elif event==0x9D:
                pass
            elif event==0xA0:
                expr=u8(f)
                curoct=expr
                #print hex(event)+':Track',self.trkid,'octave',expr,"at tick",curtick
            elif event==0xA4:
                expr=u8(f)
                self.events.append([curtick,['tempo',[expr]]])
                #print hex(event)+':Track',self.trkid,'tempo',expr,"at tick",curtick
            elif event==0xA8:
                expr=u16(f)
            elif event==0xA9:
                expr=u8(f)
                #print hex(event)+':Track',self.trkid,'unknown',expr,"at tick",curtick
            elif event==0xAA:
                expr=u8(f)
                #print hex(event)+':Track',self.trkid,'unknown',expr,"at tick",curtick
            elif event==0xAC:
                expr=u8(f)
                #print hex(event)+':Track',self.trkid,'instrument',expr,"at tick",curtick
            elif event==0xB2:
                expr=u8(f)
            elif event==0xB4:
                expr=u16(f)
            elif event==0xB5:
                expr=u8(f)
            elif event==0xB6:
                expr=u8(f)
            elif event==0xBE:
                expr=u8(f)
            elif event==0xBF:
                expr=u8(f)
            elif event==0xC0:
                pass
            elif event==0xD0:
                expr=u8(f)
            elif event==0xD1:
                expr=u8(f)
            elif event==0xD2:
                expr=u8(f)
            elif event==0xD4:
                expr=u24(f)
            elif event==0xD6:
                expr=u16(f)
            elif event==0xD7:
                expr=u16(f)
                #print hex(event)+':Track',self.trkid,'pitchbend',expr,"at tick",curtick
            elif event==0xDB:
                expr=u8(f)
            elif event==0xDC:
                expr=u8(f)
                expr=u32(f)
            elif event==0xE0:
                expr=u8(f)
                nvol=expr
                #print hex(event)+':Track',self.trkid,'volume',expr,"at tick",curtick
            elif event==0xE2:
                expr=u24(f)
            elif event==0xE3:
                expr=u8(f)
                nexpr=expr
                #print hex(event)+':Track',self.trkid,'expression',expr,"at tick",curtick
            elif event==0xE8:
                expr=u8(f)
                #print hex(event)+':Track',self.trkid,'pan',expr,"at tick",curtick
            elif event==0xEA:
                expr=u24(f)
            elif event==0xF6:
                expr=u8(f)
            else:
                print "unknown event",hex(event)
                assert(False)
        f.seek(curloc+self.chunklen)
        self.pad=st(f,(0 if self.chunklen%4==0 else (4-(self.chunklen%4))))
