#-*- coding: cp949 -*-
from Tkinter import *
import tkMessageBox
import winsound
import random

#deck data
NUM = {'A' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '1' : 10, 'J' : 11, 'Q' : 12, 'K' : 13} #1 = 10

SPADE = ['♤A', '♤2', '♤3', '♤4', '♤5', '♤6', '♤7', '♤8', '♤9', '♤10', '♤J', '♤Q', '♤K']
DIA = ['◇A', '◇2', '◇3', '◇4', '◇5', '◇6', '◇7', '◇8', '◇9', '◇10', '◇J', '◇Q', '◇K']
CLOVER= ['♧A', '♧2', '♧3', '♧4', '♧5', '♧6', '♧7', '♧8', '♧9', '♧10', '♧J', '♧Q', '♧K']
HEART= ['♡A', '♡2', '♡3', '♡4', '♡5', '♡6', '♡7', '♡8', '♡9', '♡10', '♡J', '♡Q', '♡K']

#difficulty
DIFFICULTY = 0

#score
score = 500

#state(for backup)
state = -1

#trans
transparency=1
transparency_backup=1

class spider():
    def __init__(self, master):
        #create menubar
        self.v=IntVar()
        self.v.set(0)

        self.menu=Menu(root,tearoff=0)
        self.gamesubmenu=Menu(self.menu,tearoff=0)
        self.gamesubmenu.add_command(label=unicode("새 게임",'cp949'),command=lambda : self.restart(-1))
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_radiobutton(label=unicode("초급",'cp949'),variable=self.v,value=0,command=lambda : self.restart(0))
        self.gamesubmenu.add_radiobutton(label=unicode("중급",'cp949'),variable=self.v,value=1,command=lambda : self.restart(1))
        self.gamesubmenu.add_radiobutton(label=unicode("고급",'cp949'),variable=self.v,value=2,command=lambda : self.restart(2))
        self.gamesubmenu.add_separator()
        self.gamesubmenu.add_command(label=unicode("닫기",'cp949'),command=root.destroy)
        self.menu.add_cascade(label=unicode("게임",'cp949'),menu=self.gamesubmenu)

        self.helpsubmenu=Menu(self.menu,tearoff=0)
        self.helpsubmenu.add_command(label=unicode("조작키",'cp949'),command=lambda : tkMessageBox.showinfo(unicode("조작키",'cp949'),unicode("Z : 수 무르기\n\nF2 : 새 게임\nF4 : 창 숨기기/보이기",'cp949'),parent=root))
        self.menu.add_cascade(label=unicode("도움말",'cp949'),menu=self.helpsubmenu)

        root.config(menu=self.menu)

        #create top ui
        self.topui_frame = Frame(root)
        self.topui_frame.pack(fill = 'x')

        self.score_label = Label(self.topui_frame, text = "SCORE : 500")
        self.score_label.pack(side = LEFT)

        self.trans_sdr=Scale(self.topui_frame, from_ = 0, to = 100, orient = HORIZONTAL, showvalue = False, sliderlength = 10, length = 50, command = self.settransparency)
        self.trans_sdr.set(transparency * 100)
        self.trans_sdr.pack(side = RIGHT)

        #create board
        self.board_frame = Frame(root)
        self.board_frame.pack(fill = BOTH, expand = True)

        self.board_frame_bottom = Frame(root, bg = "light grey")
        self.board_frame_bottom.pack(side = BOTTOM, fill = X)

        self.create_board(DIFFICULTY)

        #click empty space or right click for cancel
        self.board_frame.bind("<Button-1>", lambda e : self.clear_highlights())
        root.bind("<Button-3>", lambda e : self.clear_highlights())

        #bind buttons
        root.bind('<F4>',lambda e : self.hidewindow())
        root.bind('<F2>',lambda e : self.restart(-1))
        root.bind('<z>',lambda e : self.undo())
        root.bind('<Z>',lambda e : self.undo())

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

    #create board
    def create_board(self, difficulty):
        #board 2 dimentional array
        self.G_board = [[] for i in range(10)]

        #variables for backup
        self.score_backup = [[] for i in range(21)]
        self.G_board_backup = [[[] for i in range(10)] for j in range(21)]
        self.progress_backup = [[[] for i in range(8)] for j in range(21)]
        self.G_deck_backup = [[] for i in range(21)]

        #create deck
        if(difficulty == 0):
            self.G_deck = SPADE * 8
        if(difficulty == 1):
            self.G_deck = SPADE * 4 + DIA * 4
        if(difficulty == 2):
            self.G_deck = SPADE * 2 + DIA * 2 + CLOVER * 2 + HEART * 2

        random.shuffle(self.G_deck)

        #place on board
        for i in range(10):
            if(i <= 3):
                sliced = self.G_deck[:6]
                for j in range(6):
                    self.G_board[i].append([Label(self.board_frame, text = "???"), sliced[j], 0]) #[0] : label, [1] : card, [2] : 0 = hide, 1 = show
                    self.G_board[i][j][0].bind("<Button-1>", lambda e, x = i, y = j : self.click_handler(x, y))
                    self.G_board[i][j][0].grid(row = j, column = i)
                self.G_deck = self.G_deck[6:]
            else:
                sliced = self.G_deck[:5]
                for j in range(5):
                    self.G_board[i].append([Label(self.board_frame, text = "???"), sliced[j], 0]) #[0] : label, [1] : card, [2] : 0 = hide, 1 = show
                    self.G_board[i][j][0].bind("<Button-1>", lambda e, x = i, y = j : self.click_handler(x, y))
                    self.G_board[i][j][0].grid(row = j, column = i)
                self.G_deck = self.G_deck[5:]

            #min size column
            self.board_frame.grid_columnconfigure(i, minsize=33)

            #flip over topmost
        for i in range(10):
            self.G_board[i][len(self.G_board[i]) - 1][2] = 1
            self.G_board[i][len(self.G_board[i]) - 1][0].config(text = unicode(self.G_board[i][len(self.G_board[i]) - 1][1], 'cp949'))

        #clicked tile
        self.clicked = (None, None)

        #available tile(temp)
        self.available_t = [[None] for i in range(10)]

        #bottom ui
        self.progress = []
        if(difficulty == 0):
            for i in range(8):
                self.progress.append(Label(self.board_frame_bottom, text = unicode('♤', 'cp949'), bg = "light grey", fg = "dark grey"))
                self.progress[i].grid(row = i / 4, column = i % 4)
        if(difficulty == 1):
            for i in range(8):
                if(i % 4 == 0 or i % 4 == 1):
                    self.progress.append(Label(self.board_frame_bottom, text = unicode('♤', 'cp949'), bg = "light grey", fg = "dark grey"))
                else:
                    self.progress.append(Label(self.board_frame_bottom, text = unicode('◇', 'cp949'), bg = "light grey", fg = "dark grey"))
                self.progress[i].grid(row = i / 4, column = i % 4)
        if(difficulty == 2):
            for i in range(8):
                if(i % 4 == 0):
                    self.progress.append(Label(self.board_frame_bottom, text = unicode('♤', 'cp949'), bg = "light grey", fg = "dark grey"))
                if(i % 4 == 1):
                    self.progress.append(Label(self.board_frame_bottom, text = unicode('◇', 'cp949'), bg = "light grey", fg = "dark grey"))
                if(i % 4 == 2):
                    self.progress.append(Label(self.board_frame_bottom, text = unicode('♧', 'cp949'), bg = "light grey", fg = "dark grey"))
                if(i % 4 == 3):
                    self.progress.append(Label(self.board_frame_bottom, text = unicode('♡', 'cp949'), bg = "light grey", fg = "dark grey"))
                self.progress[i].grid(row = i / 4, column = i % 4)

        self.mid_label = Label(self.board_frame_bottom, fg = "black", bg = "light grey")
        self.mid_label.grid(row = 0, rowspan = 2, column = 4)

        self.deck = Label(self.board_frame_bottom, text = "???\n(50)", bg = "light grey")
        self.deck.bind("<Button-1>", lambda e : self.draw_cards())
        self.deck.grid(row = 0, column = 5, rowspan = 2, sticky = E)

        self.board_frame_bottom.columnconfigure(4, weight = 1)

        #click empty space or right click for cancel (re-enable clear for after success)
        self.board_frame.bind("<Button-1>", lambda e : self.clear_highlights())
        root.bind("<Button-3>", lambda e : self.clear_highlights())

        #save first to zero!
        self.savestate()

    #restart function
    def restart(self, difficulty):
        global DIFFICULTY, score, state

        #if same as previous -> do nothing
        if(difficulty == DIFFICULTY):
            return None

        #save difficulty
        if(difficulty != -1):
            DIFFICULTY = difficulty

        #restart
            #reset score
        score = 500
        self.score_label.config(text = "SCORE : 500")

            #reset state
        state = -1

            #destroy previous board
        self.clear_highlights()

        for i in range(10):
            for j in reversed(range(len(self.G_board[i]))):
                self.G_board[i][j][0].unbind("<Button-1>")
                self.G_board[i][j][0].destroy()
                self.G_board[i] = self.G_board[i][:j]

        for i in range(8):
            self.progress[i].destroy()

        self.mid_label.destroy()

        self.deck.unbind("<Button-1>")
        self.deck.destroy()

            #create new board
        self.create_board(DIFFICULTY)

    #save state function
    def savestate(self):
        global state

        #save state (board)
        if(state == 20):
            #score
            for i in range(0, 20):
                self.score_backup[i] = self.score_backup[i + 1]
            self.score_backup[state] = score

            #board
            for i in range(0, 20):
                for j in range(10):
                    self.G_board_backup[i][j] = [[] for _ in range(len(self.G_board_backup[i + 1][j]))]
                    for k in range(len(self.G_board_backup[i+1][j])):
                        self.G_board_backup[i][j][k] = self.G_board_backup[i + 1][j][k]
            for i in range(10):
                self.G_board_backup[state][i] = [[] for _ in range(len(self.G_board[i]))]
                for j in range(len(self.G_board[i])):
                    self.G_board_backup[state][i][j] = [self.G_board[i][j][1], self.G_board[i][j][2]] #[0] : card / [1] : show or hide

            #progress
            for i in range(0, 20):
                for j in range(8):
                    self.progress_backup[i][j] = self.progress_backup[i + 1][j]
            for i in range(8):
                self.progress_backup[state][i] = self.progress[i].cget("fg") #complete or not

            #deck
            for i in range(0, 20):
                self.G_deck_backup[i] = self.G_deck_backup[i + 1]
            self.G_deck_backup[state] = self.G_deck #deck
        elif(state < 20):
            state += 1

            #score
            self.score_backup[state] = score

            #board
            for i in range(10):
                self.G_board_backup[state][i] = [[] for _ in range(len(self.G_board[i]))]
                for j in range(len(self.G_board[i])):
                    self.G_board_backup[state][i][j] = [self.G_board[i][j][1], self.G_board[i][j][2]] #[0] : card / [1] : show or hide

            #progress
            for i in range(8):
                self.progress_backup[state][i] = self.progress[i].cget("fg") #complete or not

            #deck
            self.G_deck_backup[state] = self.G_deck #deck

    #undo func
    def undo(self):
        global state
        global score

        #restore state + make new grid
        if(state > 0):
            #first "destroy" previous board
            self.clear_highlights()

            for i in range(10):
                for j in reversed(range(len(self.G_board[i]))):
                    self.G_board[i][j][0].unbind("<Button-1>")
                    self.G_board[i][j][0].destroy()
                    self.G_board[i] = self.G_board[i][:j]

            #score
            score = self.score_backup[state - 1]
            score_t = "SCORE : " + str(score)
            self.score_label.config(text = score_t)

            #board
            for i in range(10):
                for j in range(len(self.G_board_backup[state - 1][i])):
                    self.G_board[i].append([Label(self.board_frame, text = "???"), self.G_board_backup[state - 1][i][j][0], self.G_board_backup[state - 1][i][j][1]])
                    self.G_board[i][j][0].bind("<Button-1>", lambda e, x = i, y = j : self.click_handler(x, y))
                    self.G_board[i][j][0].grid(row = j, column = i)

                    if(self.G_board_backup[state - 1][i][j][1] == 1):
                        self.G_board[i][j][0].config(text = unicode(self.G_board_backup[state - 1][i][j][0], 'cp949'))

                    #min size column
                    self.board_frame.grid_columnconfigure(i, minsize=33)

            #progress
            for i in range(8):
                self.progress[i].config(fg = self.progress_backup[state - 1][i])

            #deck
            self.G_deck = self.G_deck_backup[state - 1]

            if(len(self.G_deck) == 0):
                self.deck.config(text = '')
            else:
                d_text= "???\n" + "(" + str(len(self.G_deck)) + ")"
                self.deck.config(text = d_text)

            #reset clicked
            self.clicked = (None, None)

            #shift down state
            state -= 1

    #clear highlights
    def clear_highlights(self):
        #reset clicked
        self.clicked = (None, None)

        #clear clicked
        for i in range(10):
            for j in range(len(self.G_board[i])):
                if(self.G_board[i][j][0].cget("bg") != "SystemButtonFace"):
                    self.G_board[i][j][0].config(bg = "SystemButtonFace")

        #clear available
        for i in range(10):
            try:
                self.available_t[i].unbind("<Button-1>")
                self.available_t[i].destroy()
            except:
                pass

    #highlight func
    def highlight(self, x, y_start, y_end):
        #highlight clicked pile
        for i in range(y_start, y_end + 1):
            self.G_board[x][i][0].config(bg = "lightsteelblue")

        #highlight available
        for i in range(10):
            #if same as clicked -> pass
            if(i == x):
                pass
            else:
                self.available_t[i] = Label(self.board_frame, text = "     ", bg = "slategrey")
                self.available_t[i].bind("<Button-1>", lambda e, x_before = x, x_after = i, y_s = y_start, y_e = y_end  : self.move(x_before, x_after, y_s, y_e))
                self.available_t[i].grid(row = len(self.G_board[i]), column = i)

    #full_set function
    def full_set(self, x_after):
        global score

        #scan for a king
        king_idx = None
        for i in range(len(self.G_board[x_after])):
            if(self.G_board[x_after][i][0].cget("text")[1] == 'K'):
                king_idx = i

        #if there is no king or king was moved or ace is not the last card -> do nothing
        if(king_idx == None or king_idx == len(self.G_board[x_after]) - 1 or self.G_board[x_after][len(self.G_board[x_after]) - 1][0].cget("text")[1] != 'A'):
            return None

        #scan down column from king -> if invalid during scan -> do nothing
        for i in range(king_idx + 1, len(self.G_board[x_after])):
            if not(self.G_board[x_after][i][0].cget("text")[0] == self.G_board[x_after][i-1][0].cget("text")[0] \
               and NUM[self.G_board[x_after][i][0].cget("text")[1]] + 1 == NUM[self.G_board[x_after][i-1][0].cget("text")[1]]):
                return None

        #move full set to the bottom + remove from board
        for i in range(8):
            if(self.progress[i].cget("text") == self.G_board[x_after][len(self.G_board[x_after]) - 1][0].cget("text")[0]):
                if(self.progress[i].cget("fg") == "dark grey"):
                    self.progress[i].config(fg = "black")
                    break

        for i in reversed(range(king_idx, len(self.G_board[x_after]))):
            self.G_board[x_after][i][0].unbind("<Button-1>")
            self.G_board[x_after][i][0].destroy()
            self.G_board[x_after] = self.G_board[x_after][:i]

        #if no open card -> flip over topmost card
        try:
            if(self.G_board[x_after][len(self.G_board[x_after]) - 1][2] == 0):
                self.G_board[x_after][len(self.G_board[x_after]) - 1][2] = 1
                self.G_board[x_after][len(self.G_board[x_after]) - 1][0].config(text = unicode(self.G_board[x_after][len(self.G_board[x_after]) - 1][1], 'cp949'))
        except:
            pass

        #update score
        score += 100
        score_t = "SCORE : " + str(score)
        self.score_label.config(text = score_t)

        #check for success
        success = True
        for i in range(8):
            if(self.progress[i].cget("fg") == "dark grey"):
                success = False
                break
        if success:
            self.mid_label.config(text = unicode("성공!!", 'cp949'), fg = "dark green")

            #play success sound
            winsound.PlaySound("SystemAsterisk",winsound.SND_ASYNC)

            #message stay (disable clear message)
            self.board_frame.unbind("<Button-1>")
            root.unbind("<Button-3>")

    #draw cards function
    def draw_cards(self):
        global score

        #check if possible (rule) -> if not valid -> warning
        for i in range(10):
            if(len(self.G_board[i]) == 0):
                self.mid_label.config(text = unicode("모든 슬롯에 한 장 이상의\n카드가 놓여있어야 합니다!", 'cp949'), fg = "red")
                return None

        #check if possible (deck != 0)
        if(len(self.G_deck) == 0):
            return None

        #clear all highlights
        self.clear_highlights()

        #draw cards and place them on the board
        drawed = self.G_deck[:10]
        for i in range(10):
            self.G_board[i].append([Label(self.board_frame, text = unicode(drawed[i], 'cp949')), drawed[i], 1]) #[0] : label, [1] : card, [2] : 0 = hide, 1 = show
            self.G_board[i][len(self.G_board[i]) - 1][0].bind("<Button-1>", lambda e, x = i, y = len(self.G_board[i]) - 1 : self.click_handler(x, y))
            self.G_board[i][len(self.G_board[i]) - 1][0].grid(row = len(self.G_board[i]) - 1, column = i)
        self.G_deck = self.G_deck[10:]

        #check if any column has a full set
        for i in range(10):
            self.full_set(i)

        #update deck label
        if(len(self.G_deck) == 0):
            self.deck.config(text = '')
        else:
            d_text= "???\n" + "(" + str(len(self.G_deck)) + ")"
            self.deck.config(text = d_text)

        #update score
        score -= 1
        score_t = "SCORE : " + str(score)
        self.score_label.config(text = score_t)

        #after move, save state + clear message
        self.mid_label.config(text = '')
        self.savestate()

    #move function
    def move(self, x_before, x_after, y_s, y_e):
        global score

        #first clear all highlights
        self.clear_highlights()

        #check if valid
        valid = False
        try:
            if(NUM[self.G_board[x_before][y_s][0].cget("text")[1]] + 1 == NUM[self.G_board[x_after][len(self.G_board[x_after]) - 1][0].cget("text")[1]]):
                valid = True
                print("valid")
        except:
            valid = True
            print("valid")
