from datatypes import *
from ndsfileheader import NDSFileHeader
from pcm import PCM

import sys

class SWAR():
    def __init__(self,f):
        self.file=NDSFileHeader(f)
        self.type=st(f,4)
        self.nSize=u32(f)
        st(f,32)
        self.nSample=u32(f)
        self.nOffset=[u32(f) for i in xrange(self.nSample)]
        self.samples=[]
        for i in self.nOffset:
            f.seek(i)
            self.samples.append(SWAV(f))
            
class SWAV():
    def __init__(self,f):
        self.info=SWAVINFO(f)
        size=(self.info.nLoopOffset+self.info.nNonLoopLen)*4
        self.data=[u8(f) for i in xrange(size)]
        self.pcm=PCM(self.data,self.info.nWaveType)
        
class SWAVINFO():
    def __init__(self,f):
        self.nWaveType=u8(f)
        self.bLoop=u8(f)
        self.nSampleRate=u16(f)
        self.nTime=u16(f)
        self.nLoopOffset=u16(f)
        self.nNonLoopLen=u16(f)

if __name__=="__main__":
    with open(sys.argv[1],'rb') as f:
        swar=SWAR(f)
        #for i in swar:
            #print i
        for i in swar.samples:
            print i.pcm.data
            print ' '*42200
        
            
