from gazesdk import *
import time
import sys
import json
import random
import Tkinter as tk
import ctypes

# this stuff is finicky on high DPI, if it doesn't work manually change it down below to match your screen resolution
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

winwidth = user32.GetSystemMetrics(0)
winheight = user32.GetSystemMetrics(1)

listOfFixations = {}
timeout = time.time() + 10
nameCounter = 0
currentX = 0
currentY = 0
windowX = 0
windowY = 0
def start_eye_stream(pat_id='0'):
   
    global listOfFixations, t, out_file, nameCounter, currentX, currentY
   
    url = get_connected_eye_tracker()
    t = Tracker(url)
    t.run_event_loop()
    #out_file = open(local_dir + 'eye_stream/'+pat_id+'_'+str(time.time()) + '.txt','w+')
    t.connect()
    t.start_tracking()

    window = []
    xPrev = 0
    yPrev = 0
    fixNum = 0
    counter = 0
    threadTracking = True
    currentTime = time.time()

    # if threadTracking == False:
    #     stop_tracking()


    while threadTracking == True:
        try:
            data = t.event_queue.get()
            leftX = data.left.gaze_point_on_display_normalized[0]
            rightX = data.right.gaze_point_on_display_normalized[0]
            leftY = data.left.gaze_point_on_display_normalized[1]
            rightY = data.right.gaze_point_on_display_normalized[1]
            # if leftX !=0.0:
            #       if rightX:	x = (leftX+rightX)/2.0
            #       else:	x = leftX
            # else:	x = rightX

            # if leftY !=0.0:
            #       if rightY:	y = (leftY+rightY)/2.0
            #       else:	y = leftY

            currentX = ((leftX + rightX)/ 2) * winwidth
            currentY = ((leftY + rightY)/ 2) * winheight

            # coordinates = {}

            # coordinates["location"] = {
            #     'xCoordinate': currentX,
            #     'yCoordinate': currentY
            # }

            
            #Just remember that you are appending fixations as 
            
            # print(gui.c.coords(x))
            
            if ((currentX - xPrev)**(2) + (currentY - yPrev)**(2))**(.5) > 60:
                if windowX < currentX < windowX + 400:
                    if windowY < currentY < windowY + 400:    
                        if window:
                            for i in window:
                                listOfFixations["num" + str(nameCounter)] = {
                                    'X':  i[0],
                                    'y':  i[1],
                                    'num':  i[2]
                                }
                                nameCounter += 1
                            window = []
                            fixNum += 1
                            counter = 0
                        else:
                            pass 
                        xPrev = currentX
                        yPrev = currentY
            elif ((currentX - xPrev)**(2) + (currentY - yPrev)**(2))**(.5) < 60:
                window.append([currentX, currentY, fixNum])

            # if time.time() = currentTime:
            #     break

            #print(output)

            #file = open("eyetrackingdata.txt", "w")
            #file.write(str(computeX) + ',' + str(computeY) + ',' + str(time.time()))
            #readfile = open("eyetrackingdata.txt", 'r').read()
            #print(readfile)

                #out_file.write(str(x)+','+str(y)+','+str(curr_time)+'\n')
                #help.append[computeX, computeY, curr_time]
            #t.event_queue.task_done()



        except KeyboardInterrupt:
            try:
                with open("eyetrackingdata.json", "w") as f:
                    f.write(json.dumps(listOfFixations))
            except:
                pass
            
            print('\nEye Tracking Terminated')
            t.event_queue.task_done()
            t.stop_tracking()
            t.disconnect()
            sys.exit()

    t.event_queue.task_done()
    t.stop_tracking()
    t.disconnect()
    sys.exit()
                



# start_eye_stream()