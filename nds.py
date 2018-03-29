from datatypes import *

class NDS:
    def load(self,f):
        self.title=st(f,12)
        self.gamecode=st(f,4)
        self.makercode=st(f,2)
        self.unitcode=['NDS',None,'NDS+DSi','DSi'][u8(f)]
        self.seedsel=u8(f)
        self.devicecapacity=u8(f)
        f.read(9)
        self.romversion=u8(f)
        self.autostart=(u8(f)&0b00000100)!=0
        self.arm9romoffset=u32(f)
        self.arm9entryaddress=u32(f)
        self.arm9ramaddress=u32(f)
        self.arm9size=u32(f)
        self.arm7romoffset=u32(f)
        self.arm7entryaddress=u32(f)
        self.arm7ramaddress=u32(f)
        self.arm7size=u32(f)        
        self.fntoffset=u32(f)
        self.fntsize=u32(f)
        self.fatoffset=u32(f)
        self.fatsize=u32(f)
        self.arm9overlayoffset=u32(f)
        self.arm9overlaysize=u32(f)
        self.arm7overlayoffset=u32(f)
        self.arm7overlaysize=u32(f)
        self.p4001A4normal=u32(f)
        self.p4001A4KEY1=u32(f)
        self.iconoffset=u32(f)
        self.securechecksum=u16(f)
        self.securedelay=u16(f)
        self.arm9autoload=u32(f)
        self.arm7autoload=u32(f)
        self.securedisable=st(f,8)
        self.usedromsize=u32(f)
        self.headersize=u32(f)
        f.read(0x38)
        f.read(0x9C)
        self.logochecksum=u16(f)
        self.debugoffset=u32(f)
        self.debugsize=u32(f)
        self.debugaddress=u32(f)
    def __repr__(self):
        s=''
        for k in sorted(self.__dict__.keys()):
            if k =='securedelay':
                v=siprefix(self.__dict__[k]/130912.0)+'s'
            elif k=='devicecapacity':
                v=siprefix((128*1024)<<self.__dict__[k])+'iB'
            else:
                try:
                    v=str(hex(self.__dict__[k]))
                except:
                    v=str(self.__dict__[k])
            s+=(' '*20+k)[-20:]+':'+v
            s+='\n'
        return s
