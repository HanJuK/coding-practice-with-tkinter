#-*- coding: cp949 -*-
from Tkinter import *
import tkMessageBox
import winsound
import random

#mode
mode=0

#state
state=0

#score
score=0

#trans
transparency=1
transparency_backup=1

#2048
class T048():
    def __init__(self,master):
        #create menubar
        self.v=IntVar()
        self.v.set(0)

        self.menu=Menu(root,tearoff=0)
        self.gamesubmenu=Menu(self.menu,tearoff=0)
        self.gamesubmenu.add_command(label=unicode("새 게임",'cp949'),command=self.newgame)
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_radiobutton(label=unicode("클래식 모드",'cp949'),variable=self.v,value=0,command=self.restart)
        self.gamesubmenu.add_radiobutton(label=unicode("연습 모드",'cp949'),variable=self.v,value=1,command=self.restart)
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_command(label=unicode("닫기",'cp949'),command=root.destroy)
        self.menu.add_cascade(label=unicode("게임",'cp949'),menu=self.gamesubmenu)

        self.helpsubmenu=Menu(self.menu,tearoff=0)
        self.helpsubmenu.add_command(label=unicode("조작키",'cp949'),command=lambda : tkMessageBox.showinfo(unicode("조작키",'cp949'),unicode("방향키 / W,A,S,D : 이동\nZ : 수 무르기(연습모드)\n\nF2 : 새 게임\nF4 : 창 숨기기/보이기",'cp949'),parent=root)) #NEW
        self.menu.add_cascade(label=unicode("도움말",'cp949'),menu=self.helpsubmenu)

        root.config(menu=self.menu)

        #create top ui(default classic)
        self.classicbar_frame,self.practicebar_frame=Frame(root),Frame(root)
        self.createclassicbar()

        #create blocks
        self.block_frame=Frame(root)
        self.block_frame.grid(row=1)
        self.blocks()

        #bind buttons
        root.bind('<F4>',lambda e : self.hidewindow())
        root.bind('<F2>',lambda e : self.newgame())

        root.bind('<a>',lambda e : self.left())
        root.bind('<w>',lambda e : self.up())
        root.bind('<d>',lambda e : self.right())
        root.bind('<s>',lambda e : self.down())
        root.bind('<A>',lambda e : self.left())
        root.bind('<W>',lambda e : self.up())
        root.bind('<D>',lambda e : self.right())
        root.bind('<S>',lambda e : self.down())
        root.bind('<Left>',lambda e : self.left())
        root.bind('<Up>',lambda e : self.up())
        root.bind('<Right>',lambda e : self.right())
        root.bind('<Down>',lambda e : self.down())

        root.bind('<z>',lambda e : self.undo()) #NEW
        root.bind('<Z>',lambda e : self.undo()) #NEW

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

    #create blocks
    def blocks(self):
        #blocks 2-dimentional array
        self.G_blocks=[[0]*4 for i in range(4)]
        #create blocks
        for i in range(0,16):
            self.G_blocks[i/4][i%4]=[Label(self.block_frame,text='',relief='groove',font=("consolas",10,"bold"),width=6,height=3,bg="#e7ecf0"),0,0] #[0]:Block / [1]:exist 0 or 1 / [2]:combined 1 or 0
            self.G_blocks[i/4][i%4][0].grid(row=i/4,column=i%4)

        #create array for backup blocks
        self.backup=[0,0,0,0,0,0,0,0,0,0,0] #NEW
        for i in range(0,11): #NEW
            self.backup[i]=[[0]*4 for j in range(4)]
            for j in range(0,16):
                self.backup[i][j/4][j%4]=[0,0,0,0] #text,bg,[1],[2]

        #add two random(for start)
        rand_start=random.sample(range(16),2)

        if(self.twofour()==4):
            self.G_blocks[rand_start[0]/4][rand_start[0]%4][0].config(text=4)
            self.G_blocks[rand_start[0]/4][rand_start[0]%4][0].config(bg=self.blockcolors(rand_start[0]/4,rand_start[0]%4))
            self.G_blocks[rand_start[1]/4][rand_start[1]%4][0].config(text=2)
            self.G_blocks[rand_start[1]/4][rand_start[1]%4][0].config(bg=self.blockcolors(rand_start[1]/4,rand_start[1]%4))
            self.G_blocks[rand_start[0]/4][rand_start[0]%4][1]=1
            self.G_blocks[rand_start[1]/4][rand_start[1]%4][1]=1
        else:
            self.G_blocks[rand_start[0]/4][rand_start[0]%4][0].config(text=2)
            self.G_blocks[rand_start[0]/4][rand_start[0]%4][0].config(bg=self.blockcolors(rand_start[0]/4,rand_start[0]%4))
            self.G_blocks[rand_start[1]/4][rand_start[1]%4][0].config(text=2)
            self.G_blocks[rand_start[1]/4][rand_start[1]%4][0].config(bg=self.blockcolors(rand_start[1]/4,rand_start[1]%4))
            self.G_blocks[rand_start[0]/4][rand_start[0]%4][1]=1
            self.G_blocks[rand_start[1]/4][rand_start[1]%4][1]=1

        if(mode==1):
            for i in range(0,16):
                self.backup[0][i/4][i%4]=[self.G_blocks[i/4][i%4][0].cget("text"),self.G_blocks[i/4][i%4][0].cget("bg"),self.G_blocks[i/4][i%4][1],self.G_blocks[i/4][i%4][2]]

    #blockcolors func
    def blockcolors(self,i,j):
        if(self.G_blocks[i][j][0].cget("text")==''): #NEW
            return "#e7ecf0"
        elif(self.G_blocks[i][j][0].cget("text")==2): #NEW
            return "#ffffde"
        elif(self.G_blocks[i][j][0].cget("text")==4):
            return "#fff5ba"
        elif(self.G_blocks[i][j][0].cget("text")==8):
            return "#ffcbc1"
        elif(self.G_blocks[i][j][0].cget("text")==16):
            return "#ffabab"
        elif(self.G_blocks[i][j][0].cget("text")==32):
            return "#c8f7c1"
        elif(self.G_blocks[i][j][0].cget("text")==64):
            return "#a4edd0"
        elif(self.G_blocks[i][j][0].cget("text")==128):
            return "#c4faf8"
        elif(self.G_blocks[i][j][0].cget("text")==256):
            return "#ace7ff"
        elif(self.G_blocks[i][j][0].cget("text")==512):
            return "#85e3ff"
        elif(self.G_blocks[i][j][0].cget("text")==1024):
            return "#6eb5ff"
        elif(self.G_blocks[i][j][0].cget("text")==2048):
            return "#b28dff"
        elif(self.G_blocks[i][j][0].cget("text")>=4096):
            return "#ff9cee"

    #createclassicbar func
    def createclassicbar(self):
        self.practicebar_frame.destroy()

        self.classicbar_frame=Frame(root)
        self.classicbar_frame.grid(row=0,sticky=E+W)

        self.classic_label=Label(self.classicbar_frame,font=("Times",11,"bold"),text="Classic")
        self.classic_label.pack(side="left")

        self.score_label=Label(self.classicbar_frame,font=("Verdana",10,"normal"),text=str(score)) #NEW
        self.score_label.pack(side="left",padx=(2,0),expand=True) #NEW

        self.trans_sdr=Scale(self.classicbar_frame,from_=0,to=100,orient=HORIZONTAL,showvalue=False,sliderlength=10,length=50,command=self.settransparency)
        self.trans_sdr.set(transparency*100)
        self.trans_sdr.pack(side="right")

    #createpracticebar func
    def createpracticebar(self):
        self.classicbar_frame.destroy()

        self.practicebar_frame=Frame(root)
        self.practicebar_frame.grid(row=0,sticky=E+W)

        self.practice_label=Label(self.practicebar_frame,font=("Times",11,"bold"),text="Practice")
        self.practice_label.pack(side="left")

        self.undo_button=Button(self.practicebar_frame,relief="ridge",font=("Verdana",7,"normal"),text="UNDO",command=self.undo) #NEW
        self.undo_button.pack(side="left",padx=(0,3),expand=True) #NEW

        self.trans_sdr=Scale(self.practicebar_frame,from_=0,to=100,orient=HORIZONTAL,showvalue=False,sliderlength=10,length=50,command=self.settransparency)
        self.trans_sdr.set(transparency*100)
        self.trans_sdr.pack(side="right")

    #newgame func
    def newgame(self):
        global score
        global state

        #destroy previous grid
        for i in range(0,16):
            self.G_blocks[i/4][i%4][0].destroy()

        #reset values
        if(mode==0):
            score=0
            self.score_label.config(font=("Verdana",10,"normal"),text=str(score))
        if(mode==1):
            state=0

        #make new blocks
        self.blocks()

    #restart func(for mode)
    def restart(self):
        global mode
        global score
        global state

        #if already mode no nothing
        if(mode==self.v.get()):
            return None

        #destroy previous grid
        for i in range(0,16):
            self.G_blocks[i/4][i%4][0].destroy()

        #reset values
        score=0
        state=0

        #save mode
        mode=self.v.get()

        #make new blocks + ui
        self.createclassicbar() if self.v.get()==0 else self.createpracticebar()
        self.blocks()

    #savestate func
    def savestate(self):
        global state

        #save state
        if(state==10): #NEW
            for i in range(0,10): #NEW
                for j in range(0,16):
                    self.backup[i][j/4][j%4]=self.backup[i+1][j/4][j%4]
            for i in range(0,16):
                self.backup[state][i/4][i%4]=[self.G_blocks[i/4][i%4][0].cget("text"),self.G_blocks[i/4][i%4][0].cget("bg"),self.G_blocks[i/4][i%4][1],self.G_blocks[i/4][i%4][2]]
        elif(state<10): #NEW
            state+=1
            for i in range(0,16):
                self.backup[state][i/4][i%4]=[self.G_blocks[i/4][i%4][0].cget("text"),self.G_blocks[i/4][i%4][0].cget("bg"),self.G_blocks[i/4][i%4][1],self.G_blocks[i/4][i%4][2]]

    #undo func
    def undo(self):
        global state

        #if classic do nothing
        if(mode==0): #NEW
            return None #NEW

        #restore state
        if(state>0):
            for i in range(0,16):
                self.G_blocks[i/4][i%4][0].config(text=self.backup[state-1][i/4][i%4][0],bg=self.backup[state-1][i/4][i%4][1])
                self.G_blocks[i/4][i%4][1]=self.backup[state-1][i/4][i%4][2]
                self.G_blocks[i/4][i%4][2]=self.backup[state-1][i/4][i%4][3]
            state-=1

            #restore color for gameover
            for i in range(0,16): #NEW
                self.G_blocks[i/4][i%4][0].config(bg=self.blockcolors(i/4,i%4)) #NEW

    #twofour func
    def twofour(self):
        return 4 if random.randrange(4)==0 else 2 #25% -> 4 / 75% -> 2

    #randnumspawn func
    def randnumspawn(self):
        #blank blocks array
        self.blank=[]

        #find blank blocks and add them to the array
        for i in range (0,4):
            for j in range (0,4):
                if(self.G_blocks[i][j][1]==0):
                    self.blank.append(i*4+j)

        #spawn a 2 or a 4 in a random blank block
        self.t=int(random.sample(self.blank,1)[0])
        self.G_blocks[self.t/4][self.t%4][0].config(text=self.twofour())
        self.G_blocks[self.t/4][self.t%4][0].config(bg=self.blockcolors(self.t/4,self.t%4))
        self.G_blocks[self.t/4][self.t%4][1]=1

    #gameovercheck func
    def gameovercheck(self):
        #check for game over
        for i in range(0,16): #NEW
            if(self.G_blocks[i/4][i%4][0].cget("text")==''): #NEW
                return None #NEW
        for i in range (0,4):
            for j in range (0,3):
                if(self.G_blocks[i][j][0].cget("text")==self.G_blocks[i][j+1][0].cget("text")):
                    return None
                if(self.G_blocks[j][i][0].cget("text")==self.G_blocks[j+1][i][0].cget("text")):
                    return None

        #if game over darken out colors + bold score
        for i in range(0,16): #NEW
            self.G_blocks[i/4][i%4][0].config(bg="#999999")
        if(mode==0):
            self.score_label.config(font=("Verdana",10,"bold")) #NEW

        #play gameover sound
        winsound.PlaySound("SystemHand",winsound.SND_ASYNC) #NEW

