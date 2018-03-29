from datatypes import *

class Nitro:
    def load(self,f,nds):
        self.fat=[]
        f.seek(nds.fatoffset)
        for i in xrange(nds.fatsize/8):
            self.fat.append([u32(f),u32(f)])
        f.seek(nds.fntoffset+6)
        fntnumdirs=u16(f)
        f.seek(nds.fntoffset)
        self.dirs=[]
        for i in xrange(fntnumdirs):
            self.dirs.append(FNTMainEntry(0xF000+i,u32(f),u16(f),u16(f)))
        for i in self.dirs:
            i.loadsub(f,nds.fntoffset)
        return
        for i in self.dirs:
            print i
            for j in i.sub:
                print '   ',j
        
    def __repr__(self):
        s=''
        for k in sorted(self.__dict__.keys()):
            if k =='fat':
                v='[FAT]'
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

class FNTMainEntry():
    def __init__(self,id,offset,ffid,parent):
        self.id=id
        self.offset=offset
        self.ffid=ffid
        self.parent=parent
    def loadsub(self,f,fntoff):
        self.sub=[]
        id=self.ffid
        f.seek(fntoff+self.offset)
        while True:
            tlen=u8(f)
            if tlen==0x00:
                break
            name=st(f,tlen&0b01111111)
            if tlen<0x80:
                ciid=id
                id+=1
                isdir=False
            else:
                ciid=u16(f)
                isdir=True
            self.sub.append(FileEntry(ciid,name,isdir))
                
    def __repr__(self):
        return padhex(self.id,4)+' @ '+padhex(self.offset,8)+' ('+padhex(self.ffid,4)+' - '+') : '+padhex(self.parent,4)

class FileEntry():
    def __init__(self,id,name,isdir=False):
        self.id=id
        self.name=name
        self.isdir=isdir
    def __repr__(self):
        return padhex(self.id,4)+' : '+self.name+(' (D)' if self.isdir else '')
