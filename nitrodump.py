import sys
import os

from nds import NDS
from nitro import Nitro

with open(sys.argv[1],'rb') as f:
    nds=NDS()
    nds.load(f)
    nitro=Nitro()
    nitro.load(f,nds)
    toscan=[[0xF000,'']]
    while len(toscan)>0:
        curid,curpath=toscan.pop()
        print hex(curid),curpath
        if curid>len(nitro.dirs)+0xF000:
            continue
        for i in nitro.dirs[curid-0xF000].sub[::-1]:
            if i.isdir:
                toscan.append([i.id,os.path.join(curpath,i.name)])
                os.mkdir(os.path.join(sys.argv[2],curpath,i.name))
            else:
                with open(os.path.join(sys.argv[2],curpath,i.name),'wb') as of:
                    fat=nitro.fat[i.id]
                    f.seek(fat[0])
                    of.write(f.read(fat[1]-fat[0]))
