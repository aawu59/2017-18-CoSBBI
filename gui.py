#IMPORT EVERYTHING
from Tkinter import *
from PIL import ImageTk, Image
import SimpleITK as sitk
import numpy as np
import scipy.misc
import gazestuffold
import DataAnalysis
import threading
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import ctypes
from skimage import data, color
from skimage.transform import resize
import json
#import main as mn
#import main
#import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)

# This can adapt to window resolution but scaling of the scan itself doesn't work yet
# If you have a 4K screen the scan will be tiny and it will break a few other features so set your resolution to 1920x1080

#DEFINE GLOBALS
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
winwidth = user32.GetSystemMetrics(0)
winheight = user32.GetSystemMetrics(1)
imgPath = "Images/test.nii"
# switch = False
scanstate = 0
forgCoordinates = [] #HOLDS ALL FOREGROUND COORDINATES, [X,Y,Z]
backCoordinates = [] #HOLDS ALL BACKGROUND COORDINATES, [X,Y,Z]
tempCoordinates = [[50,50]]
slice = 0
t = 0
refTime = 0
totalTime = 0
c = 0
x = 0
xcoord = []
ycoord = []
#DEFINE THREADING

# class myThread(threading.Thread):
#     def __init__(self, threadID, name):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#     def run(self):
#         while running == 0:
#             gazestuffold.start_eye_stream()


randomvar = 0

class eyeTracking(Tk):

#     #DEFINE MAIN FUNCTION
#     # def __init__(self):
#     #     pass


    def __init__(self, master):

        global slice, imgHeight, imgWidth, imgPath, running, randomvar, t, refTime, c, x

        randomvar = 1
        # root = Tk()
        # root.update()
        # root.geometry("512x580")
        # root.title('Tkinter Widgets')
        # root.minsize(root.winfo_width(), root.winfo_height())

        #CREATE MASTER FRAME
        # frame = Frame(master, width=1000, height=512, bd=1)
        # frame.pack(fill=NONE, expand=0)

        self.frame = Frame(master, width=512, height=512, bd=1, relief=RAISED)
        self.frame2 = Frame(master, bd=10, relief=RAISED)
        backButton = Button(self.frame2, text = "Menu", command= lambda : Menu2())
        #stopTrackingButton = Button(self.frame2, text = "Stop", command= lambda: lambdaCall())

        c = Canvas(self.frame, bg='white', width=1, height=1)

        #READ 3D IMAGE
        img = sitk.ReadImage(imgPath)

        #TRANSLATE TO ARRAY
        IMG = sitk.GetArrayFromImage(img)
        yourImg = IMG[slice,:,:]  #USE GLOBAL SLICE SO WE CAN CHANGE IT WITH SLIDER
        print ('slice number is: ', slice)

        #CHANGE FROM ARRAY TO INITIAL IMAGE
        reConstruct = ImageTk.PhotoImage(scipy.misc.toimage(yourImg))  # use scipy.toimage instead of Image.fromarray
        root.reConstruct = reConstruct #CLEAN GARBAGE
        imgHeight = int(len(IMG[1,1,:]))
        imgWidth = int(len(IMG[1,:,1]))
        c.configure(width=imgWidth, height=imgHeight) #CHANGE CANVAS TO SIZE OF IMAGE

        #DRAW IMAGE
        x = c.create_image(0, 0, image=reConstruct, anchor="nw")

        #CREATE SUBFRAME FOR CANVAS
        self.frame.pack(fill=NONE, expand=0, pady=0, padx=1)
        self.frame2.pack(fill=NONE, expand=0, pady=0, padx=5, side=TOP)
        c.pack(fill=BOTH, expand=1)

        #CALLBACK FUNCTION FOR SLIDER - REDRAWS THE IMAGE AT THE VALUE OF GLOBAL SLICE
        def changeSlice(self):
            global slice
            slice = slider.get()
            yourImg = IMG[slice, :, :]
            reConstruct = ImageTk.PhotoImage(scipy.misc.toimage(yourImg))
            root.reConstruct = reConstruct
            c.create_image(0, 0, image=reConstruct, anchor="nw")
            c.pack(fill=BOTH, expand=1)
            # print ('slice number is: ', slice)

        #SLIDER
        slider = Scale(self.frame2, from_=0, to_=len(IMG[:,1,1])-1, orient=HORIZONTAL, command=changeSlice)
        slider.pack()

        backButton.pack()

        t = threading.Thread(target=gazestuffold.start_eye_stream)
        t.start()
        # if currentX > 400:
        #     print("greater")
        # refTime = time.time()
        #stopTrackingButton.pack()
        # eyeTrackingThread = myThread(1, "Tracking")
        # eyeTrackingThread.start()

        #THESE LOGIC BLOCKS SMOOTH OUT THE DRAWING
