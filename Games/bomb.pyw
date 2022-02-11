#-*- coding: cp949 -*-
from Tkinter import *
import tkMessageBox
import winsound
import random

#x,y,mines (numbers), flag_cnt #8 8 10 / 16 16 40 / 24 24 99 / max : 30 30 900
number_of_x=8
number_of_y=8
number_of_mines=10
flag_cnt=0

#mode(for custom not changing)
mode=0

#variables for timer
countup_time="00:00:00"
counter_running=0
timer=[0,0,-1]
gameend=1

#variables for multiclick
left_state=0
right_state=0

#variables for trans
transparency=1
transparency_backup=1 #NEW

#minesweeper game
class mine():
    def __init__(self,master):
        #create buttons
        self.button_frame=Frame(root)
        self.button_frame.grid(row=1)
        self.buttons()

        #create menubar
        self.v=IntVar()
        self.v.set(0)

        self.menu=Menu(root,tearoff=0)
        self.gamesubmenu=Menu(self.menu,tearoff=0)
        self.gamesubmenu.add_command(label=unicode("새 게임",'cp949'),command=self.newgame)
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_radiobutton(label=unicode("초급",'cp949'),variable=self.v,value=0,command=lambda : self.restart(8,8,10))
        self.gamesubmenu.add_radiobutton(label=unicode("중급",'cp949'),variable=self.v,value=1,command=lambda : self.restart(16,16,40))
        self.gamesubmenu.add_radiobutton(label=unicode("고급",'cp949'),variable=self.v,value=2,command=lambda : self.restart(24,24,99))
        self.gamesubmenu.add_radiobutton(label=unicode("사용자 지정",'cp949'),variable=self.v,value=3,command=self.customgrid_ui)
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_command(label=unicode("닫기",'cp949'),command=root.destroy)
        self.menu.add_cascade(label=unicode("게임",'cp949'),menu=self.gamesubmenu)

        self.helpsubmenu=Menu(self.menu,tearoff=0)
        self.helpsubmenu.add_command(label=unicode("조작키",'cp949'),command=lambda : tkMessageBox.showinfo(unicode("조작키",'cp949'),unicode("좌클릭 : 칸 열기\n우클릭 : 깃발 꽂기\n스크롤 휠 클릭 : 물음표 표기\n좌클릭+우클릭 : 주변의 지뢰 수와 깃발 수가 일치할 경우 작동 / 깃발의 위치와 지뢰의 위치가 일치할 경우, 주변의 닫혀있는 칸 전부 열기 / 일치하지 않을 시 게임 오버\n\nF2 : 새 게임\nF4 : 창 숨기기/보이기",'cp949'),parent=root))
        self.menu.add_cascade(label=unicode("도움말",'cp949'),menu=self.helpsubmenu)

        root.config(menu=self.menu)

        #create top ui
        self.topui_frame=Frame(root)
        self.topui_frame.grid(row=0,sticky=E+W)

        self.timer_label=Label(self.topui_frame,font=("Verdana",10,"normal"),text=countup_time)
        self.timer_label.pack(side="left")

        self.mine_label=Label(self.topui_frame,font=("Verdana",10,"normal"),text=str(number_of_mines-flag_cnt))
        self.mine_label.pack(side="left",expand=True,padx=(0,11))

        self.trans_sdr=Scale(self.topui_frame,from_=0,to=100,orient=HORIZONTAL,showvalue=False,sliderlength=10,length=50,command=self.settransparency)
        self.trans_sdr.set(100)
        self.trans_sdr.pack(side="right")

        #bind shortkeys
        root.bind('<F4>',lambda e : self.hidewindow())
        root.bind('<F2>',lambda e : self.newgame())

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

    #buttons func -> generate buttons(for restart)
    def buttons(self):
        #Buttons 2-dimentional array
        self.G_buttons=[[0]*number_of_x for i in range(number_of_y)]
        #generate random mines
        self.G_mines=random.sample(range(number_of_x*number_of_y),number_of_mines)

        #create buttons, mark mines, bind functions
        for i in range(0,number_of_x*number_of_y):
            #declare buttons + place buttons + bind left command / [0]:Button,[1]:reveal=1or0,[2]:number=0~8/for mine =10,[3]:flag=1or0
            self.G_buttons[i/number_of_x][i%number_of_x]=[Button(self.button_frame,font=("consolas",10,"bold"),text="",width=2,height=1,command=lambda y=i/number_of_x, x=i%number_of_x : self.left(y,x)),0,0,0]
            self.G_buttons[i/number_of_x][i%number_of_x][0].grid(row=i/number_of_x,column=i%number_of_x)

            #set mines
            for j in range(0,number_of_mines):
                if(self.G_mines[j]==i):
                    self.G_buttons[i/number_of_x][i%number_of_x][2]=10 #10 equals mine

            #bind functions to buttons
            self.G_buttons[i/number_of_x][i%number_of_x][0].bind('<Button-1>',lambda e, y=i/number_of_x, x=i%number_of_x : self.lefton(y,x))
            self.G_buttons[i/number_of_x][i%number_of_x][0].bind('<ButtonRelease-1>',lambda e : self.leftrelease())

            self.G_buttons[i/number_of_x][i%number_of_x][0].bind('<Button-2>',lambda e, y=i/number_of_x, x=i%number_of_x : self.middle(y,x))

            self.G_buttons[i/number_of_x][i%number_of_x][0].bind('<Button-3>',lambda e, y=i/number_of_x, x=i%number_of_x : [self.righton(y,x),self.right(y,x)])
            self.G_buttons[i/number_of_x][i%number_of_x][0].bind('<ButtonRelease-3>',lambda e : self.rightrelease())

        #calculate numbers(regarding mines)
        for i in range(0,number_of_x*number_of_y):
            if(self.G_buttons[i/number_of_x][i%number_of_x][2]==10):
                if(i/number_of_x-1>=0 and i%number_of_x-1>=0):                      #one
                    if(self.G_buttons[i/number_of_x-1][i%number_of_x-1][2]!=10):
                        self.G_buttons[i/number_of_x-1][i%number_of_x-1][2]+=1
                if(i%number_of_x-1>=0):                                             #two
                    if(self.G_buttons[i/number_of_x][i%number_of_x-1][2]!=10):
                        self.G_buttons[i/number_of_x][i%number_of_x-1][2]+=1
                if(i/number_of_x+1<number_of_y and i%number_of_x-1>=0):             #three
                    if(self.G_buttons[i/number_of_x+1][i%number_of_x-1][2]!=10):
                        self.G_buttons[i/number_of_x+1][i%number_of_x-1][2]+=1
                if(i/number_of_x-1>=0):                                             #four
                    if(self.G_buttons[i/number_of_x-1][i%number_of_x][2]!=10):
                        self.G_buttons[i/number_of_x-1][i%number_of_x][2]+=1
                if(i/number_of_x+1<number_of_y):                                    #five
                    if(self.G_buttons[i/number_of_x+1][i%number_of_x][2]!=10):
                        self.G_buttons[i/number_of_x+1][i%number_of_x][2]+=1
                if(i/number_of_x-1>=0 and i%number_of_x+1<number_of_x):             #six
                    if(self.G_buttons[i/number_of_x-1][i%number_of_x+1][2]!=10):
                        self.G_buttons[i/number_of_x-1][i%number_of_x+1][2]+=1
                if(i%number_of_x+1<number_of_x):                                    #seven
                    if(self.G_buttons[i/number_of_x][i%number_of_x+1][2]!=10):
                        self.G_buttons[i/number_of_x][i%number_of_x+1][2]+=1
                if(i/number_of_x+1<number_of_y and i%number_of_x+1<number_of_x):    #eight
                    if(self.G_buttons[i/number_of_x+1][i%number_of_x+1][2]!=10):
                        self.G_buttons[i/number_of_x+1][i%number_of_x+1][2]+=1
        #testing
