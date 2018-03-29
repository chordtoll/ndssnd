ima_index_table=[  -1, -1, -1, -1, 2, 4, 6, 8,
                   -1, -1, -1, -1, 2, 4, 6, 8]

ima_step_table=[7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
	            19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
	            50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
	            130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
	            337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
	            876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
	            2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
	            5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
	            15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767   ]

def u16(a,i):
    return i+2,a[i]+a[i+1]*256

def u4(a,i,h):
    if h==0:
        return i,1,a[i]%16
    else:
        return i+1,0,a[i]>>4

class PCM():
    def __init__(self,data,type):
        self.data=[]
        if type==0:
            print 5/0
        if type==1:
            print 5/0
        if type==2:
            aidx=0
            hidx=0
            aidx,predictor=u16(data,aidx)
            aidx,sidx=u16(data,aidx)
            s=""
            while aidx<len(data):
                step=ima_step_table[sidx]
                aidx,hidx,n=u4(data,aidx,hidx)
                sidx=min(max(sidx+ima_index_table[n],0),88)
                if n<7:
                    n=n-16
                diff=(n+0.5)*(step/4)
                predictor=min(max(predictor+diff,-32768),32767)
                s+=chr(int((predictor+32768))/256)
                s+=chr(int((predictor+32768))%256)
            self.data=s
                