#         def drawingLogic1(thing):
#             if switch:
#                 if (forgCoordinates[-1][0] - tempCoordinates[0][0] > 1 or forgCoordinates[-1][1] - tempCoordinates[0][
#                     1] > 1):
#                     c.create_line(thing.x, thing.y, forgCoordinates[-1][0], forgCoordinates[-1][1], fill="red")

#         def drawingLogic2(thing):
#             if switch:
#                 if (backCoordinates[-2][0] - tempCoordinates[0][0] > 1 or backCoordinates[-2][1] - tempCoordinates[0][
#                     1] > 1):
#                     c.create_line(thing.x, thing.y, backCoordinates[-2][0], backCoordinates[-2][1], fill="blue")

#         #FOREGROUND - DRAW A 1PX LINE WHERE MOUSE IS
#         def mouse1Motion(event):
#             global switch , slice
#             tempCoordinates = [] #CLEAR TEMPORARY COORDINATES
#             tempCoordinates.append([event.x, event.y])
#             drawingLogic1(event)
#             forgCoordinates.append([event.x, event.y, slice]) #APPENDS TO FOREGROUND ARRAY
#             c.create_line(event.x, event.y, event.x + 1, event.y + 1, fill="red", smooth=TRUE) #ACTUALLY DRAWING
#             switch = True #BOOLEAN LOGIC TO STOP FROM DRAWING LINES AFTER EVERY MOUSE UP/DOWN
# #            print ("for" + str(forgCoordinates)) #VISUALIZE

#         #BACKGROUND - DRAW A 1PX LINE WHERE MOUSE IS
#         def mouse2Motion(event):
#             global switch , slice
#             backCoordinates.append([event.x, event.y, slice]) #APPENDS TO BACKGROUND ARRAY
#             tempCoordinates = []
#             tempCoordinates.append([event.x, event.y,])
#             drawingLogic2(event)
#             c.create_line(event.x, event.y, event.x + 1, event.y + 1, fill="blue")
#             switch = True
# #           print ("back" + str(backCoordinates))

#         #TO STOP FROM ALWAYS DRAWING LINE
#         def mouseRelease(event):
#             global switch
#             switch = False

#         def mouseRelease2(event):
#             global switch
#             switch = False

#         # WHEN YOU HIT THE BUTTON, THE COORDINATES ARE RETURNED IN DICTIONARY FORM TO THIS FUNCTION
#         def returnCoordinates():
#             global imgPath
#             dictPoints = {
#                 "Foreground": forgCoordinates,
#                 "Background": backCoordinates
#             }
# #            print ("Foreground: " + str(dictPoints["Foreground"]))
# #            print ("Background: " + str(dictPoints["Background"]))
#             slice = 90
#             #mn.start(imgPath , slice ,dictPoints)
#             return dictPoints

#         #BUTTON
#         returnCoordinatesButton = Button(frame3, text="Return Coordinates", command=returnCoordinates)
#         returnCoordinatesButton.pack(fill=None, expand=0)

