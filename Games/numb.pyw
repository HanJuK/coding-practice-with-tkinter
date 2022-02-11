#-*- coding: cp949 -*-
from Tkinter import *
import tkMessageBox
import winsound
import random

#variables for timer
countup_time="00:00:00"
counter_running=0
timer=[0,0,-1]
gameend=1

#attempt
attempt_cnt=0

#randnum
randnum=[0,0,0,0]

#trans
transparency=1
transparency_backup=1

#numbase class
class numbase():
    def __init__(self,master):
        #create menubar
        self.menu=Menu(root,tearoff=0)

        self.gamesubmenu=Menu(self.menu,tearoff=0)
        self.gamesubmenu.add_command(label=unicode("새 게임",'cp949'),command=self.newgame)
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_command(label=unicode("닫기",'cp949'),command=root.destroy)
        self.menu.add_cascade(label=unicode("게임",'cp949'),menu=self.gamesubmenu)

        self.helpsubmenu=Menu(self.menu,tearoff=0)
        self.helpsubmenu.add_command(label=unicode("조작키",'cp949'),command=lambda : tkMessageBox.showinfo(unicode("조작키",'cp949'),unicode("엔터키 : 입력\n\nF2 : 새 게임\nF3 : 메모장 초기화\nF4 : 창 숨기기/보이기",'cp949'),parent=root))
        self.menu.add_cascade(label=unicode("도움말",'cp949'),menu=self.helpsubmenu)

        root.config(menu=self.menu)

        #create top ui
        self.topui_frame=Frame(root)
        self.topui_frame.grid(row=0,sticky=E+W)

        self.timer_label=Label(self.topui_frame,font=("Verdana",10,"normal"),text=countup_time)
        self.timer_label.pack(side="left")

        self.attempt_label=Label(self.topui_frame,font=("Verdana",10,"normal"),text=attempt_cnt)
        self.attempt_label.pack(side="left",expand=True,padx=(0,10))

        self.trans_sdr=Scale(self.topui_frame,from_=0,to=100,orient=HORIZONTAL,showvalue=False,sliderlength=10,length=50,command=self.settransparency)
        self.trans_sdr.set(100)
        self.trans_sdr.pack(side="right")

        #create bottom ui
        self.bottomui_frame=Frame(root)
        self.bottomui_frame.grid(row=1)

        self.title_label=Label(self.bottomui_frame,font=(None,12,'bold'),text=unicode("4자리 숫자 입력",'cp949'))
        self.title_label.grid(row=0,columnspan=4)

        self.entrybox=Entry(self.bottomui_frame,font=("Verdana",18,"normal"),width=10,relief="solid",justify="center")
        self.entrybox.grid(row=1,columnspan=4,pady=(7,0))

        self.error_label=Label(self.bottomui_frame,font=(None,8,''),text='',fg="red")
        self.error_label.grid(row=2,columnspan=4)

        self.enterbtn=Button(self.bottomui_frame,font=(None,10,''),text=unicode("입력",'cp949'),width=13,relief="groove",command=self.getinput)
        self.enterbtn.place(x=63,y=81)

        self.giveupbtn=Button(self.bottomui_frame,font=(None,10,''),text=unicode("포기",'cp949'),relief="groove",command=self.gameover) ##command
        self.giveupbtn.place(x=179,y=81)

        self.result_label=Label(self.bottomui_frame,font=(None,8,''),text=unicode("결과:",'cp949'))
        self.result_label.grid(row=4,pady=(26,0),sticky=W)

        self.memo_label=Label(self.bottomui_frame,font=(None,8,''),text=unicode("메모:",'cp949'))
        self.memo_label.grid(row=4,column=2,pady=(26,0),sticky=W)

        self.resulttext=Text(self.bottomui_frame,font=(None,10,''),width=14,height=15,state=DISABLED)
        self.resultscroll=Scrollbar(self.bottomui_frame,command=self.resulttext.yview)
        self.resulttext.config(yscrollcommand=self.resultscroll.set)
        self.resulttext.grid(row=5)
        self.resultscroll.grid(row=5,column=1,sticky=N+S+W)

        self.memotext=Text(self.bottomui_frame,font=(None,10,''),width=20,height=15,undo=True)
        self.memoscroll=Scrollbar(self.bottomui_frame,command=self.memotext.yview)
        self.memotext.config(yscrollcommand=self.memoscroll.set)
        self.memotext.grid(row=5,column=2)
        self.memoscroll.grid(row=5,column=3,sticky=N+S+W)

        #create random number
        self.generate_randnum()

        #bind shortkeys
        root.bind('<F4>',lambda e : self.hidewindow())
        root.bind('<F2>',lambda e : self.newgame())
        root.bind('<F3>',lambda e : self.memotext.delete(1.0, END))
        self.entrybox.bind('<Return>',lambda e : self.getinput())

    #settransparency func
    def settransparency(self,val):
        global transparency
        transparency=int(val)/100.0
        root.attributes('-alpha',transparency)

    #hidewindow func
    def hidewindow(self):
        global transparency_backup

        #hide/unhide window
        if(transparency!=0):
            transparency_backup=transparency
            self.trans_sdr.set(0)
        else:
            self.trans_sdr.set(transparency_backup*100)

    #countup func(for timer)
    def countup(self):
        global countup_time,timer
        global counter_running

        #if game not yet started -> stop timer + ready for next timer to start
        if(gameend==1):
            counter_running=0
            self.timer_label.config(text=countup_time)
            #enable entry+buttons
            self.entrybox.config(state=NORMAL)
            self.enterbtn.config(state=NORMAL)
            self.giveupbtn.config(state=NORMAL)
            self.memotext.config(state=NORMAL)
            self.entrybox.bind('<Return>',lambda e : self.getinput())

            return None

        #start timer
        counter_running=1

        #update time
        timer[2]+=1
        if(timer[2]==60):
            timer[2]=0
            timer[1]+=1
        if(timer[1]==60):
            timer[1]=0
            timer[0]+=1

        #save time to string
        countup_time=str(timer[0]).zfill(2)+':'+str(timer[1]).zfill(2)+':'+str(timer[2]).zfill(2)

        #update every second
        self.timer_label.config(text=countup_time)
        root.after(1000,self.countup)

    #newgame func
    def newgame(self):
        global attempt_cnt
        global countup_time,timer,gameend

        #reset values
        gameend=1
        attempt_cnt=0
        timer=[0,0,-1]
        countup_time="00:00:00"
        self.timer_label.config(font=("Verdana",10,"normal"),text=countup_time)
        self.attempt_label.config(font=("Verdana",10,"normal"),text=attempt_cnt)
        self.entrybox.delete(0, END)
        self.resulttext.config(state=NORMAL)
        self.resulttext.delete(1.0, END)
        self.resulttext.config(state=DISABLED)
        self.memotext.delete(1.0, END)
        self.error_label.config(text='')

        #create a new random number
        self.generate_randnum()

        #re-activate buttons
        self.enterbtn.config(command=self.getinput)
        self.giveupbtn.config(command=self.gameover)
        self.entrybox.bind('<Return>',lambda e : self.getinput())

        #temporarily disable buttons(for timer sync)
        if(counter_running==1):
            self.timer_label.config(text="Loading..")
            self.entrybox.config(state=DISABLED)
            self.enterbtn.config(state=DISABLED)
            self.giveupbtn.config(state=DISABLED)
            self.memotext.config(state=DISABLED)
            self.entrybox.unbind('<Return>')

    #generate_randnum func
    def generate_randnum(self):
        global randnum

        #set variable
        self.temp=[]

        #first digit
        randnum[0]=random.randint(1,9)

        #rest of the digits
        while True:
            self.temp=random.sample(range(10),3)
            if(self.temp[0]==randnum[0] or self.temp[1]==randnum[0] or self.temp[2]==randnum[0]):
                continue
            else:
                randnum[1],randnum[2],randnum[3]=self.temp[0],self.temp[1],self.temp[2]
                break

        #end of func
        return None

    #calculate_result func
    def calculate_result(self,guess):
        #set variables
        self.ball_cnt=0
        self.strike_cnt=0
        self.out=0

        #calculate
        for i in range(4):
            for j in range(4):
                if(guess[i]==randnum[j]):
                    if(i==j):
                        self.strike_cnt+=1
                    else:
                        self.ball_cnt+=1

        if(self.ball_cnt+self.strike_cnt==0):
            self.out=1

        #return calculation
        return [self.ball_cnt,self.strike_cnt,self.out]

    #success func
    def success(self):
        global gameend
        gameend=1

        #bold text
        self.timer_label.config(font=("Verdana",10,"bold"))
        self.attempt_label.config(font=("Verdana",10,"bold"))

        #make buttons useless
        self.enterbtn.config(command=self.donothing)
        self.giveupbtn.config(command=self.donothing)
        self.entrybox.unbind('<Return>')

        #play success sound
        winsound.PlaySound("SystemAsterisk",winsound.SND_ASYNC)

    #gameover func
    def gameover(self):
        global gameend
        gameend=1

        #make buttons useless
        self.enterbtn.config(command=self.donothing)
        self.giveupbtn.config(command=self.donothing)
        self.entrybox.unbind('<Return>')

        #show answer
        self.resulttext.config(state=NORMAL)
        self.resulttext.insert(END,unicode("*****실패*****\n-[정답 : %d]-"%(randnum[0]*1000+randnum[1]*100+randnum[2]*10+randnum[3]),'cp949'))
        self.resulttext.config(state=DISABLED)
        self.resulttext.see("end")

        #play gameover sound
        winsound.PlaySound("SystemHand",winsound.SND_ASYNC)

    #donothong(literally)
    def donothing(self):
        return None

    #getinput func
    def getinput(self):
        global gameend
        global attempt_cnt

        #if somehow activated after the game has ended -> do nothing
        if(gameend==1 and self.resulttext.index(END)!="2.0"):
            return None

        #get input(check if relevant)
        self.guess=[0,0,0,0]
        self.repeat=0

        try:
            int(self.entrybox.get())+1

            if(int(self.entrybox.get())<1000):
                self.error_label.config(text=unicode("4자리 자연수를 입럭하시오.",'cp949'))
                return None
            elif(int(self.entrybox.get())>9999):
                self.error_label.config(text=unicode("4자리 자연수를 입럭하시오.",'cp949'))
                return None
            else:
                self.guess=[int(i) for i in str(self.entrybox.get())]
                for i in range(0,3):
                    for j in range(i+1,4):
                        if(self.guess[i]==self.guess[j]):
                            self.repeat=1
                            self.error_label.config(text=unicode("중복숫자 없이 입력하시오.",'cp949'))
                            return None
        except:
            self.error_label.config(text=unicode("숫자를 입럭하시오.",'cp949'))
            return None

        #start timer
        if(gameend==1 and counter_running==0):
            gameend=0
            self.countup()

        #update values
        attempt_cnt+=1
        self.attempt_label.config(text=attempt_cnt)
        self.entrybox.delete(0, END)
        self.error_label.config(text='')

        #do the calculation
        self.result=self.calculate_result(self.guess)

        #show the result
        if(self.result[2]==1):
            self.resulttext.config(state=NORMAL)
            self.resulttext.insert(END,"%d : OUT!\n"%(self.guess[0]*1000+self.guess[1]*100+self.guess[2]*10+self.guess[3]))
            self.resulttext.config(state=DISABLED)
            self.resulttext.see("end")
        elif(self.result[1]==4):
            self.resulttext.config(state=NORMAL)
            self.resulttext.insert(END,unicode("*****성공*****\n-[정답 : %d]-"%(randnum[0]*1000+randnum[1]*100+randnum[2]*10+randnum[3]),'cp949'))
            self.resulttext.config(state=DISABLED)
            self.resulttext.see("end")
            self.success()
        else:
            self.resulttext.config(state=NORMAL)
            self.resulttext.insert(END,"%d : %d B - %d S\n"%(self.guess[0]*1000+self.guess[1]*100+self.guess[2]*10+self.guess[3],self.result[0],self.result[1]))
            self.resulttext.config(state=DISABLED)
            self.resulttext.see("end")

#start program
root=None

def start():
    global countup_time,counter_running,timer,gameend
    global attempt_cnt
    global randnum
    global transparency,transparency_backup

    global root

    countup_time="00:00:00"
    counter_running=0
    timer=[0,0,-1]
    gameend=1

    attempt_cnt=0

    randnum=[0,0,0,0]

    transparency=1
    transparency_backup=1

    root = Tk()
    root.focus_force()
    root.title(unicode('숫자 야구게임','cp949'))
    root.resizable(0,0)
    basenum=numbase(root)
    root.mainloop()

if __name__ == '__main__':
    start()