##        valid = True #testing
        #if valid -> move
        if valid:
            #copy from before to after
            for i in range(y_s, y_e + 1):
                self.G_board[x_after].append([Label(self.board_frame, text = self.G_board[x_before][i][0].cget("text")), self.G_board[x_before][i][1], self.G_board[x_before][i][2]])
                self.G_board[x_after][len(self.G_board[x_after]) - 1][0].bind("<Button-1>", lambda e, x = x_after, y = len(self.G_board[x_after]) - 1 : self.click_handler(x, y))
                self.G_board[x_after][len(self.G_board[x_after]) - 1][0].grid(row = len(self.G_board[x_after]) - 1, column = x_after)

            #delete from before
            for i in reversed(range(y_s, y_e + 1)):
                self.G_board[x_before][i][0].unbind("<Button-1>")
                self.G_board[x_before][i][0].destroy()
                self.G_board[x_before] = self.G_board[x_before][:i]

        #if not valid -> warning + do nothing
        else:
            self.mid_label.config(text = unicode("내림차순이 아닙니다!", 'cp949'), fg = "red")
            return None

        #if before left an empty column -> flip over topmost card
        if not(len(self.G_board[x_before]) == 0):
            self.G_board[x_before][len(self.G_board[x_before]) - 1][2] = 1
            self.G_board[x_before][len(self.G_board[x_before]) - 1][0].config(text = unicode(self.G_board[x_before][len(self.G_board[x_before]) - 1][1], 'cp949'))

        #update score
        score -= 1
        score_t = "SCORE : " + str(score)
        self.score_label.config(text = score_t)

        #check if after has a full set
        self.full_set(x_after)

        #after move, save state
        self.savestate()

    #click handler
    def click_handler(self, x, y):
        #if clicked on hidden or clicked on clicked -> do nothing
        if(self.G_board[x][y][0].cget("text") == "???" or self.clicked == (x, y)):
            self.clicked = (None, None)
            self.clear_highlights()
            return None

        #first clear all highlights
        self.clear_highlights()

        #scan down column
        valid = False
        y_end = y
        while True:
            try:
                if(self.G_board[x][y_end][0].cget("text")[0] == self.G_board[x][y_end + 1][0].cget("text")[0] \
                   and NUM[self.G_board[x][y_end][0].cget("text")[1]] - 1 == NUM[self.G_board[x][y_end + 1][0].cget("text")[1]]):
                    y_end += 1
                else:
                    break
            except:
                valid = True
                break

        #if valid -> highlight
        if valid:
            self.clicked = (x, y)
            self.highlight(x, y, y_end)
            self.mid_label.config(text = '')

        #if not valid -> warning
        else:
            self.mid_label.config(text = unicode("옮길 카드들이 모두 같은 짝패\n이고 내림차순 이어야 합니다!", 'cp949'), fg = "red")

#######################################################################################################################################################################################################

#start program
root=None

def start():
    global DIFFICULTY
    global score
    global state
    global transparency, transparency_backup

    global root

    #difficulty
    DIFFICULTY = 0

    #score
    score = 500

    #state(for backup)
    state = -1

    transparency=1
    transparency_backup=1

    root = Tk()
    root.focus_force()
    root.title('Spider Solitaire')
    root.resizable(0,1)
    ss=spider(root)
    root.mainloop()

if __name__ == '__main__':
    start()
