from Tkinter import *
import random
import time
import copy

############################
##bubble
##selection
##insertion
##quick
##merge
##heap
##
##radix
##shell
##
##counting
##gravity

##import winsound as ws
##
##def beepsound():
##    freq = 500    # range : 37 ~ 32767
##    dur = 1000     # ms
##    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)
##
##print(beepsound())
############################

############################################################################################################

#RAW soring Algs
#bubble
def sort_bubble(array):
    arr=copy.deepcopy(array)

    for i in range(len(arr)-1):
        for j in reversed(range(1,len(arr))):
            if(arr[j]<arr[j-1]):
                arr[j-1],arr[j]=arr[j],arr[j-1]

    return arr

#selection
def sort_selection(array):
    arr=copy.deepcopy(array)

    for i in range(len(arr)-1):
        t_min_idx=i

        for j in range(i+1,len(arr)):
            if(arr[j]<=arr[t_min_idx]):
                t_min_idx=j

        arr[i],arr[t_min_idx]=arr[t_min_idx],arr[i]

    return arr

#insertion
def sort_insertion(array):
    arr=copy.deepcopy(array)

    sorted_idx=0
    for i in range(1,len(arr)):
        for j in range(sorted_idx+1):
            if(j==0):
                if(arr[i]<=arr[j]):
                    t=arr.pop(i)
                    arr.insert(0,t)
                    break
            elif(arr[i]>=arr[j-1] and arr[i]<=arr[j]):
                    t=arr.pop(i)
                    arr.insert(j,t)
                    break

        sorted_idx+=1

    return arr