#         # MOUSE BINDINGS
#         c.bind("<B1-Motion>", mouse1Motion)
#         c.bind("<B2-Motion>", mouse2Motion)  # for using in Mac it has to be B2-Motion
#     # c.bind("<B3-Motion>", mouse2Motion)  # for use in window it has to be B3-Motion
#         c.bind("<ButtonRelease-1>", mouseRelease)
#         c.bind("<ButtonRelease-3>", mouseRelease2)



#         root.mainloop()




class analysis(Tk):

    def __init__(self, master):

        global slice, imgHeight, imgWidth, imgPath, randomvar, c

        randomvar = 2
        DataAnalysis.point_cutoffs()
        DataAnalysis.data_processing()
        DataAnalysis.firstplot()
        from DataAnalysis import xleft, xright, ytop, ybottom
        # root = Tk()
        # root.update()
        # root.geometry("512x580")
        # root.title('Tkinter Widgets')
        # root.minsize(root.winfo_width(), root.winfo_height())

        #CREATE MASTER FRAME
        # frame = Frame(master, width=1000, height=512, bd=1)
        # frame.pack(fill=NONE, expand=0)
        self.frame = Frame(master, width=512, height=512, bd=1, relief=RAISED)
        self.frame2 = Frame(master, bd=10, relief=RAISED)
        backButton = Button(self.frame2, text = "Menu", command= lambda : Menu3())


        c = Canvas(self.frame, bg='white', width = 1, height = 1)

        #READ 3D IMAGE
        img = sitk.ReadImage(imgPath)
    
        #TRANSLATE TO ARRAY
        IMG = sitk.GetArrayFromImage(img)
        yourImg = IMG[slice,:,:]  #USE GLOBAL SLICE SO WE CAN CHANGE IT WITH SLIDER
        print ('slice number is: ', slice)

        #CHANGE FROM ARRAY TO INITIAL IMAGE
        reConstruct = ImageTk.PhotoImage(scipy.misc.toimage(yourImg))  # use scipy.toimage instead of Image.fromarray
        master.reConstruct = reConstruct #CLEAN GARBAGE
        imgHeight = int(len(IMG[1,1,:]))
        imgWidth = int(len(IMG[1,:,1]))
        c.configure(width=imgWidth, height=imgHeight) #CHANGE CANVAS TO SIZE OF IMAGE

        # GET HEATMAP FROM SAVED PNG 
        plot = Image.open('temp.png')
        photo = ImageTk.PhotoImage(plot)

        #DRAW IMAGES
        c.create_image(0, 0, image=reConstruct, anchor="nw")
        c.create_image(imgHeight/2,imgWidth/2, image=photo, anchor='center')

        #CREATE SUBFRAME FOR CANVAS
        self.frame.pack(fill=NONE, expand=0, pady=0, padx=1)
        self.frame2.pack(fill=NONE, expand=0, pady=0, padx=5, side=TOP)
        c.pack(fill=NONE, expand=0)
        c.pack_propagate(0)
        c.grid_rowconfigure(2, weight=1)
        c.columnconfigure(2, weight=1)
        #CALLBACK FUNCTION FOR SLIDER - REDRAWS THE IMAGE AT THE VALUE OF GLOBAL SLICE
        
        def changeSlice(self):
            global slice
            slice = slider.get()
            yourImg = IMG[slice, :, :]
            reConstruct = ImageTk.PhotoImage(scipy.misc.toimage(yourImg))
            root.reConstruct = reConstruct
            c.create_image(0, 0, image=reConstruct, anchor="nw")
            c.create_image(imgHeight/2,imgWidth/2, image=photo, anchor='center')
            c.pack(fill=BOTH, expand=1)
            c.grid_rowconfigure(2, weight=1)
            c.columnconfigure(2, weight=1)
            print ('slice number is: ', slice)

        #SLIDER
        slider = Scale(self.frame2, from_=0, to_=len(IMG[:,1,1])-1, orient=HORIZONTAL, command=changeSlice)
        slider.pack()

        backButton.pack()

    # def __init__(self, master):
    #     # Create a container
    #     frame = Frame(master)
    #     # Create 2 buttons
    #     # def changeSlice(self):
    #     #     global slice
    #     #     slice = slider.get()
    #     #     yourImg = IMG[slice, :, :]
    #     #     reConstruct = ImageTk.PhotoImage(scipy.misc.toimage(yourImg))
    #     #     root.reConstruct = reConstruct
    #     #     c.create_image(0, 0, image=reConstruct, anchor="nw")
    #     #     c.pack(fill=BOTH, expand=1)
    #     #     print ('slice number is: ', slice)

    #     # #SLIDER
    #     # slider = Scale(self.frame2, from_=0, to_=len(IMG[:,1,1])-1, orient=HORIZONTAL, command=changeSlice)
    #     # slider.pack()


    #     self.button_left = Button(frame,text="< Decrease Slope",
    #                                     command=self.decrease)
    #     self.button_left.pack(side="left")
    #     self.button_right = Button(frame,text="Increase Slope >",
    #                                     command=self.increase)
    #     self.button_right.pack(side="left")

    #     x = np.random.randn(8873)
    #     y = np.random.randn(8873)
    #     heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
    #     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    #     self.canvas = FigureCanvasTkAgg(heatmap,master=master)
    #     self.canvas.show()
    #     self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    #     frame.pack()

    # def decrease(self):
    #     x, y = self.line.get_data()
    #     self.line.set_ydata(y - 0.2 * x )
    #     self.canvas.draw()

    # def increase(self):
    #     x, y = self.line.get_data()
    #     self.line.set_ydata(y + 0.2 * x)
    #     self.canvas.draw()



