from Tkinter import *
import sys
import time

sys.setrecursionlimit(3000)

#global variables
fast_forward=0
speed=0

row=34
col=65

start_node=(row-1)//2*col+8
end_node=((row-1)//2+1)*col-9

visualizer_running=0
start_clicked=0
end_clicked=0

#the visualizer
class visualizer():
    def __init__(self,master):
        #top ui
        self.top_ui_frame=Frame(root)
        self.top_ui_frame.grid(row=0)

        self.alg=IntVar()
        self.alg_dijkstra=Radiobutton(self.top_ui_frame,font=("courier",10,"normal"),text="Dijkstra's",variable=self.alg,value=0)
        self.alg_astar=Radiobutton(self.top_ui_frame,font=("courier",10,"normal"),text="A* Search",variable=self.alg,value=1)

        self.alg_dijkstra.grid(row=0,column=0,sticky=W)
        self.alg_astar.grid(row=0,column=1,sticky=W)

        self.visualize_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Visualize Algorithm!",relief="ridge",command=self.alg_start)
        self.visualize_btn.grid(row=1,column=0,columnspan=2,sticky=E+W)

        self.speed_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Speed")
        self.speed_label.grid(row=0,column=2,padx=(10,0),sticky=W)
        self.speed_sdr=Scale(self.top_ui_frame,orient=HORIZONTAL,from_=0,to=400,showvalue=False,sliderlength=10,length=100,command=self.set_speed)
        self.speed_sdr.grid(row=0,column=3)

        self.FF_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Fast Forward",relief="ridge",command=self.FF,state=DISABLED)
        self.FF_btn.grid(row=1,column=2,columnspan=2,padx=(10,0),sticky=E+W)

        self.start_color=Label(self.top_ui_frame,width=2,height=1,bg="#00dd00")
        self.start_color.grid(row=0,column=4,padx=(10,0))
        self.start_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Start Node")
        self.start_label.grid(row=0,column=5,sticky=W)

        self.target_color=Label(self.top_ui_frame,width=2,height=1,bg="#ee4400")
        self.target_color.grid(row=1,column=4,padx=(10,0))
        self.target_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Target Node")
        self.target_label.grid(row=1,column=5,sticky=W)

        self.unvisited_color=Label(self.top_ui_frame,width=2,height=1,bg="white")
        self.unvisited_color.grid(row=0,column=6,padx=(10,0))
        self.unvidited_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Unvisited Node")
        self.unvidited_label.grid(row=0,column=7,sticky=W)

        self.wall_color=Label(self.top_ui_frame,width=2,height=1,bg="#afd8f8")
        self.wall_color.grid(row=1,column=6,padx=(10,0))
        self.wall_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Wall Node")
        self.wall_label.grid(row=1,column=7,sticky=W)

        self.visited_color=Label(self.top_ui_frame,width=2,height=1,bg="#98fb98")
        self.visited_color.grid(row=0,column=8,padx=(10,0))
        self.visited_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Visited Node")
        self.visited_label.grid(row=0,column=9,sticky=W)

        self.shortest_color=Label(self.top_ui_frame,width=2,height=1,bg="#fcfc64")
        self.shortest_color.grid(row=1,column=8,padx=(10,0))
        self.shortest_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Shortest-path Node")
        self.shortest_label.grid(row=1,column=9,sticky=W)

        self.clear_walls_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Clear Walls",relief="ridge",command=self.clear_walls)
        self.clear_walls_btn.grid(row=0,column=10,padx=(3,0))

        self.clear_path_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Clear Path",relief="ridge",command=self.clear_path)
        self.clear_path_btn.grid(row=1,column=10,padx=(3,0),sticky=E+W)

        self.reset_board_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Reset\nBoard",relief="ridge",command=self.reset_board)
        self.reset_board_btn.grid(row=0,column=11,rowspan=2,sticky=N+S)

        #create grid
        self.grid_frame=Frame(root)
        self.grid_frame.grid(row=1)

        self.canvas=Canvas(self.grid_frame,relief="solid",width=col*15,height=row*15,bg="white")
        self.canvas.pack()

        self.create_grid()

    #Fast forward
    def FF(self):
        global fast_forward
        fast_forward=1

    #set speed
    def set_speed(self,val):
        global speed
        speed=(500-int(val))/10000.0

    def create_grid(self):
        self.grid=[]
        for i in range(row*col):
            #[0] btn /[1] is_visited /[2] previous index /[3] type(0 -> normal /1 -> wall /2 -> start_node /3 -> end_node) /[4] distance_from_start_node /[5] [G,H,F] for A*
            self.grid.append([self.canvas.create_polygon(1+(i%col)*15,1+(i/col)*15,1+(i%col)*15+15,1+(i/col)*15,1+(i%col)*15+15,1+(i/col)*15+15,1+(i%col)*15,1+(i/col)*15+15,outline="#afd8f8",fill="white"),0,None,0,float('inf'),[float('inf'),float('inf'),float('inf')]])
            self.canvas.tag_bind(self.grid[i][0],"<Button-1>",lambda e,a=i : self.click(a))

        #bind to canvas
        self.prev_grid=None
        self.canvas.bind("<B1-Motion>",self.draw)
        self.canvas.bind("<ButtonRelease-1>",self.unclick)

        #start and end
        self.grid[start_node][3]=2
        self.canvas.itemconfig(self.grid[start_node][0],fill="#00dd00")
        self.grid[end_node][3]=3
        self.canvas.itemconfig(self.grid[end_node][0],fill="#ee4400")

    def clear_walls(self):
        #first clear path
        self.clear_path()

        #clear walls
        for i in range(row*col):
            if(self.grid[i][3]==1):
                self.grid[i][3]=0
                self.canvas.itemconfig(self.grid[i][0],fill="white")

    def clear_path(self):
        #clear path(is_visited)
        for i in range(row*col):
            if(self.grid[i][1]==1):
                self.grid[i][1]=0
                if (i!=start_node and i!=end_node and self.grid[i][3]!=1):
                    self.canvas.itemconfig(self.grid[i][0],fill="white")

        #reset previous, distance, GHF-cost data
        for i in range(row*col):
            self.grid[i][2]=None
            self.grid[i][4]=float('inf')
            self.grid[i][5]=[float('inf'),float('inf'),float('inf')]

    def reset_board(self):
        global start_node,end_node

        #the 2 clearing funcs
        self.clear_path()
        self.clear_walls()

        #replace start and end nodes
        for i in range(row*col):
            if(self.grid[i][3]==2):
                self.grid[i][3]=0
                self.canvas.itemconfig(self.grid[i][0],fill="white")
            if(self.grid[i][3]==3):
                self.grid[i][3]=0
                self.canvas.itemconfig(self.grid[i][0],fill="white")

        start_node=(row-1)//2*col+8
        end_node=((row-1)//2+1)*col-9
        self.grid[start_node][3]=2
        self.grid[end_node][3]=3
        self.canvas.itemconfig(self.grid[start_node][0],fill="#00dd00")
        self.canvas.itemconfig(self.grid[end_node][0],fill="#ee4400")

    def unclick(self,event):
        global start_clicked,end_clicked
        start_clicked=0
        end_clicked=0

    def click(self,i):
        global start_clicked,end_clicked

        #if running do nothing
        if(visualizer_running==1):
            return None

        #save to previous
        self.prev_grid=i

        #if entered start or end node -> variable
        if(self.grid[i][3]==2):
            start_clicked=1
            return None
        if(self.grid[i][3]==3):
            end_clicked=1
            return None

        #if entered not (normal or wall) -> do nothing
        if(self.grid[i][3]>1):
            return None

        #wall -> not wall / not wall -> wall
        if(self.grid[i][3]==0):
            self.grid[i][3]=1
            self.canvas.itemconfig(self.grid[i][0],fill="#afd8f8")
        else:
            self.grid[i][3]=0
            self.canvas.itemconfig(self.grid[i][0],fill="white")

    def draw(self,event):
        global start_node,end_node

        #if running do nothing
        if(visualizer_running==1):
            return None

        #if overflow -> do nothing
        if not(((event.x-2)//15>=0 and (event.x-2)//15 <=col-1) and ((event.y-2)//15>=0 and (event.y-2)//15 <=row-1)):
            return None

        #set current grid
        i=((event.y-2)//15)*col+(event.x-2)//15

        #if same as previous
        if(i==self.prev_grid):
            return None

        #save to previous
        self.prev_grid=i

        #if start_end_clicked -> True -> move start/end node
        if(start_clicked==1):
            #if on a start/end node -> do nothing
            if(self.grid[i][3]==3):
                return None

            #remove previous start/end
            self.grid[start_node][3]=0
            self.canvas.itemconfig(self.grid[start_node][0],fill="white")

            #set new start/end
            start_node=i
            self.grid[start_node][3]=2
            self.canvas.itemconfig(self.grid[start_node][0],fill="#00dd00")

            return None
        if(end_clicked==1):
            #if on a start/end node -> do nothing
            if(self.grid[i][3]==2):
                return None

            #remove previous start/end
            self.grid[end_node][3]=0
            self.canvas.itemconfig(self.grid[end_node][0],fill="white")

            #set new start/end
            end_node=i
            self.grid[end_node][3]=3
            self.canvas.itemconfig(self.grid[end_node][0],fill="#ee4400")

            return None

        #if entered on a not (normal or wall) -> do nothing
        if(self.grid[i][3]>1):
            return None

        #wall -> not wall / not wall -> wall
        if(self.grid[i][3]==0):
            self.grid[i][3]=1
            self.canvas.itemconfig(self.grid[i][0],fill="#afd8f8")
        else:
            self.grid[i][3]=0
            self.canvas.itemconfig(self.grid[i][0],fill="white")

    def alg_start(self):
        global fast_forward,visualizer_running

        #disable/enable buttons + variables
        self.visualize_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.clear_walls_btn.config(state=DISABLED)
        self.clear_path_btn.config(state=DISABLED)
        self.reset_board_btn.config(state=DISABLED)

        visualizer_running=1

        #first clear path(if any)
        self.clear_path()

        #alg start
        if(self.alg.get()==0): #dijkstra
            #set start distance to zero
            self.grid[start_node][4]=0

            #start alg
            self.dijkstra(start_node)

        else: #astar
            #create arrays
            self.opened,self.closed=[],[]
            self.opened.append(start_node)

            #set start node values
            t_G=abs(start_node//col-start_node//col)+abs(start_node%col-start_node%col)
            t_H=abs(end_node//col-start_node//col)+abs(end_node%col-start_node%col)
            self.grid[start_node][5]=[t_G,t_H,t_G+t_H]

            #start alg
            self.astar()

        #disable/enable buttons + variables
        self.visualize_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.clear_walls_btn.config(state=NORMAL)
        self.clear_path_btn.config(state=NORMAL)
        self.reset_board_btn.config(state=NORMAL)

        fast_forward=0
        visualizer_running=0

    def dijkstra(self,current):
        #mark as visited
        self.grid[current][1]=1

        #visualize
        if current is not start_node:
            self.canvas.itemconfig(self.grid[current][0],fill="#98fb98")
            if not fast_forward:
                time.sleep(speed)
            root.update()

        #add 1 to neighbor nodes(if (normal(blank) or end) and node and not visited) + save previous
        if not(current-col<0): #up
            if((self.grid[current-col][3]==0 or self.grid[current-col][3]==3) and self.grid[current-col][1]==0):
                self.grid[current-col][4]=self.grid[current][4]+1
                self.grid[current-col][2]=current
        if not(current//col!=(current+1)//col): #right
            if((self.grid[current+1][3]==0 or self.grid[current+1][3]==3) and self.grid[current+1][1]==0):
                self.grid[current+1][4]=self.grid[current][4]+1
                self.grid[current+1][2]=current
        if not(current+col>=row*col): #down
            if((self.grid[current+col][3]==0 or self.grid[current+col][3]==3) and self.grid[current+col][1]==0):
                self.grid[current+col][4]=self.grid[current][4]+1
                self.grid[current+col][2]=current
        if not(current//col!=(current-1)//col): #left
            if((self.grid[current-1][3]==0 or self.grid[current-1][3]==3) and self.grid[current-1][1]==0):
                self.grid[current-1][4]=self.grid[current][4]+1
                self.grid[current-1][2]=current

        #find minimum grid(from unvisited)
        t_min=float('inf')
        t_min_idx=None

        for i in range(row*col):
            if(self.grid[i][1]==0 and (self.grid[i][3]==0 or self.grid[i][3]==3)):
                if(self.grid[i][4]<t_min):
                    t_min=self.grid[i][4]
                    t_min_idx=i

        #if the minimum is the end node -> success + animate
        if(t_min_idx==end_node):
            #print("success!",t_min)
            #if right next to the other -> return None
            if(t_min==1):
                return None

            #save path
            path=[]
            i=self.grid[end_node][2]
            while True:
                path.append(i)
                i=self.grid[i][2]
                if i == start_node :
                    break

            #show path
            for p in reversed(path):
                self.canvas.itemconfig(self.grid[p][0],fill="#fcfc64")
                root.update()
                time.sleep(.01)

            return None

        #if the minimum is none -> return None (failed)
        if(t_min_idx==None):
            return None

        #call dijkstra for min idx
        self.dijkstra(t_min_idx)

    def astar(self):
        while True:
            #from opened -> find the min F cost -> set that idx to current(temp variable)
            t_H_min,t_F_min=float('inf'),float('inf')
            t_F_min_idx=None
            for i in self.opened:
                #first calculate H cost
                self.grid[i][5][1]=abs(end_node//col-i//col)+abs(end_node%col-i%col)

                #find the minimum
                if(self.grid[i][5][2]<=t_F_min):
                    if(self.grid[i][5][2]==t_F_min):
                        if(self.grid[i][5][1]<t_H_min):
                            t_H_min=self.grid[i][5][1]
                            t_F_min=self.grid[i][5][2]
                            t_F_min_idx=i
                    else:
                        t_H_min=self.grid[i][5][1]
                        t_F_min=self.grid[i][5][2]
                        t_F_min_idx=i
            t_current=t_F_min_idx

            #if the minimum is none -> return None (failed)
            if(t_current==None):
                return None

            #remove current from opened and add that to closed
            self.opened.remove(t_current)
            self.closed.append(t_current)

            #print(self.opened,self.closed)
            #if current is the end node -> success
            if(t_current==end_node):
                #print("success",self.grid[end_node][5][0])
                #if right next to the other -> return None
                if(self.grid[end_node][5][0]==1):
                    return None

                #save path
                path=[]
                i=self.grid[end_node][2]
                while True:
                    path.append(i)
                    i=self.grid[i][2]
                    if i == start_node :
                        break

                #show path
                for p in reversed(path):
                    self.canvas.itemconfig(self.grid[p][0],fill="#fcfc64")
                    root.update()
                    time.sleep(.01)

                return None

            #search through neighbor nodes
            if not(t_current-col<0): #up
                t_neighbor_idx=t_current-col
                if((self.grid[t_neighbor_idx][3]==0 or self.grid[t_neighbor_idx][3]==3) and (t_neighbor_idx not in self.closed)):
                    #calculate new values
                    t_G=self.grid[t_current][5][0]+1
                    t_H=abs(end_node//col-t_neighbor_idx//col)+abs(end_node%col-t_neighbor_idx%col)

                    #if shorter or not in opened
                    if(((t_G+t_H)<self.grid[t_neighbor_idx][5][2]) or t_neighbor_idx not in self.opened):
                        #save new G,H,F cost + save parent(previous)
                        self.grid[t_neighbor_idx][5][0]=t_G
                        self.grid[t_neighbor_idx][5][2]=t_G+t_H
                        self.grid[t_neighbor_idx][2]=t_current

                        #if not in opened -> add to opened + mark as visited(except end node)
                        if(t_neighbor_idx not in self.opened):
                            self.opened.append(t_neighbor_idx)
                            if(t_neighbor_idx!=end_node):
                                self.grid[t_neighbor_idx][1]=1
                                #visualize
                                self.canvas.itemconfig(self.grid[t_neighbor_idx][0],fill="#98fb98")
                                if not fast_forward:
                                    time.sleep(speed)
                                root.update()

            if not(t_current//col!=(t_current+1)//col): #right
                t_neighbor_idx=t_current+1
                if((self.grid[t_neighbor_idx][3]==0 or self.grid[t_neighbor_idx][3]==3) and (t_neighbor_idx not in self.closed)):
                    #calculate new values
                    t_G=self.grid[t_current][5][0]+1
                    t_H=abs(end_node//col-t_neighbor_idx//col)+abs(end_node%col-t_neighbor_idx%col)

                    #if shorter or not in opened
                    if(((t_G+t_H)<self.grid[t_neighbor_idx][5][2]) or t_neighbor_idx not in self.opened):
                        #save new G,H,F cost + save parent(previous)
                        self.grid[t_neighbor_idx][5][0]=t_G
                        self.grid[t_neighbor_idx][5][2]=t_G+t_H
                        self.grid[t_neighbor_idx][2]=t_current

                        #if not in opened -> add to opened + mark as visited(except end node)
                        if(t_neighbor_idx not in self.opened):
                            self.opened.append(t_neighbor_idx)
                            if(t_neighbor_idx!=end_node):
                                self.grid[t_neighbor_idx][1]=1
                                #visualize
                                self.canvas.itemconfig(self.grid[t_neighbor_idx][0],fill="#98fb98")
                                if not fast_forward:
                                    time.sleep(speed)
                                root.update()

            if not(t_current+col>=row*col): #down
                t_neighbor_idx=t_current+col
                if((self.grid[t_neighbor_idx][3]==0 or self.grid[t_neighbor_idx][3]==3) and (t_neighbor_idx not in self.closed)):
                    #calculate new values
                    t_G=self.grid[t_current][5][0]+1
                    t_H=abs(end_node//col-t_neighbor_idx//col)+abs(end_node%col-t_neighbor_idx%col)

                    #if shorter or not in opened
                    if(((t_G+t_H)<self.grid[t_neighbor_idx][5][2]) or t_neighbor_idx not in self.opened):
                        #save new G,H,F cost + save parent(previous)
                        self.grid[t_neighbor_idx][5][0]=t_G
                        self.grid[t_neighbor_idx][5][2]=t_G+t_H
                        self.grid[t_neighbor_idx][2]=t_current

                        #if not in opened -> add to opened + mark as visited(except end node)
                        if(t_neighbor_idx not in self.opened):
                            self.opened.append(t_neighbor_idx)
                            if(t_neighbor_idx!=end_node):
                                self.grid[t_neighbor_idx][1]=1
                                #visualize
                                self.canvas.itemconfig(self.grid[t_neighbor_idx][0],fill="#98fb98")
                                if not fast_forward:
                                    time.sleep(speed)
                                root.update()

            if not(t_current//col!=(t_current-1)//col): #left
                t_neighbor_idx=t_current-1
                if((self.grid[t_neighbor_idx][3]==0 or self.grid[t_neighbor_idx][3]==3) and (t_neighbor_idx not in self.closed)):
                    #calculate new values
                    t_G=self.grid[t_current][5][0]+1
                    t_H=abs(end_node//col-t_neighbor_idx//col)+abs(end_node%col-t_neighbor_idx%col)

                    #if shorter or not in opened
                    if(((t_G+t_H)<self.grid[t_neighbor_idx][5][2]) or t_neighbor_idx not in self.opened):
                        #save new G,H,F cost + save parent(previous)
                        self.grid[t_neighbor_idx][5][0]=t_G
                        self.grid[t_neighbor_idx][5][2]=t_G+t_H
                        self.grid[t_neighbor_idx][2]=t_current

                        #if not in opened -> add to opened + mark as visited(except end node)
                        if(t_neighbor_idx not in self.opened):
                            self.opened.append(t_neighbor_idx)
                            if(t_neighbor_idx!=end_node):
                                self.grid[t_neighbor_idx][1]=1
                                #visualize
                                self.canvas.itemconfig(self.grid[t_neighbor_idx][0],fill="#98fb98")
                                if not fast_forward:
                                    time.sleep(speed)
                                root.update()

#start program
root=None

def start():
    global fast_forward,speed
    global row,col
    global start_node,end_node
    global visualizer_running,start_clicked,end_clicked

    #RESET GLOBAL VARIABLES
    fast_forward=0
    speed=0

    row=34
    col=65

    start_node=(row-1)//2*col+8
    end_node=((row-1)//2+1)*col-9

    visualizer_running=0
    start_clicked=0
    end_clicked=0

    #START
    global root
    root=Tk()
    root.focus_force()
    root.title("Path Finding Visualizer")
    root.resizable(0,0)
    vis=visualizer(root)
    root.mainloop()

if __name__ == '__main__':
    start()
