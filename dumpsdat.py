import sys
import os
import json

from sdat import SDAT

typenames=['sseq','ssar','sbnk','swar','sply','sgrp','spl2','strm']

with open(sys.argv[1],'rb') as f:
    sdat=SDAT()
    sdat.load(f)
    #print '\n'.join([str(i) for i in sdat.info.records[0]])
    for i in xrange(len(sdat.symb.records[0])):
        try:
            print str(hex(i))+':'+str(sdat.symb.records[0][i])+':'+str(sdat.info.records[0][i].fileID)
        except Exception as e:
            pass
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    for t in xrange(8):
        if not os.path.exists(os.path.join(sys.argv[2],typenames[t])):
            os.mkdir(os.path.join(sys.argv[2],typenames[t]))
        if not os.path.exists(os.path.join(sys.argv[2],typenames[t]+'meta')):
            os.mkdir(os.path.join(sys.argv[2],typenames[t]+'meta'))
        if not os.path.exists(os.path.join(sys.argv[2],typenames[t],'num')):
            os.mkdir(os.path.join(sys.argv[2],typenames[t],'num'))
        if not os.path.exists(os.path.join(sys.argv[2],typenames[t]+'meta','num')):
            os.mkdir(os.path.join(sys.argv[2],typenames[t]+'meta','num'))
        for i in xrange(len(sdat.symb.records[t])):
            try:
                name=sdat.symb.records[t][i]
                fid=sdat.info.records[t][i].fileID
                start=sdat.fat.Rec[fid].nOffset
                size=sdat.fat.Rec[fid].nSize
                print "Dumping file",name,'('+str(fid)+') :',hex(start),'+',hex(size)
                with open(os.path.join(sys.argv[2],typenames[t],name),'wb') as of:
                    f.seek(start)
                    of.write(f.read(size))
                if not os.path.exists(os.path.join(sys.argv[2],typenames[t],'num',str(fid))):
                    os.link(os.path.join(sys.argv[2],typenames[t],name),os.path.join(sys.argv[2],typenames[t],'num',str(fid)))
                with open(os.path.join(sys.argv[2],typenames[t]+'meta',name),'wb') as of:
                    json.dump(sdat.info.records[t][i].__dict__,of)
                if not os.path.exists(os.path.join(sys.argv[2],typenames[t]+'meta','num',str(fid))):
                    os.link(os.path.join(sys.argv[2],typenames[t]+'meta',name),os.path.join(sys.argv[2],typenames[t]+'meta','num',str(fid)))
            except AttributeError as e:
                pass
