from datatypes import *

class NDSFileHeader:
    def __init__(self,f):
        self.type=st(f,4)
        self.magic=u32(f)
        self.nFileSize=u32(f)
        self.nSize=u16(f)
        self.nBlock=u16(f)
    def __repr__(self):
        return ('\n '+' '*20).join([(' '*20+k)[-20:]+':'+str(hex(self.__dict__[k]) if isinstance(self.__dict__[k],int) else self.__dict__[k]) for k in sorted(self.__dict__.keys())])
