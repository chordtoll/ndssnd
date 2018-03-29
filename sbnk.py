from datatypes import *
from ndsfileheader import NDSFileHeader

import sys

class SBNK():
    def __init__(self,f):
        self.file=NDSFileHeader(f)
        self.type=st(f,4)
        self.nSize=u32(f)
        st(f,32)
        self.nCount=u32(f)
        self.Ins=[]
        for i in xrange(self.nCount):
            self.Ins.append(SBNKINS(f,self))
        [i.load(f) for i in self.Ins]
        self.wars=[]
        self.wavs=[{} for i in xrange(4)]
            
class SBNKINS():
    def __init__(self,f,parent):
        self.parent=parent
        self.fRecord=u8(f)
        self.nOffset=u16(f)
        u8(f)
    def iter(self,note,freq,dur,amp):
        print self.dict[note].__dict__
        if self.dict[note].swav in self.parent.wavs:
            wav=self.parent.wavs[self.dict[note].swav]
        else:
            self.parent.wavs=SWAR
        ticks=0
        while True:
            ticks+=1
            yield 32767.0*amp*((freq*ticks/44160)%1)
        
    def load(self,f):
        f.seek(self.nOffset)
        if self.fRecord==0:
            self.dict={}
            return
        if self.fRecord<16:
            rec=SBNKREC(f)
            self.dict={rec.note:rec}
            return
        if self.fRecord==16:
            lower=u8(f)
            upper=u8(f)
            a={}
            for i in xrange(lower,upper+1):
                u16(f)
                a[i]=SBNKREC(f)
            self.dict=a
            return
        if self.fRecord==17:
            regions=[u8(f) for i in xrange(8)]
            while regions[-1]==0:
                regions=regions[:-1]
            rs=0
            rr=[]
            for i in regions:
                rr.append([rs,i])
                rs=i+1
            a={}
            for i in rr:
                u16(f)
                rec=SBNKREC(f)
                for j in xrange(i[0],i[1]+1):
                    a[j]=rec
            self.dict=a
            return

class SBNKREC():
    def __init__(self,f):
        self.swav=u16(f)
        self.swar=u16(f)
        self.note=u8(f)
        self.attack=u8(f)
        self.decay=u8(f)
        self.sustain=u8(f)
        self.release=u8(f)
        self.pan=u8(f)

if __name__=="__main__":
    with open(sys.argv[1],'rb') as f:
        sbnk=SBNK(f)
        for j,i in enumerate(sbnk.Ins):
            print j
            print '\t'+'\n\t'.join([str(j)+':'+repr(i.load(f)[j].__dict__) for j in i.load(f)])
            
