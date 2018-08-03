import json
from PIL import Image
# import numpy as np
import matplotlib.pyplot as plt
# from PIL import ImageTk, Image
import SimpleITK as sitk
import ctypes
import matplotlib
import operator
# Anything that's commented out doesn't work or wasn't necessary, that's for future reference or something like that

# Setup for data and stuff below this
imgPath = "Images/test.nii"
img = sitk.ReadImage(imgPath)
IMG = sitk.GetArrayFromImage(img)
imgHeight = int(len(IMG[1,1,:]))
imgWidth = int(len(IMG[1,:,1]))
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
winwidth = 1920 # user32.GetSystemMetrics(0)
winheight = 1080 # user32.GetSystemMetrics(1)

sn = 0 # Slice Number, for use in slices()
tpn = 0 # Total number of points, for use in slices()
xcoord = []
ycoord = []
xextra = [] # These two aren't neccesary for the GUI or visualizations
yextra = [] # I'm still keeping them for fun though
subxcoord = []
subycoord = []
xleft = 0
xright = 0
ybottom = 0
ytop = 0 
# xmin = 0
# xmax = 0
# ymin = 0
# ymax = 0


def point_cutoffs():

    global xleft, xright, ybottom, ytop # xmin, xmax, ymin, ymax

    xleft = winwidth/2 - imgWidth/2
    xright = winwidth/2 + imgWidth/2
    ytop = 0
    ybottom = imgHeight

    # print(xleft)
    # print(xright)
    # print(ytop)
    # print(ybottom)
    print("Cutoffs Adjusted")


def data_processing():

    global xcoord, ycoord, xextra, yextra  # xmin, xmax, ymin, ymax, xstr, ystr, xexstr, yexstr 

    with open('eyetrackingdata.json', 'r') as f:
        j = json.loads(f.read())  
        for i in range(len(j)):
            access = j["num" + str(i)]
            
            w = access["X"]  # These two are w and h instead of x and y to avoid confusion with some other stuff in gui.py
            h = access["y"]  
        
            if (w <= xright and w >= xleft and h >= ytop and h <= ybottom):

                xcoord.append(w)
                ycoord.append(h)
                # print(w, h)

            else:

                xextra.append(w)
                yextra.append(h)
                    
    # xmin = min(xcoord)
    # xmax = max(xcoord)
    # ymin = min(ycoord)
    # ymax = max(ycoord)

    # print(imgHeight)
    # print(imgWidth)
    print('Data Processing Complete')


lsall = []

def slices(): 
    # This part is annoying, doesn't work properly, and isn't in the GUI, it's meant to display a heatmap of points on each slice
    # I'm writing this on the last day of the program so I don't think I'll have time to fix this
    # Considering how this is extremely annoying, slow, and not exactly essential just skip it for now
    # I'm not sure the way I'm doing it is the best way even if I did get it to work, explore other options if you do decide to work on it

    global sn, tpn, subxcoord, subycoord

    with open('eyetrackingdata.json', 'r') as f:
        j = json.loads(f.read())  
        for i in range(len(j)):
            access = j["num" + str(i)]

            w = access['X']
            h = access['y']
            n = access['num']

            lsall.append(n)
            lsall.append(w)
            lsall.append(h)

    print(lsall)
    tpn = len(lsall)/3
    print(tpn)
    forfun = tpn*3 - 3
    finalslice = operator.itemgetter(forfun)(lsall)
    sn = 0
    n1 = 0
    nx = 1
    ny = 2

    for i in range(0, tpn):        

        if sn == operator.itemgetter(n1)(lsall):
            
            w = operator.itemgetter(nx)(lsall)
            h = operator.itemgetter(ny)(lsall) 
            if (w <= xright and w >= xleft and h >= ytop and h <= ybottom):

                subxcoord.append(w)
                subycoord.append(h)
             
                try:
                    fig = plt.figure()
                    plt.hexbin([subxcoord], [subycoord], cmap = None, mincnt = 1, gridsize = 60)
                    plt.axis([xleft, xright, ytop, ybottom])
                    plt.axis('off')
                    plt.gca().invert_yaxis()
                    sns = str(sn)
                    fig.savefig('SliceHeatmaps/' + sns + '.png', transparent = True)
                    plt.clf()
                    plt.close(fig)
                except:
                    pass

            n1 += 3
            nx += 3
            ny += 3
            print('Figure ' + sns + ' Saved')

        else:
            sn += 1
            subxcoord = []
            subycoord = []

    print(sn)
    print(finalslice)
    print(n1, nx, ny)


def firstplot():
    
    fig = plt.figure()
    plt.hexbin([xcoord],[ycoord], cmap = None, mincnt = 1, gridsize = 40)
    plt.axis([xleft, xright, ytop, ybottom])
    plt.axis('off')
    # plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    # cb = plt.colorbar()
    # cb.set_label('Frequency')
    fig.savefig('temp.png', transparent = True)
    # plt.show()


def extrapoints():

    plt.hexbin([xextra], [yextra], cmap = None, mincnt = 1)
    # plt.axis([0, winwidth, 0, winheight])
    plt.axis('on')
    plt.gca().invert_yaxis()
    plt.title("Extra Data Points Not on Scan")
    cb = plt.colorbar()
    cb.set_label('Frequency')
    
    # plt.show()

# heatmap, xedges, yedges = np.histogram2d(x, y, bins=512)
# extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
# #plt.clf()
# plt.imshow(heatmap, extent=extent, origin = 'lower')
# plt.show()
