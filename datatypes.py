def padhex(n,d):
    return ('0'*d+(str(hex(n))[2:].rstrip('L')))[-d:]

def siprefix(n,binary=True):
    pre=8
    prefixes='yzafpnum kMGTPEZY'
    while n<1:
        n*=1024 if binary else 1000
        pre-=1
    while n>1024 if binary else 1000:
        n/=1024.0 if binary else 1000.0
        pre+=1
    return str(int(n*10)/10.0)+prefixes[pre]

def st(f,n):
    return f.read(n).rstrip('\x00')

def nt(f):
    s=''
    while True:
        c=f.read(1)
        if c=='\x00':
            return s
        s+=c

def var(f):
    n=0
    c=0x100
    while c>0x7F:
        c=u8(f)
        n<<=7
        n|=c&0x7F
    return n

def u8(f):
    return ord(f.read(1))

def s8(f):
    n=u8(f)
    if n<0x80:
        return n
    return n-0x100

def u16(f):
    return u8(f)|(u8(f)<<8)

def u24(f):
    return u16(f)|(u8(f)<<16)
    
def u32(f):
    return u16(f)|(u16(f)<<16)

def swap(n,b):
    o=""
    s=('0'*b+hex(n)[2:])[-b*2:]
    while len(s)>0:
        print s,o
        o+=s[-2:]
        s=s[:-2]
    print o
    return int(o,16)
    
    
        
