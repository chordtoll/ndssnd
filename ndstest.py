from nds import NDS
from nitro import Nitro

with open('roms/diamond.nds','rb') as f:
    nds=NDS()
    nds.load(f)
    print nds
    nitro=Nitro()
    nitro.load(f,nds)
    print nitro
