from datatypes import *
from ndsfileheader import NDSFileHeader

class SWD():
    def __init__(self,f):
        self.label=st(f,4)
        self.unk18=u32(f)
        self.flen=u32(f)
        self.version=u16(f)
        self.unk1=u8(f)
        self.unk2=u8(f)
        self.unk3=u32(f)
        self.unk4=u32(f)
        self.createtime=[u16(f),u8(f),u8(f),u8(f),u8(f),u8(f),u8(f)]
        self.fname=st(f,16)
        self.unk10=u32(f)
        self.unk11=u32(f)
        self.unk12=u32(f)
        self.unk13=u32(f)
        self.pcmdlen=u32(f)
        self.unk14=u16(f)
        self.nbwavislots=u16(f)
        self.nbprgislots=u16(f)
        self.unk17=u16(f)
        self.wavilen=u32(f)
        self.wavi=WAVI(f,self.nbwavislots)
    def __repr__(self):
        s=''
        for k in sorted(self.__dict__.keys()):
            if k =='symb':
                v='[SYMB]'
            elif k =='info':
                v='[INFO]'
            else:
                try:
                    v=str(hex(self.__dict__[k]))
                except:
                    v=str(self.__dict__[k])
            s+=(' '*20+k)[-20:]+':'+v
            s+='\n'
        return s
class chunk():
    def __init__(self,f):
        self.label=st(f,4)
        self.unka=u16(f)
        self.unkb=u16(f)
        self.chunkbeg=u32(f)
        self.chunksize=u32(f)
    def __repr__(self):
        s='\n'
        for k in sorted(self.__dict__.keys()):
            if k =='symb':
                v='[SYMB]'
            elif k =='info':
                v='[INFO]'
            else:
                try:
                    v=str(hex(self.__dict__[k]))
                except:
                    v=str(self.__dict__[k])
            s+='\t'+(' '*20+k)[-20:]+':'+v
            s+='\n'
        return s
class WAVI(chunk):
    def __init__(self,f,nbwavislots):
        chunk.__init__(self,f)
        wts=f.tell()
        self.WavTable=[u16(f) for i in xrange(nbwavislots)]
        self.SampleInfoTbl=[]
        for i in self.WavTable:
            if i==0:
                self.SampleInfoTbl.append(tnc())
            else:
                f.seek(wts+i)
                self.SampleInfoTbl.append(WAVISampleInfo(f))
class tnc():
    def __repr__(self):
        return ''
class WAVISampleInfo():
    def __init__(self,f):
        self.unk1=u16(f)
        self.ID=u16(f)
        self.ftune=s8(f)
        self.ctune=s8(f)
        self.rootkey=u8(f)
        self.ktps=s8(f)
        self.vol=s8(f)
        self.pan=s8(f)
        self.unk5=u8(f)
        self.unk58=u8(f)
        self.unk6=u16(f)
        self.unk7=u16(f)
        self.unk59=u16(f)
        self.smplfmt=u16(f)
        self.unk9=u8(f)
        self.smplloop=u8(f)
        self.unk10=u8(f)
        self.unk60=u8(f)
        self.unk11=u8(f)
        self.unk61=u8(f)
        self.unk12=u8(f)
        self.unk62=u8(f)
        self.unk13=u32(f)
        self.smplrate=u32(f)
        self.smplpos=u32(f)
        self.loopbeg=u32(f)
        self.looplen=u32(f)
        self.envon=u8(f)
        self.envmult=u8(f)
        self.unk19=u8(f)
        self.unk20=u8(f)
        self.unk21=u16(f)
        self.unk22=u16(f)
        self.atkvol=u8(f)
        self.attack=u8(f)
        self.decay=u8(f)
        self.sustain=u8(f)
        self.hold=u8(f)
        self.decay2=u8(f)
        self.release=u8(f)
        self.unk57=u8(f)
        print hex(self.unk1)
    def __repr__(self):
        s='\n'
        for k in sorted(self.__dict__.keys()):
            if k =='symb':
                v='[SYMB]'
            elif k =='info':
                v='[INFO]'
            else:
                try:
                    v=str(hex(self.__dict__[k]))
                except:
                    v=str(self.__dict__[k])
            s+='\t\t'+(' '*20+k)[-20:]+':'+v
            s+='\n'
        return s
