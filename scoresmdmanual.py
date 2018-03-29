import sys
import time
import wave
import math
import struct
import random
import curses
import asciimatics.screen
from random import randint

from smd import SMD

#with open(sys.argv[1],'rb') as f:
with open(r'fs\sky\SOUND\BGM\bgm0002.smd','rb') as f:
    sseq=SMD(f)


n1='CCDDEFFGGAAB'
n2=' # #  # # # '

def n2n(n):
    return n1[n%12]+('#' if n2[n%12]=='#' else '')+str((n/12)-1)

nbt=[{} for i in xrange(32)]

for e in sorted(sseq.events.keys()):
    for i in xrange(32):
        if i in sseq.events[e].keys():
            nbt[i][e]=sseq.events[e][i]



lasttick= max([max([j+i[j][0][1][2] if i[j][0][0]=='note' else j for j in i.keys()]+[0]) for i in nbt])
print lasttick
#print 5/0
STAFF_ROW_HEIGHT=4

STATE_PICK_PPQN=0
STATE_PICK_MEASURELEN=1
STATE_LAYOUT_MEASURE=2

ppqnar=[3,6,12,24,48,96,192,4,8,16,32,64,128,256]

mlenar=[1,2,3,4,6,8,12]

#lasttick=3000

CANVAS_WIDTH=1200
CANVAS_HEIGHT=600
CANVAS_SCROLL_WIDTH=lasttick
CANVAS_SCROLL_HEIGHT=2000

canvascolspan=16

from Tkinter import *