##        for i in range(0,number_of_x*number_of_y):
##            if not(self.G_buttons[i/number_of_x][i%number_of_x][2]==10):
##                self.G_buttons[i/number_of_x][i%number_of_x][0].config(text=str(self.G_buttons[i/number_of_x][i%number_of_x][2]),fg="black")
##            else:
##                self.G_buttons[i/number_of_x][i%number_of_x][0].config(bg="blue")

    #countup func(for timer)
    def countup(self):
        global countup_time,timer
        global counter_running

        #if game not yet started -> stop timer + ready for next timer to start
        if(gameend==1):
            counter_running=0
            self.timer_label.config(text=countup_time)
            #enable buttons
            for i in range(0,number_of_x*number_of_y):
                self.G_buttons[i/number_of_x][i%number_of_x][0].config(state=NORMAL)

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

    #newgame func(for New game 100%/retry/etc)
    def newgame(self):
        global countup_time,timer
        global gameend,flag_cnt

        #destroy previous grid
        for i in range(0,number_of_x*number_of_y):
            self.G_buttons[i/number_of_x][i%number_of_x][0].destroy()

        #reset values
        gameend=1
        flag_cnt=0
        timer=[0,0,-1]
        countup_time="00:00:00"
        self.timer_label.config(font=("Verdana",10,"normal"),text=countup_time)
        self.mine_label.config(text=str(number_of_mines-flag_cnt),fg="black")

        #make new grid
        self.buttons()

        #temporarily disable buttons(for timer sync)
        if(counter_running==1):
            self.timer_label.config(text="Loading..")
            for i in range(0,number_of_x*number_of_y):
                self.G_buttons[i/number_of_x][i%number_of_x][0].config(state=DISABLED)

    #restart func(for difficulty change)
    def restart(self,xn,yn,mn):
        global number_of_x,number_of_y,number_of_mines
        global mode
        global countup_time,timer
        global gameend,flag_cnt

        #if already mode -> no nothing / except custom
        if(xn==number_of_x and yn==number_of_y and mn==number_of_mines):
            if(self.v.get()!=3 and mode!=3):
                return None

        #destroy previous grid
        for i in range(0,number_of_x*number_of_y):
            self.G_buttons[i/number_of_x][i%number_of_x][0].destroy()

        #new variables(numbers)
        number_of_x=xn
        number_of_y=yn
        number_of_mines=mn

        #reset values
        gameend=1
        flag_cnt=0
        timer=[0,0,-1]
        countup_time="00:00:00"
        self.timer_label.config(font=("Verdana",10,"normal"),text=countup_time)
        self.mine_label.config(text=str(number_of_mines-flag_cnt),fg="black")

        #make new grid
        self.buttons()

        #temporarily disable buttons(for timer sync)
        if(counter_running==1):
            self.timer_label.config(text="Loading..")
            for i in range(0,number_of_x*number_of_y):
                self.G_buttons[i/number_of_x][i%number_of_x][0].config(state=DISABLED)

        #save mode
        mode=self.v.get()

    #customgrid_set func
    def customgrid_set(self):
        global number_of_x,number_of_y,number_of_mines

        #check for invalid inputs
        try: #check if int
            int(self.x_spinbox.get())+1
            int(self.y_spinbox.get())+1
            int(self.m_spinbox.get())+1

            #if x,y not in range -> error sound + do nothing
            if((int(self.x_spinbox.get())>30 or int(self.x_spinbox.get())<1) or (int(self.y_spinbox.get())>30 or int(self.y_spinbox.get())<1)):
                winsound.PlaySound("SystemQuestion",winsound.SND_ASYNC)
                return None
            #if mine<0 or >x*y -> error sound + do nothing
            elif(int(self.m_spinbox.get())<0 or int(self.m_spinbox.get())>int(self.x_spinbox.get())*int(self.y_spinbox.get())):
                winsound.PlaySound("SystemQuestion",winsound.SND_ASYNC)
                return None

        except: #when wrong input(str or double etc) -> error sound + do nothing
            winsound.PlaySound("SystemQuestion",winsound.SND_ASYNC)
            return None

        #set radio to custom
        self.v.set(3)

        #restart
        self.restart(int(self.x_spinbox.get()),int(self.y_spinbox.get()),int(self.m_spinbox.get()))

        #close window
        self.customgrid_window.destroy()

    #customgrid_ui func
    def customgrid_ui(self):
        #set radio to the mode before(for cancel)
        self.v.set(mode)

        #make window
        self.customgrid_window=Toplevel(root)
        self.x,self.y=root.winfo_x(),root.winfo_y()
        self.customgrid_window.geometry("+%d+%d"%(self.x+7,self.y+29))
        self.customgrid_window.title(unicode("사용자 지정",'cp949'))
        self.customgrid_window.resizable(0,0)
        self.customgrid_window.focus_force()
        self.customgrid_window.grab_set()

        #set IntVars
        self.vx=IntVar(self.customgrid_window)
        self.vx.set(number_of_x)
        self.vy=IntVar(self.customgrid_window)
        self.vy.set(number_of_y)
        self.vm=IntVar(self.customgrid_window)
        self.vm.set(number_of_mines)

        #create labels and spinboxes
        self.bounds_label=Label(self.customgrid_window,font=("consolas",10,"normal"),text=unicode("최대 : 30x30",'cp949'))
        self.x_label=Label(self.customgrid_window,font=("consolas",10,"normal"),text=unicode("가로 ",'cp949'))
        self.x_spinbox=Spinbox(self.customgrid_window,relief="solid",width=4,from_=1,to=30,textvariable=self.vx)
        self.y_label=Label(self.customgrid_window,font=("consolas",10,"normal"),text=unicode("세로 ",'cp949'))
        self.y_spinbox=Spinbox(self.customgrid_window,relief="solid",width=4,from_=1,to=30,textvariable=self.vy)
        self.m_label=Label(self.customgrid_window,font=("consolas",10,"normal"),text=unicode("지뢰 수 ",'cp949'))
        self.m_spinbox=Spinbox(self.customgrid_window,relief="solid",width=4,from_=0,to=900,textvariable=self.vm)

        #place them
        self.bounds_label.grid(row=0,columnspan=2,padx=15,pady=(5,10))
        self.x_label.grid(row=1,column=0,sticky=E)
        self.x_spinbox.grid(row=1,column=1,sticky=W)
        self.y_label.grid(row=2,column=0,sticky=E,pady=3)
        self.y_spinbox.grid(row=2,column=1,sticky=W,pady=3)
        self.m_label.grid(row=3,column=0,sticky=E)
        self.m_spinbox.grid(row=3,column=1,sticky=W)

        #create buttons
        self.confirm_btn=Button(self.customgrid_window,width=5,text=unicode("확인",'cp949'),command=self.customgrid_set)
        self.cancel_btn=Button(self.customgrid_window,width=5,text=unicode("취소",'cp949'),command=self.customgrid_window.destroy)

        #bind key to buttons
        self.customgrid_window.bind('<Return>',lambda e : self.customgrid_set())
        self.customgrid_window.bind('<Escape>',lambda e : self.customgrid_window.destroy())

        #place them
        self.confirm_btn.grid(row=4,column=0,pady=(10,5))
        self.cancel_btn.grid(row=4,column=1,padx=(0,5),pady=(10,5))

    #success func
    def success(self):
        global gameend
        gameend=1

        #bold timer
        self.timer_label.config(font=("Verdana",10,"bold"))

        #reveal bombs
        for i in range(0,number_of_x*number_of_y):
            if(self.G_buttons[i/number_of_x][i%number_of_x][2]==10):
                self.G_buttons[i/number_of_x][i%number_of_x][0].config(text=unicode('☆','cp949'))

        #make buttons useless
        for i in range(0,number_of_x*number_of_y):
            self.G_buttons[i/number_of_x][i%number_of_x][0].config(command=self.donothing)
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<Button-1>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<Button-2>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<Button-3>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<ButtonRelease-1>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<ButtonRelease-3>')

        #change flag counter to success
        self.mine_label.config(text="CLEAR!",fg="dark green")

        #play success sound
        winsound.PlaySound("SystemAsterisk",winsound.SND_ASYNC)

    #gameover func
    def gameover(self,yxarr):
        global gameend
        gameend=1

        #temp
        self.temp=0

        #highlight mistake
        for i in range(0,len(yxarr)):
            for j in range(0,number_of_x*number_of_y):
                if(j/number_of_x==yxarr[i][0] and j%number_of_x==yxarr[i][1]):
                    self.G_buttons[j/number_of_x][j%number_of_x][0].config(text=unicode('★','cp949'),relief="sunken",bg="red")

        #darken out bombs(reveal) except mistake / no need to change [1] to 1 (cause game over)
        for i in range(0,number_of_x*number_of_y):
            if(self.G_buttons[i/number_of_x][i%number_of_x][2]==10):
                for j in range(0,len(yxarr)):
                    if(i/number_of_x==yxarr[j][0] and i%number_of_x==yxarr[j][1]):
                        self.temp=1
                        continue
                if(self.temp==1):
                    self.temp=0
                    continue
                self.G_buttons[i/number_of_x][i%number_of_x][0].config(text=unicode('★','cp949'),relief="sunken",bg="dark grey")

        #make buttons useless
        for i in range(0,number_of_x*number_of_y):
            self.G_buttons[i/number_of_x][i%number_of_x][0].config(command=self.donothing)
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<Button-1>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<Button-2>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<Button-3>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<ButtonRelease-1>')
            self.G_buttons[i/number_of_x][i%number_of_x][0].unbind('<ButtonRelease-3>')

        #change flag counter to fail
        self.mine_label.config(text="FAIL..",fg="red")

        #play gameover sound
        winsound.PlaySound("SystemHand",winsound.SND_ASYNC)

    #donothong(literally)
    def donothing(self):
        return None

    #numbercolor func
    def numbercolor(self,n):
        if(n==1):
            return "#0000ff"
        elif(n==2):
            return "#008000"
        elif(n==3):
            return "#ff0000"
        elif(n==4):
            return "#000080"
        elif(n==5):
            return "#800000"
        elif(n==6):
            return "#008080"
        elif(n==7):
            return "#000000"
        elif(n==8):
            return "#808080"

    #functions for multiclick
    #lefton func
    def lefton(self,y,x):
        global left_state

        #set left to on
        left_state=1

        #if both pressed -> multiclick fn
        if(left_state==1 and right_state==1):
            self.multiclick(y,x)

    #righton func
    def righton(self,y,x):
        global right_state

        #set right to on
        right_state=1

        #if both pressed -> multiclick fn
        if(left_state==1 and right_state==1):
            self.multiclick(y,x)

    #leftrelease func
    def leftrelease(self):
        global left_state

        #set left to off
        left_state=0

    #rightrelease funcright
    def rightrelease(self):
        global right_state

        #set right to off
        right_state=0