#######################################################################################################################################################################################################

    #left func
    def left(self):
        global score

        #flag for no moves
        self.flag=0

        #for every line
        for i in range (0,4):
            for j in range (0,4):
                #if there is a number
                if(self.G_blocks[i][j][1]==1):
                    #if the number is at the edge
                    if(j==0):
                        print("already at edge / Do nothing")
                        continue
                    #find the nearest number or edge
                    for k in reversed(range(0,j)):
                        #if found a number
                        if(self.G_blocks[i][k][1]==1):
                            #if the numbers are the same and the 'k' number hasn't been combined yet -> combine them
                            if(self.G_blocks[i][k][0].cget("text")==self.G_blocks[i][j][0].cget("text") and self.G_blocks[i][k][2]==0):
                                self.G_blocks[i][k][0].config(text=int(self.G_blocks[i][k][0].cget("text"))*2)
                                self.G_blocks[i][k][0].config(bg=self.blockcolors(i,k))
                                self.G_blocks[i][k][2]=1

                                self.G_blocks[i][j][1]=0
                                self.G_blocks[i][j][0].config(text='')
                                self.G_blocks[i][j][0].config(bg="#e7ecf0")

                                self.flag=1

                                if(mode==0):
                                    score+=int(self.G_blocks[i][k][0].cget("text"))
                                    self.score_label.config(text=str(score))
                                print("combined")

                            #if the numbers aren't the same or the 'k' number has already been combined -> move the number to the blank space next to the 'k' number
                            else:
                                #if not already in place
                                if not(j==k+1):
                                    self.G_blocks[i][k+1][0].config(text=self.G_blocks[i][j][0].cget("text"))
                                    self.G_blocks[i][k+1][0].config(bg=self.blockcolors(i,k+1))
                                    self.G_blocks[i][k+1][1]=1

                                    self.G_blocks[i][j][1]=0
                                    self.G_blocks[i][j][0].config(text='')
                                    self.G_blocks[i][j][0].config(bg="#e7ecf0")

                                    self.flag=1
                                    print("not combined / placed next to the number")
                                else:
                                    print("numbers not the same or already combined / Do nothing")

                            #break out
                            break

                        #if didn't find a number(edge) -> move the number to the edge
                        if(k==0):
                            self.G_blocks[i][k][0].config(text=self.G_blocks[i][j][0].cget("text"))
                            self.G_blocks[i][k][0].config(bg=self.blockcolors(i,k))
                            self.G_blocks[i][k][1]=1

                            self.G_blocks[i][j][1]=0
                            self.G_blocks[i][j][0].config(text='')
                            self.G_blocks[i][j][0].config(bg="#e7ecf0")

                            self.flag=1
                            print("Didn't find a number / moved to edge")

        #reset [2] values
        for i in range(0,4):
            for j in range(0,4):
                self.G_blocks[i][j][2]=0

        #randnumspawn + gameovercheck + savestate fn
        if(self.flag==1):
            self.randnumspawn()
            self.gameovercheck()
            if(mode==1):
                self.savestate()

    #up func
    def up(self):
        global score

        #flag for no moves
        self.flag=0

        #for every line
        for i in range (0,4):
            for j in range (0,4):
                #if there is a number
                if(self.G_blocks[j][i][1]==1):
                    #if the number is at the edge
                    if(j==0):
                        print("already at edge / Do nothing")
                        continue
                    #find the nearest number or edge
                    for k in reversed(range(0,j)):
                        #if found a number
                        if(self.G_blocks[k][i][1]==1):
                            #if the numbers are the same and the 'k' number hasn't been combined yet -> combine them
                            if(self.G_blocks[k][i][0].cget("text")==self.G_blocks[j][i][0].cget("text") and self.G_blocks[k][i][2]==0):
                                self.G_blocks[k][i][0].config(text=int(self.G_blocks[k][i][0].cget("text"))*2)
                                self.G_blocks[k][i][0].config(bg=self.blockcolors(k,i))
                                self.G_blocks[k][i][2]=1

                                self.G_blocks[j][i][1]=0
                                self.G_blocks[j][i][0].config(text='')
                                self.G_blocks[j][i][0].config(bg="#e7ecf0")

                                self.flag=1

                                if(mode==0):
                                    score+=int(self.G_blocks[k][i][0].cget("text"))
                                    self.score_label.config(text=str(score))
                                print("combined")

                            #if the numbers aren't the same or the 'k' number has already been combined -> move the number to the blank space next to the 'k' number
                            else:
                                #if not already in place
                                if not(j==k+1):
                                    self.G_blocks[k+1][i][0].config(text=self.G_blocks[j][i][0].cget("text"))
                                    self.G_blocks[k+1][i][0].config(bg=self.blockcolors(k+1,i))
                                    self.G_blocks[k+1][i][1]=1

                                    self.G_blocks[j][i][1]=0
                                    self.G_blocks[j][i][0].config(text='')
                                    self.G_blocks[j][i][0].config(bg="#e7ecf0")

                                    self.flag=1
                                    print("not combined / placed next to the number")
                                else:
                                    print("numbers not the same or already combined / Do nothing")

                            #break out
                            break

                        #if didn't find a number(edge) -> move the number to the edge
                        if(k==0):
                            self.G_blocks[k][i][0].config(text=self.G_blocks[j][i][0].cget("text"))
                            self.G_blocks[k][i][0].config(bg=self.blockcolors(k,i))
                            self.G_blocks[k][i][1]=1

                            self.G_blocks[j][i][1]=0
                            self.G_blocks[j][i][0].config(text='')
                            self.G_blocks[j][i][0].config(bg="#e7ecf0")

                            self.flag=1
                            print("Didn't find a number / moved to edge")

        #reset [2] values
        for i in range(0,4):
            for j in range(0,4):
                self.G_blocks[i][j][2]=0

        #randnumspawn + gameovercheck + savestate fn
        if(self.flag==1):
            self.randnumspawn()
            self.gameovercheck()
            if(mode==1):
                self.savestate()

    #right func
    def right(self):
        global score

        #flag for no moves
        self.flag=0

        #for every line
        for i in range (0,4):
            for j in reversed(range(0,4)):
                #if there is a number
                if(self.G_blocks[i][j][1]==1):
                    #if the number is at the edge
                    if(j==3):
                        print("already at edge / Do nothing")
                        continue
                    #find the nearest number or edge
                    for k in range(j+1,4):
                        #if found a number
                        if(self.G_blocks[i][k][1]==1):
                            #if the numbers are the same and the 'k' number hasn't been combined yet -> combine them
                            if(self.G_blocks[i][k][0].cget("text")==self.G_blocks[i][j][0].cget("text") and self.G_blocks[i][k][2]==0):
                                self.G_blocks[i][k][0].config(text=int(self.G_blocks[i][k][0].cget("text"))*2)
                                self.G_blocks[i][k][0].config(bg=self.blockcolors(i,k))
                                self.G_blocks[i][k][2]=1

                                self.G_blocks[i][j][1]=0
                                self.G_blocks[i][j][0].config(text='')
                                self.G_blocks[i][j][0].config(bg="#e7ecf0")

                                self.flag=1

                                if(mode==0):
                                    score+=int(self.G_blocks[i][k][0].cget("text"))
                                    self.score_label.config(text=str(score))
                                print("combined")

                            #if the numbers aren't the same or the 'k' number has already been combined -> move the number to the blank space next to the 'k' number
                            else:
                                #if not already in place
                                if not(j==k-1):
                                    self.G_blocks[i][k-1][0].config(text=self.G_blocks[i][j][0].cget("text"))
                                    self.G_blocks[i][k-1][0].config(bg=self.blockcolors(i,k-1))
                                    self.G_blocks[i][k-1][1]=1

                                    self.G_blocks[i][j][1]=0
                                    self.G_blocks[i][j][0].config(text='')
                                    self.G_blocks[i][j][0].config(bg="#e7ecf0")

                                    self.flag=1
                                    print("not combined / placed next to the number")
                                else:
                                    print("numbers not the same or already combined / Do nothing")

                            #break out
                            break

                        #if didn't find a number(edge) -> move the number to the edge
                        if(k==3):
                            self.G_blocks[i][k][0].config(text=self.G_blocks[i][j][0].cget("text"))
                            self.G_blocks[i][k][0].config(bg=self.blockcolors(i,k))
                            self.G_blocks[i][k][1]=1

                            self.G_blocks[i][j][1]=0
                            self.G_blocks[i][j][0].config(text='')
                            self.G_blocks[i][j][0].config(bg="#e7ecf0")

                            self.flag=1
                            print("Didn't find a number / moved to edge")

        #reset [2] values
        for i in range(0,4):
            for j in range(0,4):
                self.G_blocks[i][j][2]=0

        #randnumspawn + gameovercheck + savestate fn
        if(self.flag==1):
            self.randnumspawn()
            self.gameovercheck()
            if(mode==1):
                self.savestate()

    #down func
    def down(self):
        global score

        #flag for no moves
        self.flag=0

        #for every line
        for i in range (0,4):
            for j in reversed(range(0,4)):
                #if there is a number
                if(self.G_blocks[j][i][1]==1):
                    #if the number is at the edge
                    if(j==3):
                        print("already at edge / Do nothing")
                        continue
                    #find the nearest number or edge
                    for k in range(j+1,4):
                        #if found a number
                        if(self.G_blocks[k][i][1]==1):
                            #if the numbers are the same and the 'k' number hasn't been combined yet -> combine them
                            if(self.G_blocks[k][i][0].cget("text")==self.G_blocks[j][i][0].cget("text") and self.G_blocks[k][i][2]==0):
                                self.G_blocks[k][i][0].config(text=int(self.G_blocks[k][i][0].cget("text"))*2)
                                self.G_blocks[k][i][0].config(bg=self.blockcolors(k,i))
                                self.G_blocks[k][i][2]=1

                                self.G_blocks[j][i][1]=0
                                self.G_blocks[j][i][0].config(text='')
                                self.G_blocks[j][i][0].config(bg="#e7ecf0")

                                self.flag=1

                                if(mode==0):
                                    score+=int(self.G_blocks[k][i][0].cget("text"))
                                    self.score_label.config(text=str(score))
                                print("combined")

                            #if the numbers aren't the same or the 'k' number has already been combined -> move the number to the blank space next to the 'k' number
                            else:
                                #if not already in place
                                if not(j==k-1):
                                    self.G_blocks[k-1][i][0].config(text=self.G_blocks[j][i][0].cget("text"))
                                    self.G_blocks[k-1][i][0].config(bg=self.blockcolors(k-1,i))
                                    self.G_blocks[k-1][i][1]=1

                                    self.G_blocks[j][i][1]=0
                                    self.G_blocks[j][i][0].config(text='')
                                    self.G_blocks[j][i][0].config(bg="#e7ecf0")

                                    self.flag=1
                                    print("not combined / placed next to the number")
                                else:
                                    print("numbers not the same or already combined / Do nothing")

                            #break out
                            break

                        #if didn't find a number(edge) -> move the number to the edge
                        if(k==3):
                            self.G_blocks[k][i][0].config(text=self.G_blocks[j][i][0].cget("text"))
                            self.G_blocks[k][i][0].config(bg=self.blockcolors(k,i))
                            self.G_blocks[k][i][1]=1

                            self.G_blocks[j][i][1]=0
                            self.G_blocks[j][i][0].config(text='')
                            self.G_blocks[j][i][0].config(bg="#e7ecf0")

                            self.flag=1
                            print("Didn't find a number / moved to edge")

        #reset [2] values
        for i in range(0,4):
            for j in range(0,4):
                self.G_blocks[i][j][2]=0

        #randnumspawn + gameovercheck + savestate fn
        if(self.flag==1):
            self.randnumspawn()
            self.gameovercheck()
            if(mode==1):
                self.savestate()

#######################################################################################################################################################################################################

#start program
root=None

def start():
    global mode
    global state
    global score
    global transparency,transparency_backup

    global root

    mode=0

    state=0

    score=0

    transparency=1
    transparency_backup=1

    root = Tk()
    root.focus_force()
    root.title('2048+')
    root.resizable(0,0)
    T024=T048(root)
    root.mainloop()

if __name__ == '__main__':
    start()