#quick
def sort_quick(array):
    arr=copy.deepcopy(array)

    def sort(low,high):
        if(high<=low):
            return None

        mid=partition(low,high)
        sort(low,mid-1)
        sort(mid,high)

    def partition(low,high):
        pivot=arr[(low+high)//2]
        while(low<=high):
            while(arr[low]<pivot):
                low+=1
            while(arr[high]>pivot):
                high-=1
            if(low<=high):
                arr[low],arr[high]=arr[high],arr[low]
                low,high=low+1,high-1

        return low

    sort(0,len(arr)-1)
    return arr

#merge(sliced arrays, without index passing)
##def sort_merge(array):
##    arr=copy.deepcopy(array)
##
##    def merge(left, right):
##        result=[]
##        left_count=0
##        right_count=0
##        try:
##            while True:
##                if left[left_count]>right[right_count]:
##                    result.append(right[right_count])
##                    right_count+=1
##                else:
##                    result.append(left[left_count])
##                    left_count+=1
##        except:
##            return result+left[left_count:]+right[right_count:]
##
##    def split_(arr):
##        if len(arr)<=1:
##            return arr
##        mid=len(arr)//2
##        leftList=arr[:mid]
##        rightList=arr[mid:]
##        leftList=split_(leftList)
##        rightList=split_(rightList)
##        return merge(leftList,rightList)
##
##    arr=split_(arr)
##    return arr

#merge(with indexes)
def sort_merge(array):
    arr=copy.deepcopy(array)

    def rMergeSort(A,l,r):
        if(l<r):
            m=(l+r)//2
            rMergeSort(A,l,m)
            rMergeSort(A,m+1,r)
            merge(A,l,m,r)

        return None

    def merge(A,l,m,r):
        B=[None]*len(array)
        i,k,j=l,l,m+1

        while(i<=m and j<=r):
            if(A[i]<=A[j]):
                B[k]=A[i]
                k+=1
                i+=1
            else:
                B[k]=A[j]
                k+=1
                j+=1
        while(i<=m):
            B[k]=A[i]
            k+=1
            i+=1
        while(j<=r):
            B[k]=A[j]
            k+=1
            j+=1

        for k in range(l,r+1):
            A[k]=B[k]

        return None

    rMergeSort(arr,0,len(arr)-1)
    return arr

#heap
def sort_heap(array):
    arr=copy.deepcopy(array)

    def sort_(unsorted):
        n=len(unsorted)

        for i in reversed(range(0,n//2)):
            heapify(unsorted,i,n)

        for i in reversed(range(1,n)):
            unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
            heapify(unsorted, 0, i)

    def heapify(unsorted,index,heap_size):
        largest = index
        left_index=2*index+1
        right_index=2*index+2
        if(left_index<heap_size and (unsorted[left_index]>unsorted[largest])):
            largest=left_index
        if(right_index<heap_size and (unsorted[right_index]>unsorted[largest])):
            largest=right_index
        if(largest!=index):
            unsorted[largest],unsorted[index]=unsorted[index],unsorted[largest]
            heapify(unsorted,largest,heap_size)

    sort_(arr)
    return arr

############################################################################################################

#testing
for i in range(1):
    rand_array_len=random.randint(1,500)
    rand_array=random.sample(range(1,rand_array_len+1),rand_array_len)

    arr_bubble=sort_bubble(rand_array)
    arr_selection=sort_selection(rand_array)
    arr_insertion=sort_insertion(rand_array)
    arr_quick=sort_quick(rand_array)
    arr_merge=sort_merge(rand_array)
    arr_heap=sort_heap(rand_array)

    if not(arr_bubble==sorted(rand_array)):
        print("FALSE -> bubble")
    elif not(arr_selection==sorted(rand_array)):
        print("FALSE -> selection")
    elif not(arr_insertion==sorted(rand_array)):
        print("FALSE -> insertion")
    elif not(arr_quick==sorted(rand_array)):
        print("FALSE -> quick")
    elif not(arr_merge==sorted(rand_array)):
        print("FALSE -> merge")
    elif not(arr_heap==sorted(rand_array)):
        print("FALSE -> heap")
    else:
        print("TRUE",i)

############################################################################################################

#global variables
size=150
speed=0

fast_forward=0

#visualizer
class visualizer():
    def __init__(self,master):
        #top ui
        self.top_ui_frame=Frame(root)
        self.top_ui_frame.grid(row=0)

        self.type=IntVar()
        self.type_random=Radiobutton(self.top_ui_frame,font=("courier",10,"normal"),text="Random",variable=self.type,value=0)
        self.type_reversed=Radiobutton(self.top_ui_frame,font=("courier",10,"normal"),text="Reversed",variable=self.type,value=1)
        self.type_few=Radiobutton(self.top_ui_frame,font=("courier",10,"normal"),text="Few Unique",variable=self.type,value=2)
        self.type_nearly=Radiobutton(self.top_ui_frame,font=("courier",10,"normal"),text="Nearly Sorted",variable=self.type,value=3)

        self.type_random.grid(row=0,column=0,sticky=W)
        self.type_reversed.grid(row=1,column=0,sticky=W)
        self.type_few.grid(row=0,column=1,sticky=W)
        self.type_nearly.grid(row=1,column=1,sticky=W)

        self.shuffle_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Generate New Array",relief="ridge",command=self.generate_random_numbers)
        self.shuffle_btn.grid(row=2,columnspan=2,sticky=E+W)

        self.size_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Size")
        self.size_label.grid(row=0,column=3,padx=(10,0),sticky=W)
        self.size_sdr=Scale(self.top_ui_frame,orient=HORIZONTAL,from_=50,to=250,showvalue=False,sliderlength=10,length=100,command=self.set_size)
        self.size_sdr.grid(row=0,column=4)

        self.speed_label=Label(self.top_ui_frame,font=("courier",10,"normal"),text="Speed")
        self.speed_label.grid(row=1,column=3,padx=(10,0),sticky=W)
        self.speed_sdr=Scale(self.top_ui_frame,orient=HORIZONTAL,from_=0,to=400,showvalue=False,sliderlength=10,length=100,command=self.set_speed)
        self.speed_sdr.grid(row=1,column=4)

        self.FF_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Fast Forward",relief="ridge",command=self.FF,state=DISABLED)
        self.FF_btn.grid(row=2,column=3,columnspan=2,padx=(10,0),sticky=E+W)

        self.bubble_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Bubble",relief="ridge",command=self.sort_bubble)
        self.bubble_btn.grid(row=0,column=5,padx=(10,0),sticky=E+W)
        self.selection_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Selection",relief="ridge",command=self.sort_selection)
        self.selection_btn.grid(row=1,column=5,padx=(10,0),sticky=E+W)
        self.insertion_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Insertion",relief="ridge",command=self.sort_insertion)
        self.insertion_btn.grid(row=2,column=5,padx=(10,0),sticky=E+W)
        self.quick_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Quick",relief="ridge",command=self.sort_quick)
        self.quick_btn.grid(row=0,column=6,sticky=E+W)
        self.merge_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Merge",relief="ridge",command=self.sort_merge)
        self.merge_btn.grid(row=1,column=6,sticky=E+W)
        self.heap_btn=Button(self.top_ui_frame,font=("courier",10,"normal"),text="Heap",relief="ridge",command=self.sort_heap)
        self.heap_btn.grid(row=2,column=6,sticky=E+W)

        #the canvas
        self.canvas_frame=Frame(root)
        self.canvas_frame.grid(row=1)
        self.canvas=Canvas(self.canvas_frame,relief="solid",width=530,height=260,bg="black")
        self.canvas.pack()

        #start
        self.size_sdr.set(size)

    #Fast forward
    def FF(self):
        global fast_forward
        fast_forward=1

    #set size
    def set_size(self,val):
        global size
        size=int(val)
        self.generate_random_numbers()

    #set speed
    def set_speed(self,val):
        global speed
        speed=(500-int(val))/10000.0

    #generate random numbers and bars
    def generate_random_numbers(self):
        if(self.type.get()==0): #random
            self.rand_array_len=size
            self.rand_array=random.sample(range(1,self.rand_array_len+1),self.rand_array_len)
            self.sorted_array=sorted(self.rand_array)
        elif(self.type.get()==1): #reversed
            self.rand_array_len=size
            self.rand_array=[]
            for i in range(size):
                self.rand_array.append(size-i)
            self.sorted_array=sorted(self.rand_array)
        elif(self.type.get()==2): #few unique
            self.rand_array_len=size
            self.rand_array=[]
            for i in range(size):
                if(i+1<=(size//4)*1):
                    self.rand_array.append((size//4)*1)
                elif(i+1<=(size//4)*2):
                    self.rand_array.append((size//4)*2)
                elif(i+1<=(size//4)*3):
                    self.rand_array.append((size//4)*3)
                else:
                    self.rand_array.append((size//4)*4)
            self.rand_array=random.sample(self.rand_array,self.rand_array_len)
            self.sorted_array=sorted(self.rand_array)
        elif(self.type.get()==3): #nearly sorted
            self.rand_array_len=size
            self.rand_array=[]
            for i in range(size):
                self.rand_array.append(i+1)
            for i in range(1,size-1):
                if(random.randint(0,9)==0):
                    try:
                        if(random.randint(0,1)==0):
                            self.rand_array[i-1],self.rand_array[i],self.rand_array[i+1]=self.rand_array[i],self.rand_array[i+1],self.rand_array[i-1]
                        else:
                            self.rand_array[i-1],self.rand_array[i],self.rand_array[i+1]=self.rand_array[i+1],self.rand_array[i-1],self.rand_array[i]
                    except:
                        pass
            self.sorted_array=sorted(self.rand_array)

        self.bars=[]
        self.canvas.delete("all")

        w=514/size
        os=float(514-w*size)/2.0
        for i in range(len(self.rand_array)):
            self.bars.append(self.canvas.create_line(11+os+i*w,258,11+os+i*w,258-(1+float(self.rand_array[i]-1)/float(self.rand_array_len)*250.0),width=w,fill="white"))

    #bubble sort
    def sort_bubble(self):
        global fast_forward

        #enable disable buttons
        self.size_sdr.config(state=DISABLED)
        self.shuffle_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.bubble_btn.config(state=DISABLED)
        self.selection_btn.config(state=DISABLED)
        self.insertion_btn.config(state=DISABLED)
        self.quick_btn.config(state=DISABLED)
        self.merge_btn.config(state=DISABLED)
        self.heap_btn.config(state=DISABLED)

        for i in range(len(self.rand_array)-1):
            for j in reversed(range(1,len(self.rand_array))):
                #visualization(color)
                self.canvas.itemconfig(self.bars[j-1],fill="red")
                self.canvas.itemconfig(self.bars[j],fill="red")

                if(self.rand_array[j]<self.rand_array[j-1]):
                    self.rand_array[j-1],self.rand_array[j]=self.rand_array[j],self.rand_array[j-1]

                    #visualization(movement)
                    t=self.canvas.coords(self.bars[j-1])
                    self.canvas.coords(self.bars[j-1],self.canvas.coords(self.bars[j-1])[0],self.canvas.coords(self.bars[j-1])[1],self.canvas.coords(self.bars[j-1])[2],self.canvas.coords(self.bars[j])[3])
                    self.canvas.coords(self.bars[j],self.canvas.coords(self.bars[j])[0],self.canvas.coords(self.bars[j])[1],self.canvas.coords(self.bars[j])[2],t[3])

                    if not fast_forward:
                        time.sleep(speed)
                    root.update()

                #visualization(color)
                self.canvas.itemconfig(self.bars[j-1],fill="white")
                self.canvas.itemconfig(self.bars[j],fill="white")

                #check for completion
                if(self.rand_array==self.sorted_array):
                    root.update()
                    break

            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                break

        #visualization(color-completion)
        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="green")
            root.update()

        time.sleep(.1)

        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="white")
            root.update()

        #enable disable buttons
        self.size_sdr.config(state=NORMAL)
        self.shuffle_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.bubble_btn.config(state=NORMAL)
        self.selection_btn.config(state=NORMAL)
        self.insertion_btn.config(state=NORMAL)
        self.quick_btn.config(state=NORMAL)
        self.merge_btn.config(state=NORMAL)
        self.heap_btn.config(state=NORMAL)

        fast_forward=0

    #selection sort
    def sort_selection(self):
        global fast_forward

        #enable disable buttons
        self.size_sdr.config(state=DISABLED)
        self.shuffle_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.bubble_btn.config(state=DISABLED)
        self.selection_btn.config(state=DISABLED)
        self.insertion_btn.config(state=DISABLED)
        self.quick_btn.config(state=DISABLED)
        self.merge_btn.config(state=DISABLED)
        self.heap_btn.config(state=DISABLED)

        for i in range(len(self.rand_array)-1):
            t_min_idx=i

            #visualization(color)
            self.canvas.itemconfig(self.bars[t_min_idx],fill="red")

            for j in range(i+1,len(self.rand_array)):
                if(self.rand_array[j]<=self.rand_array[t_min_idx]):
                    #visualization(color)
                    self.canvas.itemconfig(self.bars[t_min_idx],fill="white")

                    t_min_idx=j

                    #visualization(color)
                    self.canvas.itemconfig(self.bars[t_min_idx],fill="red")

            self.rand_array[i],self.rand_array[t_min_idx]=self.rand_array[t_min_idx],self.rand_array[i]

            #visualization(color)
            self.canvas.itemconfig(self.bars[i],fill="red")

            #visualization(movement)
            t=self.canvas.coords(self.bars[i])
            self.canvas.coords(self.bars[i],self.canvas.coords(self.bars[i])[0],self.canvas.coords(self.bars[i])[1],self.canvas.coords(self.bars[i])[2],self.canvas.coords(self.bars[t_min_idx])[3])
            self.canvas.coords(self.bars[t_min_idx],self.canvas.coords(self.bars[t_min_idx])[0],self.canvas.coords(self.bars[t_min_idx])[1],self.canvas.coords(self.bars[t_min_idx])[2],t[3])

            if not fast_forward:
                time.sleep(speed)
            root.update()

            #visualization(color)
            self.canvas.itemconfig(self.bars[i],fill="white")
            for k in range(i,len(self.rand_array)):
                self.canvas.itemconfig(self.bars[k],fill="white")

            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                break

        #visualization(color-completion)
        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="green")
            root.update()

        time.sleep(.1)

        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="white")
            root.update()

        #enable disable buttons
        self.size_sdr.config(state=NORMAL)
        self.shuffle_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.bubble_btn.config(state=NORMAL)
        self.selection_btn.config(state=NORMAL)
        self.insertion_btn.config(state=NORMAL)
        self.quick_btn.config(state=NORMAL)
        self.merge_btn.config(state=NORMAL)
        self.heap_btn.config(state=NORMAL)

        fast_forward=0

    #insertion sort
    def sort_insertion(self):
        global fast_forward

        #enable disable buttons
        self.size_sdr.config(state=DISABLED)
        self.shuffle_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.bubble_btn.config(state=DISABLED)
        self.selection_btn.config(state=DISABLED)
        self.insertion_btn.config(state=DISABLED)
        self.quick_btn.config(state=DISABLED)
        self.merge_btn.config(state=DISABLED)
        self.heap_btn.config(state=DISABLED)

        sorted_idx=0
        for i in range(1,len(self.rand_array)):
            for j in range(sorted_idx+1):
                if(j==0):
                    if(self.rand_array[i]<=self.rand_array[j]):
                        #visualization(color)
                        self.canvas.itemconfig(self.bars[i],fill="red")
                        self.canvas.itemconfig(self.bars[j],fill="red")
                        root.update()
                        self.canvas.itemconfig(self.bars[i],fill="white")

                        t=self.rand_array.pop(i)
                        self.rand_array.insert(0,t)

                        #visualization(movement)
                        t=self.canvas.coords(self.bars[i])
                        for k in reversed(range(1,i+1)):
                            self.canvas.coords(self.bars[k],self.canvas.coords(self.bars[k])[0],self.canvas.coords(self.bars[k])[1],self.canvas.coords(self.bars[k])[2],self.canvas.coords(self.bars[k-1])[3])
                        self.canvas.coords(self.bars[0],self.canvas.coords(self.bars[0])[0],self.canvas.coords(self.bars[0])[1],self.canvas.coords(self.bars[0])[2],t[3])

                        if not fast_forward:
                            time.sleep(speed)
                        root.update()

                        break
                elif(self.rand_array[i]>=self.rand_array[j-1] and self.rand_array[i]<=self.rand_array[j]):
                    #visualization(color)
                    self.canvas.itemconfig(self.bars[i],fill="red")
                    self.canvas.itemconfig(self.bars[j],fill="red")
                    root.update()
                    self.canvas.itemconfig(self.bars[i],fill="white")

                    t=self.rand_array.pop(i)
                    self.rand_array.insert(j,t)

                    #visualization(movement)
                    t=self.canvas.coords(self.bars[i])
                    for k in reversed(range(j+1,i+1)):
                        self.canvas.coords(self.bars[k],self.canvas.coords(self.bars[k])[0],self.canvas.coords(self.bars[k])[1],self.canvas.coords(self.bars[k])[2],self.canvas.coords(self.bars[k-1])[3])
                    self.canvas.coords(self.bars[j],self.canvas.coords(self.bars[j])[0],self.canvas.coords(self.bars[j])[1],self.canvas.coords(self.bars[j])[2],t[3])

                    if not fast_forward:
                        time.sleep(speed)
                    root.update()

                    break

            sorted_idx+=1

            #visualization(color)
            for l in range(0,sorted_idx):
                self.canvas.itemconfig(self.bars[l],fill="white")

            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                break

        #visualization(color-completion)
        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="green")
            root.update()

        time.sleep(.1)

        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="white")
            root.update()

        #enable disable buttons
        self.size_sdr.config(state=NORMAL)
        self.shuffle_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.bubble_btn.config(state=NORMAL)
        self.selection_btn.config(state=NORMAL)
        self.insertion_btn.config(state=NORMAL)
        self.quick_btn.config(state=NORMAL)
        self.merge_btn.config(state=NORMAL)
        self.heap_btn.config(state=NORMAL)

        fast_forward=0

    #quick sort
    def sort_quick(self):
        global fast_forward

        #enable disable buttons
        self.size_sdr.config(state=DISABLED)
        self.shuffle_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.bubble_btn.config(state=DISABLED)
        self.selection_btn.config(state=DISABLED)
        self.insertion_btn.config(state=DISABLED)
        self.quick_btn.config(state=DISABLED)
        self.merge_btn.config(state=DISABLED)
        self.heap_btn.config(state=DISABLED)

        def sort(low,high):
            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                return None

            if(high<=low):
                return None

            mid=partition(low,high)
            sort(low,mid-1)
            sort(mid,high)

        def partition(low,high):
            global fast_forward

            pivot=self.rand_array[(low+high)//2]
            while(low<=high):
                while(self.rand_array[low]<pivot):
                    low+=1
                while(self.rand_array[high]>pivot):
                    high-=1
                if(low<=high):
                    self.rand_array[low],self.rand_array[high]=self.rand_array[high],self.rand_array[low]

                    #visualization(color)
                    self.canvas.itemconfig(self.bars[low],fill="red")
                    self.canvas.itemconfig(self.bars[high],fill="red")
                    root.update()

                    #visualization(movement)
                    t=self.canvas.coords(self.bars[low])
                    self.canvas.coords(self.bars[low],self.canvas.coords(self.bars[low])[0],self.canvas.coords(self.bars[low])[1],self.canvas.coords(self.bars[low])[2],self.canvas.coords(self.bars[high])[3])
                    self.canvas.coords(self.bars[high],self.canvas.coords(self.bars[high])[0],self.canvas.coords(self.bars[high])[1],self.canvas.coords(self.bars[high])[2],t[3])

                    if not fast_forward:
                        time.sleep(speed)
                    root.update()

                    #visualization(color)
                    self.canvas.itemconfig(self.bars[low],fill="white")
                    self.canvas.itemconfig(self.bars[high],fill="white")

                    low,high=low+1,high-1

            return low

        sort(0,len(self.rand_array)-1)

        #visualization(color-completion)
        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="green")
            root.update()

        time.sleep(.1)

        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="white")
            root.update()

        #enable disable buttons
        self.size_sdr.config(state=NORMAL)
        self.shuffle_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.bubble_btn.config(state=NORMAL)
        self.selection_btn.config(state=NORMAL)
        self.insertion_btn.config(state=NORMAL)
        self.quick_btn.config(state=NORMAL)
        self.merge_btn.config(state=NORMAL)
        self.heap_btn.config(state=NORMAL)

        fast_forward=0

    #merge sort
    def sort_merge(self):
        global fast_forward

        #enable disable buttons
        self.size_sdr.config(state=DISABLED)
        self.shuffle_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.bubble_btn.config(state=DISABLED)
        self.selection_btn.config(state=DISABLED)
        self.insertion_btn.config(state=DISABLED)
        self.quick_btn.config(state=DISABLED)
        self.merge_btn.config(state=DISABLED)
        self.heap_btn.config(state=DISABLED)

        def rMergeSort(A,l,r):
            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                return None

            if(l<r):
                m=(l+r)//2
                rMergeSort(A,l,m)
                rMergeSort(A,m+1,r)
                merge(A,l,m,r)

            return None

        def merge(A,l,m,r):
            global fast_forward

            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                return None

            B=[None]*len(self.rand_array)
            i,k,j=l,l,m+1

            #create backup length data(for visualization)
            length_b=[None]*len(self.rand_array)
            for t in range(l,r+1):
                length_b[t]=self.canvas.coords(self.bars[t])[3]

            while(i<=m and j<=r):
                #visualization(color)
                self.canvas.itemconfig(self.bars[i],fill="red")
                self.canvas.itemconfig(self.bars[j],fill="red")
                root.update()

                if(A[i]<=A[j]):
                    B[k]=A[i]

                    #visualization(movement)
                    self.canvas.coords(self.bars[k],self.canvas.coords(self.bars[k])[0],self.canvas.coords(self.bars[k])[1],self.canvas.coords(self.bars[k])[2],length_b[i])

                    if not fast_forward:
                        time.sleep(speed)
                    root.update()

                    #visualization(color)
                    self.canvas.itemconfig(self.bars[i],fill="white")
                    self.canvas.itemconfig(self.bars[j],fill="white")

                    k+=1
                    i+=1
                else:
                    B[k]=A[j]

                    #visualization(movement)
                    self.canvas.coords(self.bars[k],self.canvas.coords(self.bars[k])[0],self.canvas.coords(self.bars[k])[1],self.canvas.coords(self.bars[k])[2],length_b[j])

                    if not fast_forward:
                        time.sleep(speed)
                    root.update()

                    #visualization(color)
                    self.canvas.itemconfig(self.bars[i],fill="white")
                    self.canvas.itemconfig(self.bars[j],fill="white")

                    k+=1
                    j+=1

            while(i<=m):
                #visualization(color)
                self.canvas.itemconfig(self.bars[i],fill="red")
                root.update()

                B[k]=A[i]

                #visualization(movement)
                self.canvas.coords(self.bars[k],self.canvas.coords(self.bars[k])[0],self.canvas.coords(self.bars[k])[1],self.canvas.coords(self.bars[k])[2],length_b[i])

                if not fast_forward:
                    time.sleep(speed)
                root.update()

                #visualization(color)
                self.canvas.itemconfig(self.bars[i],fill="white")

                k+=1
                i+=1

            while(j<=r):
                #visualization(color)
                self.canvas.itemconfig(self.bars[j],fill="red")
                root.update()

                B[k]=A[j]

                #visualization(movement)
                self.canvas.coords(self.bars[k],self.canvas.coords(self.bars[k])[0],self.canvas.coords(self.bars[k])[1],self.canvas.coords(self.bars[k])[2],length_b[j])

                if not fast_forward:
                    time.sleep(speed)
                root.update()

                #visualization(color)
                self.canvas.itemconfig(self.bars[j],fill="white")

                k+=1
                j+=1

            for k in range(l,r+1):
                A[k]=B[k]

            return None

        rMergeSort(self.rand_array,0,len(self.rand_array)-1)

        #visualization(color-completion)
        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="green")
            root.update()

        time.sleep(.1)

        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="white")
            root.update()

        #enable disable buttons
        self.size_sdr.config(state=NORMAL)
        self.shuffle_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.bubble_btn.config(state=NORMAL)
        self.selection_btn.config(state=NORMAL)
        self.insertion_btn.config(state=NORMAL)
        self.quick_btn.config(state=NORMAL)
        self.merge_btn.config(state=NORMAL)
        self.heap_btn.config(state=NORMAL)

        fast_forward=0

    #heap sort
    def sort_heap(self):
        global fast_forward

        #enable disable buttons
        self.size_sdr.config(state=DISABLED)
        self.shuffle_btn.config(state=DISABLED)
        self.FF_btn.config(state=NORMAL)

        self.bubble_btn.config(state=DISABLED)
        self.selection_btn.config(state=DISABLED)
        self.insertion_btn.config(state=DISABLED)
        self.quick_btn.config(state=DISABLED)
        self.merge_btn.config(state=DISABLED)
        self.heap_btn.config(state=DISABLED)

        def sort_(unsorted):
            #check for completion
            if(self.rand_array==self.sorted_array):
                root.update()
                return None

            n=len(unsorted)

            for i in reversed(range(0,n//2)):
                heapify(unsorted,i,n)

            for i in reversed(range(1,n)):
                #visualization(color)
                self.canvas.itemconfig(self.bars[0],fill="red")
                try:
                    self.canvas.itemconfig(self.bars[i+1],fill="white")
                except:
                    pass
                root.update()

                unsorted[0],unsorted[i]=unsorted[i],unsorted[0]

                #visualization(movement)
                t=self.canvas.coords(self.bars[0])
                self.canvas.coords(self.bars[0],self.canvas.coords(self.bars[0])[0],self.canvas.coords(self.bars[0])[1],self.canvas.coords(self.bars[0])[2],self.canvas.coords(self.bars[i])[3])
                self.canvas.coords(self.bars[i],self.canvas.coords(self.bars[i])[0],self.canvas.coords(self.bars[i])[1],self.canvas.coords(self.bars[i])[2],t[3])

                #visualization(color)
                self.canvas.itemconfig(self.bars[i],fill="red")
                root.update()

                if not fast_forward:
                    time.sleep(speed)
                root.update()

                heapify(unsorted,0,i)

        def heapify(unsorted,index,heap_size):
            largest=index

            left_index=2*index+1
            right_index=2*index+2

            if(left_index<heap_size and (unsorted[left_index]>unsorted[largest])):
                largest=left_index
            if(right_index<heap_size and (unsorted[right_index]>unsorted[largest])):
                largest=right_index
            if(largest!=index):
                unsorted[largest],unsorted[index]=unsorted[index],unsorted[largest]

                #visualization(color)
                self.canvas.itemconfig(self.bars[largest],fill="red")
                self.canvas.itemconfig(self.bars[index],fill="red")
                root.update()

                #visualization(movement)
                t=self.canvas.coords(self.bars[largest])
                self.canvas.coords(self.bars[largest],self.canvas.coords(self.bars[largest])[0],self.canvas.coords(self.bars[largest])[1],self.canvas.coords(self.bars[largest])[2],self.canvas.coords(self.bars[index])[3])
                self.canvas.coords(self.bars[index],self.canvas.coords(self.bars[index])[0],self.canvas.coords(self.bars[index])[1],self.canvas.coords(self.bars[index])[2],t[3])

                if not fast_forward:
                    time.sleep(speed)
                root.update()

                #visualization(color)
                self.canvas.itemconfig(self.bars[largest],fill="white")
                self.canvas.itemconfig(self.bars[index],fill="white")

                heapify(unsorted,largest,heap_size)

        sort_(self.rand_array)

        #visualization(color-completion)
        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="green")
            root.update()

        time.sleep(.1)

        for i in range(len(self.rand_array)):
            self.canvas.itemconfig(self.bars[i],fill="white")
            root.update()

        #enable disable buttons
        self.size_sdr.config(state=NORMAL)
        self.shuffle_btn.config(state=NORMAL)
        self.FF_btn.config(state=DISABLED)

        self.bubble_btn.config(state=NORMAL)
        self.selection_btn.config(state=NORMAL)
        self.insertion_btn.config(state=NORMAL)
        self.quick_btn.config(state=NORMAL)
        self.merge_btn.config(state=NORMAL)
        self.heap_btn.config(state=NORMAL)

        fast_forward=0

############################################################################################################

root=None

def start():
    global size,speed
    global fast_forward

    #RESET GLOBAL VARIABLES
    size=150
    speed=0

    fast_forward=0

    #START
    global root
    root=Tk()
    root.focus_force()
    root.title("Sorting Visualizer")
    root.resizable(0,0)
    vis=visualizer(root)
    root.mainloop()

if __name__ == '__main__':
    start()