class App:

    def __init__(self, master):
        
        self.master=master


        frame=Frame(master,width=CANVAS_WIDTH,height=CANVAS_HEIGHT)
        frame.grid(column=0,row=0,columnspan=len(ppqnar))

        self.canvas = Canvas(frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,scrollregion=(0,0,CANVAS_SCROLL_WIDTH,CANVAS_SCROLL_HEIGHT))
        self.canvas.grid(column=0,row=0,columnspan=canvascolspan)
        hbar=Scrollbar(frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=CANVAS_WIDTH,height=CANVAS_HEIGHT)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        '''self.canvas = Canvas(master, width=800, height=200)
        self.canvas.grid(column=0,row=0,columnspan=len(ppqnar))'''

        '''self.canvas.create_line(0, 0, 200, 100)
        self.canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

        self.canvas.create_rectangle(50, 25, 150, 75, fill="blue")'''
        self.buttonarray0=[]
        self.buttonarray1=[]

        self.buttonconfirm=Button(master,text="Confirm",command=self.actionconfirm)
        self.buttonconfirm.grid(row=3,column=0,columnspan=canvascolspan/2)
        self.buttoncancel=Button(master,text="Cancel",command=self.actioncancel)
        self.buttoncancel.grid(row=3,column=canvascolspan/2,columnspan=canvascolspan/2)

        self.state=STATE_PICK_PPQN
        self.drawstate()
        self.button0(4)
        

    def drawstate(self):
        self.redraw_canvas()
        for i in self.buttonarray0:
            i.destroy()
        for i in self.buttonarray1:
            i.destroy()
        self.buttonarray0=[]
        self.buttonarray1=[]
        if self.state==STATE_PICK_PPQN:
            
            for i in xrange(len(ppqnar)):
                b=Button(self.master,text=str(ppqnar[i]),command=lambda i=i:self.button0(i))
                b.grid(row=1,column=i)
                self.buttonarray0.append(b)
        elif self.state==STATE_PICK_MEASURELEN:
            for i in xrange(len(mlenar)):
                b=Button(self.master,text=str(mlenar[i]),command=lambda i=i:self.button0(i))
                b.grid(row=1,column=i)
                self.buttonarray0.append(b)
        elif self.state==STATE_LAYOUT_MEASURE:
            b=Entry(self.master)
            b.bind("<Return>",(lambda event,b=b: self.processcommand(b)))
            b.grid(row=1,columnspan=canvascolspan)
            self.buttonarray0.append(b)

    def processcommand(self,entry):
        command=entry.get()
        e.delete(0, END)

    def actionconfirm(self):
        if self.state==STATE_PICK_PPQN:
            self.state=STATE_PICK_MEASURELEN
            self.drawstate()
            self.button0(3)
            return
        if self.state==STATE_PICK_MEASURELEN:
            self.state=STATE_LAYOUT_MEASURE
            self.instrument=0
            self.measure=0
            self.drawstate()
            return
    def actioncancel(self):
        pass
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units")
    def redraw_canvas(self):
        self.canvas.delete("all")
        if self.state in [STATE_PICK_PPQN,STATE_PICK_MEASURELEN]:
            for ins in xrange(16):
                self.draw_staff(0,20+ins*120,CANVAS_SCROLL_WIDTH)
                #for n in xrange(12):
                #    self.draw_note(20+15*n,20,n,10)
                for i in xrange(CANVAS_SCROLL_WIDTH):
                    if i in nbt[ins]:
                        for j in nbt[ins][i]:
                            if j[0]=='note':
                                self.draw_note(i,20+ins*120,j[1][0],j[1][2])
        if self.state in [STATE_LAYOUT_MEASURE]:
            ins=self.instrument
            self.draw_staff(0,200,CANVAS_SCROLL_WIDTH)
            for i in xrange(CANVAS_SCROLL_WIDTH):
                if i in nbt[ins]:
                    for j in nbt[ins][i]:
                        if j[0]=='note':
                            self.draw_note(i,200,j[1][0],j[1][2],False)
    def button0(self,btn):
        if self.state==STATE_PICK_PPQN:
            self.canvas.delete('gridline')
            print ppqnar[btn]
            for x in xrange(0,CANVAS_SCROLL_WIDTH,ppqnar[btn]):
                self.draw_staff_line(x,20)
            self.ppqn=ppqnar[btn]
        if self.state==STATE_PICK_MEASURELEN:
            self.mlen=mlenar[btn]
            for i in self.buttonarray1:
                i.destroy()
                self.master.update()
            self.buttonarray1=[]
            for i in xrange(mlenar[btn]):
                b=Button(self.master,text=str(i),command=lambda i=i:self.button1(i))
                b.grid(row=2,column=i)
                self.buttonarray1.append(b)
            self.button1(0)
    def button1(self,btn):
        if self.state==STATE_PICK_MEASURELEN:
            self.canvas.delete('gridline')
            for x in xrange(self.ppqn*btn,CANVAS_SCROLL_WIDTH,self.ppqn*self.mlen):
                self.draw_staff_line(x,20)
            self.moff=btn
    def draw_staff_line(self,x,y):
        self.canvas.create_line(x,y,x,CANVAS_SCROLL_HEIGHT,tag='gridline')
    def draw_staff(self,x,y,w):
        for h in xrange(11):
            if h==5:
                continue
            v=h*STAFF_ROW_HEIGHT*2
            self.canvas.create_line(x,y+v,x+w,y+v)

    def draw_note(self,x,y,n,w,forcefit=True):
        grey=False
        octave=n/12
        v=STAFF_ROW_HEIGHT*10-([0,0,1,1,2,3,3,4,4,5,5,6][n%12]*STAFF_ROW_HEIGHT)
        if forcefit:
            v+=(7-octave)*7*STAFF_ROW_HEIGHT
            while (v<0):
                v+=7*STAFF_ROW_HEIGHT
                grey=True
            while (v>3*7*STAFF_ROW_HEIGHT):
                v-=7*STAFF_ROW_HEIGHT
                grey=True
        else:
            v+=(7-octave)*7*STAFF_ROW_HEIGHT
        if n2[n%12]=='#':
            self.canvas.create_line(x,y+v-STAFF_ROW_HEIGHT/2,x+3,y+v-STAFF_ROW_HEIGHT/2,width=3,fill='#000' if not grey else '#888')
            self.canvas.create_line(x,y+v-STAFF_ROW_HEIGHT/2,x+w,y+v-STAFF_ROW_HEIGHT/2,width=1,fill='#000' if not grey else '#888')
        else:
            self.canvas.create_line(x,y+v,x+3,y+v,width=5,fill='#000' if not grey else '#888')
            self.canvas.create_line(x,y+v,x+w,y+v,width=3,fill='#000' if not grey else '#888')

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below