###############################################################################################################################################################################################################

    #left func(left click on button)
    def left(self,y,x):
        global gameend

        #start timer
        if(gameend==1 and counter_running==0):
            gameend=0
            self.countup()

        #if revealed do nothing
        if(self.G_buttons[y][x][1]==1):
            return None

        #if clicked on mine
        if(self.G_buttons[y][x][2]==10):
            self.gameover([[y,x]])
            return None

        #if clicked on 0
        if(self.G_buttons[y][x][2]==0):
            #autoleft fn
            self.autoleft(y,x)

        #if clicked on number 1~8
        if(self.G_buttons[y][x][2]!=0 and self.G_buttons[y][x][2]!=10):
            self.G_buttons[y][x][1]=1
            self.G_buttons[y][x][0].config(state=NORMAL,text=str(self.G_buttons[y][x][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y][x][2]))

        #see if there are no more left clickables
        for i in range(0,number_of_x*number_of_y):
            if(self.G_buttons[i/number_of_x][i%number_of_x][2]!=10):
                if(self.G_buttons[i/number_of_x][i%number_of_x][1]==0):
                    return None

        #if there aren't -> success fn
        self.success()

    #middle func(mouse wheel button click)
    def middle(self,y,x):
        global flag_cnt

        #if revealed do nothing
        if(self.G_buttons[y][x][1]==1):
            return None

        #show/unshow qm
        if(self.G_buttons[y][x][0].cget("text")==''):
            self.G_buttons[y][x][0].config(state=DISABLED,text='?',disabledforeground="black")
        elif(self.G_buttons[y][x][0].cget("text")=='?'):
            self.G_buttons[y][x][0].config(state=NORMAL,text='')
        elif(self.G_buttons[y][x][0].cget("text")==unicode('☆','cp949')):
            self.G_buttons[y][x][0].config(text='?')

            flag_cnt-=1
            self.G_buttons[y][x][3]=0
            self.mine_label.config(text=str(number_of_mines-flag_cnt))

    #right func(right click on button)
    def right(self,y,x):
        global flag_cnt

        #if revealed do nothing
        if(self.G_buttons[y][x][1]==1):
            return None

        #activate/deactivate flag + show/unshow 'F' + flag_cnt +/- 1
        if(self.G_buttons[y][x][3]==1):
            self.G_buttons[y][x][3]=0
            self.G_buttons[y][x][0].config(state=NORMAL,text='')
            flag_cnt-=1
        else:
            if(flag_cnt==number_of_mines):
                return None
            self.G_buttons[y][x][3]=1
            self.G_buttons[y][x][0].config(state=DISABLED,text=unicode('☆','cp949'),disabledforeground="black")
            flag_cnt+=1

        #change mine counter
        self.mine_label.config(text=str(number_of_mines-flag_cnt))

    #autoleft(auto left click)
    def autoleft(self,y,x):
        #if revealed or flag do nothing
        if(self.G_buttons[y][x][1]==1 or self.G_buttons[y][x][3]==1):
            return None

        #reveal
        self.G_buttons[y][x][1]=1
        self.G_buttons[y][x][0].config(text='',relief="sunken",bg="dark grey")

        #scan nearby buttons
        if(y-1>=0 and x-1>=0):                                                  #one
            if(self.G_buttons[y-1][x-1][2]!=0 and self.G_buttons[y-1][x-1][3]==0):
                self.G_buttons[y-1][x-1][1]=1
                self.G_buttons[y-1][x-1][0].config(state=NORMAL,text=str(self.G_buttons[y-1][x-1][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y-1][x-1][2]))
            elif(self.G_buttons[y-1][x-1][1]==0 and self.G_buttons[y-1][x-1][3]==0):
                self.autoleft(y-1,x-1)
        if(x-1>=0):                                                             #two
            if(self.G_buttons[y][x-1][2]!=0 and self.G_buttons[y][x-1][3]==0):
                self.G_buttons[y][x-1][1]=1
                self.G_buttons[y][x-1][0].config(state=NORMAL,text=str(self.G_buttons[y][x-1][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y][x-1][2]))
            elif(self.G_buttons[y][x-1][1]==0 and self.G_buttons[y][x-1][3]==0):
                self.autoleft(y,x-1)
        if(y+1<number_of_y and x-1>=0):                                         #three
            if(self.G_buttons[y+1][x-1][2]!=0 and self.G_buttons[y+1][x-1][3]==0):
               self.G_buttons[y+1][x-1][1]=1
               self.G_buttons[y+1][x-1][0].config(state=NORMAL,text=str(self.G_buttons[y+1][x-1][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y+1][x-1][2]))
            elif(self.G_buttons[y+1][x-1][1]==0 and self.G_buttons[y+1][x-1][3]==0):
                self.autoleft(y+1,x-1)
        if(y-1>=0):                                                             #four
            if(self.G_buttons[y-1][x][2]!=0 and self.G_buttons[y-1][x][3]==0):
                self.G_buttons[y-1][x][1]=1
                self.G_buttons[y-1][x][0].config(state=NORMAL,text=str(self.G_buttons[y-1][x][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y-1][x][2]))
            elif(self.G_buttons[y-1][x][1]==0 and self.G_buttons[y-1][x][3]==0):
                self.autoleft(y-1,x)
        if(y+1<number_of_y):                                                    #five
            if(self.G_buttons[y+1][x][2]!=0 and self.G_buttons[y+1][x][3]==0):
                self.G_buttons[y+1][x][1]=1
                self.G_buttons[y+1][x][0].config(state=NORMAL,text=str(self.G_buttons[y+1][x][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y+1][x][2]))
            elif(self.G_buttons[y+1][x][1]==0 and self.G_buttons[y+1][x][3]==0):
                self.autoleft(y+1,x)
        if(y-1>=0 and x+1<number_of_x):                                         #six
            if(self.G_buttons[y-1][x+1][2]!=0 and self.G_buttons[y-1][x+1][3]==0):
               self.G_buttons[y-1][x+1][1]=1
               self.G_buttons[y-1][x+1][0].config(state=NORMAL,text=str(self.G_buttons[y-1][x+1][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y-1][x+1][2]))
            elif(self.G_buttons[y-1][x+1][1]==0 and self.G_buttons[y-1][x+1][3]==0):
                self.autoleft(y-1,x+1)
        if(x+1<number_of_x):                                                    #seven
            if(self.G_buttons[y][x+1][2]!=0 and self.G_buttons[y][x+1][3]==0):
                self.G_buttons[y][x+1][1]=1
                self.G_buttons[y][x+1][0].config(state=NORMAL,text=str(self.G_buttons[y][x+1][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y][x+1][2]))
            elif(self.G_buttons[y][x+1][1]==0 and self.G_buttons[y][x+1][3]==0):
                self.autoleft(y,x+1)
        if(y+1<number_of_y and x+1<number_of_x):                                #eight
            if(self.G_buttons[y+1][x+1][2]!=0 and self.G_buttons[y+1][x+1][3]==0):
                self.G_buttons[y+1][x+1][1]=1
                self.G_buttons[y+1][x+1][0].config(state=NORMAL,text=str(self.G_buttons[y+1][x+1][2]),relief="sunken",bg="dark grey",fg=self.numbercolor(self.G_buttons[y+1][x+1][2]))
            elif(self.G_buttons[y+1][x+1][1]==0 and self.G_buttons[y+1][x+1][3]==0):
                self.autoleft(y+1,x+1)

    #multiclick func
    def multiclick(self,y,x):
        #local variables
        self.cnt=0
        self.mcsuccess=1
        self.failure=[]

        #if not (activated on number and revealed) do nothing
        if not((self.G_buttons[y][x][2]>=1 and self.G_buttons[y][x][2]<=8) and self.G_buttons[y][x][1]==1):
            return None

        #count neighbor flags
        if(y-1>=0 and x-1>=0):
            if(self.G_buttons[y-1][x-1][3]==1):
                self.cnt+=1
        if(x-1>=0):
            if(self.G_buttons[y][x-1][3]==1):
                self.cnt+=1
        if(y+1<number_of_y and x-1>=0):
            if(self.G_buttons[y+1][x-1][3]==1):
                self.cnt+=1
        if(y-1>=0):
            if(self.G_buttons[y-1][x][3]==1):
                self.cnt+=1
        if(y+1<number_of_y):
            if(self.G_buttons[y+1][x][3]==1):
                self.cnt+=1
        if(y-1>=0 and x+1<number_of_x):
            if(self.G_buttons[y-1][x+1][3]==1):
                self.cnt+=1
        if(x+1<number_of_x):
            if(self.G_buttons[y][x+1][3]==1):
                self.cnt+=1
        if(y+1<number_of_y and x+1<number_of_x):
            if(self.G_buttons[y+1][x+1][3]==1):
                self.cnt+=1

        #if the bomb's number and the flag's number are the same -> check if the locations match else do nothing
        if(self.cnt==self.G_buttons[y][x][2]):
            if(y-1>=0 and x-1>=0):
                if(self.G_buttons[y-1][x-1][3]==1 and self.G_buttons[y-1][x-1][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y-1][x-1][3]==0 and self.G_buttons[y-1][x-1][2]==10):
                    self.failure.append([y-1,x-1])
            if(x-1>=0):
                if(self.G_buttons[y][x-1][3]==1 and self.G_buttons[y][x-1][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y][x-1][3]==0 and self.G_buttons[y][x-1][2]==10):
                    self.failure.append([y,x-1])
            if(y+1<number_of_y and x-1>=0):
                if(self.G_buttons[y+1][x-1][3]==1 and self.G_buttons[y+1][x-1][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y+1][x-1][3]==0 and self.G_buttons[y+1][x-1][2]==10):
                    self.failure.append([y+1,x-1])
            if(y-1>=0):
                if(self.G_buttons[y-1][x][3]==1 and self.G_buttons[y-1][x][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y-1][x][3]==0 and self.G_buttons[y-1][x][2]==10):
                    self.failure.append([y-1,x])
            if(y+1<number_of_y):
                if(self.G_buttons[y+1][x][3]==1 and self.G_buttons[y+1][x][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y+1][x][3]==0 and self.G_buttons[y+1][x][2]==10):
                    self.failure.append([y+1,x])
            if(y-1>=0 and x+1<number_of_x):
                if(self.G_buttons[y-1][x+1][3]==1 and self.G_buttons[y-1][x+1][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y-1][x+1][3]==0 and self.G_buttons[y-1][x+1][2]==10):
                    self.failure.append([y-1,x+1])
            if(x+1<number_of_x):
                if(self.G_buttons[y][x+1][3]==1 and self.G_buttons[y][x+1][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y][x+1][3]==0 and self.G_buttons[y][x+1][2]==10):
                    self.failure.append([y,x+1])
            if(y+1<number_of_y and x+1<number_of_x):
                if(self.G_buttons[y+1][x+1][3]==1 and self.G_buttons[y+1][x+1][2]!=10):
                    self.mcsuccess=0
                if(self.G_buttons[y+1][x+1][3]==0 and self.G_buttons[y+1][x+1][2]==10):
                    self.failure.append([y+1,x+1])
        else:
            return None

        #if mcsuccess -> auto open all neighbor buttons(not revealed and not flagged) / else game over
        if(self.mcsuccess==1):
            if(y-1>=0 and x-1>=0):
                if(self.G_buttons[y-1][x-1][1]==0 and self.G_buttons[y-1][x-1][3]==0):
                    self.left(y-1,x-1)
            if(x-1>=0):
                if(self.G_buttons[y][x-1][1]==0 and self.G_buttons[y][x-1][3]==0):
                    self.left(y,x-1)
            if(y+1<number_of_y and x-1>=0):
                if(self.G_buttons[y+1][x-1][1]==0 and self.G_buttons[y+1][x-1][3]==0):
                    self.left(y+1,x-1)
            if(y-1>=0):
                if(self.G_buttons[y-1][x][1]==0 and self.G_buttons[y-1][x][3]==0):
                    self.left(y-1,x)
            if(y+1<number_of_y):
                if(self.G_buttons[y+1][x][1]==0 and self.G_buttons[y+1][x][3]==0):
                    self.left(y+1,x)
            if(y-1>=0 and x+1<number_of_x):
                if(self.G_buttons[y-1][x+1][1]==0 and self.G_buttons[y-1][x+1][3]==0):
                    self.left(y-1,x+1)
            if(x+1<number_of_x):
                if(self.G_buttons[y][x+1][1]==0 and self.G_buttons[y][x+1][3]==0):
                    self.left(y,x+1)
            if(y+1<number_of_y and x+1<number_of_x):
                if(self.G_buttons[y+1][x+1][1]==0 and self.G_buttons[y+1][x+1][3]==0):
                    self.left(y+1,x+1)
        else:
            self.gameover(self.failure)

###############################################################################################################################################################################################################

#start program
root=None

def start():
    global number_of_x,number_of_y,number_of_mines
    global mode
    global countup_time,counter_running,timer,gameend
    global left_state,right_state
    global transparency,transparency_backup

    global root

    number_of_x=8
    number_of_y=8
    number_of_mines=10
    flag_cnt=0

    mode=0

    countup_time="00:00:00"
    counter_running=0
    timer=[0,0,-1]
    gameend=1

    left_state=0
    right_state=0

    transparency=1
    transparency_backup=1

    root = Tk()
    root.focus_force()
    root.title(unicode('지뢰찾기+','cp949'))
    root.resizable(0,0)
    minesweeper=mine(root)
    root.mainloop()

if __name__ == '__main__':
    start()
