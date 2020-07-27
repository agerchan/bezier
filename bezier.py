from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import random

'''
key masterlist

up/down arrow: speeds up/slows down program
right/left delete/restore points
space runs/pauses
return restarts run
delete deletes all
'''

def between(x1, y1, x2, y2, time):
    return [x1 + (time*(x2-x1)/100), y1 + (time*(y2-y1)/100)]


def getmids(points, time):
    if (len(points) == 1):
        return None
    else:
        res = []
        for i in range(len(points) - 1):
            res.append(between(points[i][0], points[i][1], points[i+1][0], points[i+1][1], time))
        return [res, getmids(res, time)]


def appStarted(app):
    app.coords = []
    app.deleted = []
    app.running = False
    app.done = False
    app.secondcoords = []
    app.timerDelay = 25
    app.count = 0
    app.paused = False
    #will go up to 100!
    app.trail = []
    #app.colors = ['lightcoral', 'sandybrown', 'khaki', 'darkseagreen', 'powderblue', 'thistle', 'lightpink']
    app.colors =  ["darkkhaki", 'darkseagreen', 'lightsteelblue', 'lightblue', 'paleturquoise', 'darkseagreen']

def keyPressed(app, event):
    if (event.key == 'Enter') and len(app.coords) > 1:
        app.running = False
        app.done = False
        app.trail = []
        app.count = 0
    elif (event.key == "Space") and len(app.coords) > 1:
        if not app.running:
            app.count = 0
            app.secondcoords = getmids(app.coords, app.count)
            app.trail = []
            app.trail.append(app.coords[0])
            app.timerDelay = 25
            app.done = False
            app.running = True
        else:
            if app.paused:
                app.paused = False
            else:
                app.paused = True
    elif (event.key == "Delete"):
        app.coords = []
        app.running = False
        app.done = False
        app.trail = []
        app.count = 0
    elif (event.key == "Up"):
        app.timerDelay = int(0.75*app.timerDelay)
    elif (event.key == "Down"):
        app.timerDelay = int(1.25*app.timerDelay)
    elif (event.key == "Left"):
        if len(app.coords) > 0:
            app.deleted.append(app.coords.pop())
        app.running = False
        app.done = False
        app.trail = []
        app.count = 0
    elif (event.key == "Right"):
        if len(app.deleted) > 0:
            app.coords.append(app.deleted.pop())
        app.running = False
        app.done = False
        app.trail = []
        app.count = 0


def mousePressed(app, event):
    app.running = False
    app.done = False
    app.coords.append((event.x, event.y))
    app.trail = []
    app.secondcoords = []
    app.count = 0


def timerFired(app):
    if app.running and not app.paused:
        if app.count < 100:
            app.count += 1
            app.secondcoords = getmids(app.coords, app.count)
        else:
            app.running = False
            app.done = True
        look = app.secondcoords
        while look[1] != None:
            look = look[1]
        app.trail.append(look[0][0])
 
def redrawAll(app, canvas):
    if app.done:
        color = "lightgrey"
    else:
        color = "black"
    if (len(app.coords) > 0):
        canvas.create_oval(app.coords[0][0] - 3, app.coords[0][1] - 3, app.coords[0][0] + 3, app.coords[0][1] + 3, fill=color, outline=color)
        for i in range(len(app.coords) - 1):
            canvas.create_line(app.coords[i][0], app.coords[i][1], app.coords[i+1][0], app.coords[i+1][1], fill=color)
            canvas.create_oval(app.coords[i+1][0] - 3, app.coords[i+1][1] - 3, app.coords[i+1][0] + 3, app.coords[i+1][1] + 3, fill=color, outline=color)
    if app.running:
        canvas.create_oval(app.coords[0][0] - 3, app.coords[0][1] - 3, app.coords[0][0] + 3, app.coords[0][1] + 5, fill="red", outline="red")
        look = app.secondcoords
        num = 0
        while look != None:
            points = look[0]
            newcolor = app.colors[num%(len(app.colors))]
            if len(points) == 1:
                canvas.create_oval(points[0][0] - 3, points[0][1] - 3, points[0][0] + 3, points[0][1] + 3, fill="red", outline="red")
            else:
                for i in range(len(points) - 1):
                    canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill=newcolor)
                    canvas.create_oval(points[i][0] - 3, points[i][1] - 3, points[i][0] + 3, points[i][1] + 3, fill=newcolor, outline=newcolor)
                    canvas.create_oval(points[i+1][0] - 3, points[i+1][1] - 3, points[i+1][0] + 3, points[i+1][1] + 3, fill=newcolor, outline=newcolor)
                #canvas.create_oval(points[0][0] - 5, points[0][1] - 5, points[0][0] + 5, points[0][1] + 5, fill="white", outline="gray")
            look = look[1]
            num += 1
        if len(app.trail) > 1:
            for i in range(len(app.trail) - 1):
                canvas.create_line(app.trail[i][0], app.trail[i][1], app.trail[i+1][0], app.trail[i+1][1], fill="red")
    if app.done:
        canvas.create_oval(app.coords[0][0] - 3, app.coords[0][1] - 3, app.coords[0][0] + 3, app.coords[0][1] + 3, outline="red", fill="red")
        if len(app.trail) > 1:
            for i in range(len(app.trail) - 1):
                canvas.create_line(app.trail[i][0], app.trail[i][1], app.trail[i+1][0], app.trail[i+1][1], fill="red")
        leng = len(app.coords) - 1
        canvas.create_oval(app.coords[leng][0] - 3, app.coords[leng][1] - 3, app.coords[leng][0] + 3, app.coords[leng][1] + 3, outline="red", fill="red")
    

runApp(width=400, height=400)