root = Tk()
button1 = Button(root, text= "Eyetracking", activebackground = 'red', highlightcolor = 'red' , highlightthickness = 20,  width = 32, height = 32, command= lambda : Tracker())
button2 = Button(root, text= "Analytics", activebackground = 'blue', highlightcolor = 'red', highlightthickness = 20,  width = 32, height = 32, command= lambda : analytics())
instance1 = 0
instance2 = 0

def lambdaCall():
    global running
    running = 1

def Tracker():
    global button1, button2, root, instance1
    button1.pack_forget()
    button2.pack_forget()
    instance1 = eyeTracking(root)

 # top = Toplevel(root)
# top.title("Eyetracking or Analytics?")

def analytics():
    global button1, button2, root, instance2
    button1.pack_forget()
    button2.pack_forget()
    instance2 = analysis(root)

def Menu():
    global button1, button2
    button1.pack(side = LEFT, padx=winwidth/8)
    button2.pack(side = RIGHT, padx=winwidth/8)

def Menu2():
    global randomvar, instance1, instance2, t
    gazestuffold.t.stop_tracking()
    gazestuffold.t.disconnect()
    gazestuffold.t.break_event_loop()
    totalTime = time.time() - refTime
    #t.join()
    if randomvar == 1:
        instance1.frame.pack_forget()
        instance1.frame2.pack_forget()
    elif randomvar == 2:
        instance2.frame.pack_forget()
        instance2.frame2.pack_forget()
    Menu()

def Menu3():
    global randomvar, instance1, instance2
    if randomvar == 1:
        instance1.frame.pack_forget()
        instance1.frame2.pack_forget()
    elif randomvar == 2:
        instance2.frame.pack_forget()
        instance2.frame2.pack_forget()
    Menu()

def stopTracking():
    gazestuffold.threadTracking = False
    Menu2()
    # t.event_queue.task_done()
    # gazestuffold.stop_tracking()
    # t.disconnect()


root.state('zoomed')
root.minsize(winwidth,winheight)
root.maxsize(winwidth,winheight)
Menu()

root.mainloop()


#instance = startUp(root)
