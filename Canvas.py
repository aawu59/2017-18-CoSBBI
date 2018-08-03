from Tkinter import *
import json
import random

root= Tk()
root.protocol("WM_DELETE_WINDOW", root.quit())
canvas=Canvas(root,width=1920,height=1080)
canvas.pack()

with open('guiandtracking2/eyetrackingdata.json', 'r') as f:
    j = json.loads(f.read())
    num = 0
    r = lambda: random.randint(0,255)
    color = '#000000'
    for i in range(len(j)):
        access = j["num" + str(i)]
        if access['num'] != num: 
            color = '#%02X%02X%02X' % (r(),r(),r())
            canvas.create_oval(access['X'], access['y'], access['X'] + 10, access['y'] + 10, fill=color)
            num = access['num']
        else:
            canvas.create_oval(access['X'], access['y'], access['X'] + 10, access['y'] + 10, fill=color)
            num = access['num']

root.state('zoomed')
root.mainloop()

