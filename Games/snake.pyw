#-*- coding: cp949 -*-
from Tkinter import *
import tkMessageBox
import winsound
import random

#score
score=0

#win ..?
win=0

#food
food=None

#state
state=2

#moves_arr
moves_arr=[state]

#location + length
snake_loc=[[7,1],[7,0],[7,17]] #head - to - tail
snake_len=3

#trans
transparency=1
transparency_backup=1

#snake Game
class snake():
    def __init__(self,master):
        #create menubar
        self.menu=Menu(root,tearoff=0)

        self.gamesubmenu=Menu(self.menu,tearoff=0)
        self.gamesubmenu.add_command(label=unicode("새 게임",'cp949'),command=self.restart)
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_command(label=unicode("닫기",'cp949'),command=root.destroy)
        self.menu.add_cascade(label=unicode("게임",'cp949'),menu=self.gamesubmenu)

        self.helpsubmenu=Menu(self.menu,tearoff=0)
        self.helpsubmenu.add_command(label=unicode("조작키",'cp949'),command=lambda : tkMessageBox.showinfo(unicode("조작키",'cp949'),unicode("방향키 / W,A,S,D : 이동\nP : 일시정지/계속하기\n\nF2 : 새 게임\nF4 : 창 숨기기/보이기",'cp949'),parent=root))
        self.menu.add_cascade(label=unicode("도움말",'cp949'),menu=self.helpsubmenu)

        root.config(menu=self.menu)

        #create top ui
        self.topui_frame=Frame(root)
        self.topui_frame.grid(row=0,sticky=E+W)

        self.score_label=Label(self.topui_frame,font=("Verdana",10,"normal"),width=5,anchor=W,text=str(score).zfill(3))
        self.score_label.pack(side="left")

        self.trans_sdr=Scale(self.topui_frame,from_=0,to=100,orient=HORIZONTAL,showvalue=False,sliderlength=10,length=50,command=self.settransparency)
        self.trans_sdr.set(transparency*100)
        self.trans_sdr.pack(side="right")

        self.pause_btn=Button(self.topui_frame,relief="ridge",font=("Verdana",7,"normal"),text="PAUSE",width=7,command=self.pause_unpause)
        self.pause_btn.pack(side="right",anchor=E,padx=(0,98))

        #create board
        self.board_frame=Frame(root)
        self.board_frame.grid(row=1)
        self.createboard()

        #bind controls / left : 0, up : 1, right : 2, down : 3
        root.bind('<F4>',lambda e : self.hidewindow())
        root.bind('<F2>',lambda e : self.restart())

        root.bind('<Left>',lambda e : self.set_state(0))
        root.bind('<Up>',lambda e : self.set_state(1))
        root.bind('<Right>',lambda e : self.set_state(2))
        root.bind('<Down>',lambda e : self.set_state(3))
        root.bind('<a>',lambda e : self.set_state(0))
        root.bind('<w>',lambda e : self.set_state(1))
        root.bind('<d>',lambda e : self.set_state(2))
        root.bind('<s>',lambda e : self.set_state(3))
        root.bind('<A>',lambda e : self.set_state(0))
        root.bind('<W>',lambda e : self.set_state(1))
        root.bind('<D>',lambda e : self.set_state(2))
        root.bind('<S>',lambda e : self.set_state(3))

        root.bind('<KeyRelease-p>',lambda e : self.pause_unpause())
        root.bind('<KeyRelease-P>',lambda e : self.pause_unpause())

        #_job WOW...
        self._job=None

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

    #createboard func
    def createboard(self):
        #2-dimentional array
        self.G_board=[[0]*18 for i in range(16)]
        #create board
        for i in range(0,288):
            if((i/18+i%18)%2==0):
                self.G_board[i/18][i%18]=Label(self.board_frame,width=2,height=1,bg="#ECF0F3")
            else:
                self.G_board[i/18][i%18]=Label(self.board_frame,width=2,height=1,bg="#E7ECF0")
            self.G_board[i/18][i%18].grid(row=i/18,column=i%18)

        #draw snake
        for i in range(snake_len):
            self.G_board[snake_loc[i][0]][snake_loc[i][1]].config(bg="#00897b")

        #start game
        self.place_food()
        self.move()

    #restart func
    def restart(self):
        global score,state,moves_arr,snake_loc,snake_len,win

        #if restarted while not pauesd -> pause it first
        if not(self._job==None):
            root.after_cancel(self._job)
            self._job=None

        #rebind p
        root.bind('<KeyRelease-p>',lambda e : self.pause_unpause())
        root.bind('<KeyRelease-P>',lambda e : self.pause_unpause())

        #restore button
        self.pause_btn.config(font=("Verdana",7,"normal"),text="PAUSE",fg="black")

        #destroy previous board
        for i in range(0,288):
            self.G_board[i/18][i%18].destroy()

        #reset values
        score=0
        self.score_label.config(font=("Verdana",10,"normal"),text=str(score).zfill(3))
        win=0
        state=2
        moves_arr=[state]
        snake_loc=[[7,1],[7,0],[7,17]] #head - to - tail
        snake_len=3

        #create new board(restart)
        self.createboard()

    #pause_unpause func
    def pause_unpause(self):
        #if gameover
        if(self.pause_btn.cget("fg")=="#00897b"):
            #restart
            self.restart()
            return None

        #pause/unpause
        if not(self._job==None):
            root.after_cancel(self._job)
            self._job=None
            self.pause_btn.config(text="RESUME")
        else:
            self.move()
            self.pause_btn.config(text="PAUSE")

    #place_food func
    def place_food(self):
        global food
        global win

        #make available space array
        self.available=[]
        for i in range(0,288):
            if not(self.G_board[i/18][i%18].cget("bg")=="#00897b"):
                self.available.append(i)

        #generate random food + success check
        try:
            food=random.choice(self.available)
        except:
            win=1

        #place food
        self.G_board[food/18][food%18].config(bg="#f8c100")

    #gameover func
    def gameover(self):
        #stop the game
        if not(self._job==None):
            root.after_cancel(self._job)
            self._job=None

        #unbind p
        root.unbind('<KeyRelease-p>')
        root.unbind('<KeyRelease-P>')

        #bold score text
        self.score_label.config(font=("Verdana",10,"bold"))

        #button -> restart
        self.pause_btn.config(font=("Verdana",7,"bold"),text="RESTART",fg="#00897b")

        #if somehow win -> play success sound, else gameover sound
        if(win==1):
            winsound.PlaySound("SystemAsterisk",winsound.SND_ASYNC)
        else:
            winsound.PlaySound("SystemHand",winsound.SND_ASYNC)

    #set_state func
    def set_state(self,s):
        global state
        global moves_arr

        #if paused do nothing
        if(self._job==None):
            return None

        #if opposite move or same move do nothing
        if(int(state)%2==int(s)%2):
            return None

        #set state + save move
        state=s
        moves_arr.append(state)

    #move func
    def move(self):
        global snake_loc,snake_len
        global moves_arr
        global score

        #temp
        self.temp=0
        self.temp_last=[0,0]

        #delete previous move / what....
        if not(len(moves_arr)==1):
            del moves_arr[0]

        #save tail loc for food intake
        self.temp_last[0]=snake_loc[snake_len-1][0]
        self.temp_last[1]=snake_loc[snake_len-1][1]

        #movement
        for i in reversed(range(1,snake_len)):
            snake_loc[i][0]=snake_loc[i-1][0]
            snake_loc[i][1]=snake_loc[i-1][1]
        if(moves_arr[0]==0):
            if(snake_loc[0][1]==0):
                snake_loc[0][1]=17
            else:
                snake_loc[0][1]-=1
        elif(moves_arr[0]==1):
            if(snake_loc[0][0]==0):
                snake_loc[0][0]=15
            else:
                snake_loc[0][0]-=1
        elif(moves_arr[0]==2):
            if(snake_loc[0][1]==17):
                snake_loc[0][1]=0
            else:
                snake_loc[0][1]+=1
        elif(moves_arr[0]==3):
            if(snake_loc[0][0]==15):
                snake_loc[0][0]=0
            else:
                snake_loc[0][0]+=1

        #if touched food -> extend + new food + score++
        if(snake_loc[0][0]==food/18 and snake_loc[0][1]==food%18):
            #extend
            snake_len+=1
            snake_loc.append(self.temp_last)

            #score++
            score+=1
            self.score_label.config(text=str(score).zfill(3))

            #delete previous food / make it a tail
            self.G_board[food/18][food%18].config(bg="#00897b")

            #create new food
            self.place_food()

        #if touched itself -> gameover
        for i in range(1,snake_len):
            if(snake_loc[0][0]==snake_loc[i][0] and snake_loc[0][1]==snake_loc[i][1]):
                #highlight head + delete tail(cause not updated yet)
                self.G_board[snake_loc[0][0]][snake_loc[0][1]].config(bg="#e31616")
                if((self.temp_last[0]+self.temp_last[1])%2==0):
                    self.G_board[self.temp_last[0]][self.temp_last[1]].config(bg="#ECF0F3")
                else:
                    self.G_board[self.temp_last[0]][self.temp_last[1]].config(bg="#E7ECF0")

                #gameover fn
                self.gameover()
                return None

        #show(print to screen)
        if((self.temp_last[0]+self.temp_last[1])%2==0):
            self.G_board[self.temp_last[0]][self.temp_last[1]].config(bg="#ECF0F3")
        else:
            self.G_board[self.temp_last[0]][self.temp_last[1]].config(bg="#E7ECF0")
        self.G_board[snake_loc[0][0]][snake_loc[0][1]].config(bg="#00897b")

        #repeat
        self._job=root.after(90,self.move)

#START
root=None

def start():
    global score
    global win
    global food
    global state
    global moves_arr
    global snake_loc,snake_len
    global transparency,transparency_backup

    global root

    score=0
    win=0
    food=None
    state=2
    moves_arr=[state]
    snake_loc=[[7,1],[7,0],[7,17]] #head - to - tail
    snake_len=3
    transparency=1
    transparency_backup=1

    root = Tk()
    root.focus_force()
    root.title(unicode("스네이크 게임",'cp949'))
    root.resizable(0,0)
    snk=snake(root)
    root.mainloop()

if __name__ == '__main__':
    start()
