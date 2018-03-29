from datatypes import *
from ndsfileheader import NDSFileHeader
class SDAT:
    def load(self,f):
        self.file=NDSFileHeader(f)
        self.nSymbOffset=u32(f)
        self.nSymbSize=u32(f)
        self.nInfoOffset=u32(f)
        self.nInfoSize=u32(f)
        self.nFatOffset=u32(f)
        self.nFatSize=u32(f)
        self.nFileOffset=u32(f)
        self.nFileSize=u32(f)
        self.symb=SDATSYMB(f,self.nSymbOffset)
        self.info=SDATINFO(f,self.nInfoOffset)
        self.fat=SDATFAT(f,self.nFatOffset)
        
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

class SDATSYMB():
    def __init__(self,f,offset):
        f.seek(offset)
        self.type=st(f,4)
        self.nSize=u32(f)
        self.nRecOffset=[u32(f) for i in xrange(8)]
        f.read(24)
        self.records=[None]*8
        for i in xrange(8):
            self.records[i]=[]
            f.seek(offset+self.nRecOffset[i])
            if i==1:
                pass
            else:
                count=u32(f)
                offsets=[u32(f) for j in xrange(count)]
                for o in offsets:
                    if o==0:
                        self.records[i].append(None)
                    else:
                        f.seek(offset+o)
                        self.records[i].append(nt(f))
                
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SDATFAT():
    def __init__(self,f,offset):
        f.seek(offset)
        self.type=st(f,4)
        self.nSize=u32(f)
        self.nCount=u32(f)
        self.Rec=[SDATFATREC(f) for i in xrange(self.nCount)]
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SDATFATREC():
    def __init__(self,f):
        self.nOffset=u32(f)
        self.nSize=u32(f)
        u32(f)
        u32(f)
                
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SDATINFO():
    def __init__(self,f,offset):
        f.seek(offset)
        self.type=st(f,4)
        self.nSize=u32(f)
        self.nRecOffset=[u32(f) for i in xrange(8)]
        f.read(24)
        self.records=[None]*8
        for i in xrange(8):
            self.records[i]=[]
            f.seek(offset+self.nRecOffset[i])
            count=u32(f)
            offsets=[u32(f) for j in xrange(count)]
            for o in offsets:
                if o==0:
                    self.records[i].append(None)
                else:
                    f.seek(offset+o)
                    if i==0:
                        self.records[i].append(SDATINFOSSEQ(f))
                    elif i==2:
                        self.records[i].append(SDATINFOBANK(f))
                    elif i==3:
                        self.records[i].append(SDATINFOSWAR(f))
                    else:
                        self.records[i].append(None)
                
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SDATINFOSSEQ():
    def __init__(self,f):
        self.fileID=u16(f)
        u16(f)
        self.bnk=u16(f)
        self.vol=u8(f)
        self.cpr=u8(f)
        self.ppr=u8(f)
        self.ply=u8(f)
        u8(f)
        u8(f)
        
                
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SDATINFOBANK():
    def __init__(self,f):
        self.fileID=u16(f)
        u16(f)
        self.wa=[u16(f) for i in xrange(4)]
        
                
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])

class SDATINFOSWAR():
    def __init__(self,f):
        self.fileID=u16(f)
        u16(f)
        
                
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])


