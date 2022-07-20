from mpl_toolkits import mplot3d
from scipy.spatial import Delaunay,ConvexHull, distance
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from tkinter import *
import sys
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
from tkinter import ttk, filedialog

points=np.array([])

def plot_triangulation():
    global points
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) == 6:
            label.grid_remove()
    if len(points) < 4:
        label=Label(root, text=f"Number of points(={len(points)}) is not enough to construct initial simplex, number of points must be more than 3",fg="red")
        label.grid(row=6,columnspan=3,sticky=W+E)
        return
    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(projection='3d')
    triangulation = Delaunay(points)
    edges = edge_collection(triangulation)
    x = np.array([])
    y = np.array([])
    z = np.array([])
    for (i,j) in edges:
        x = np.append(x, [points[i, 0], points[j, 0]])      
        y = np.append(y, [points[i, 1], points[j, 1]])      
        z = np.append(z, [points[i, 2], points[j, 2]])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.plot3D(x, y, z, color='black', lw='0.5')
    hull = ConvexHull(points)
    for s in hull.simplices:
        tri = Poly3DCollection([points[s]])
        tri.set_color("gray")
        tri.set_alpha(0.5)
        tri.set_edgecolor('red')
        tri.set_linewidth(2)
        ax.add_collection3d(tri)
        edges = []
        edges.append((s[0], s[1]))
        edges.append((s[1], s[2]))
        edges.append((s[2], s[0]))
        for v0, v1 in edges:
            ax.plot(xs=points[[v0, v1], 0], ys=points[[v0, v1], 1], zs=points[[v0, v1], 2], color='red', lw='2')
    for x, y, z in zip(points[:,0], points[:,1], points[:,2]):
        label = '(%.2f, %.2f, %.2f)' % (x, y, z)
        ax.text(x, y, z, label, 'y')
    ax.scatter(points[:,0], points[:,1], points[:,2], color='r')
    canvas = FigureCanvasTkAgg(fig,master = root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=7,column=0,sticky=W+E)
    
def edge_collection(triangulation):
    edges = set()
    def sort(a,b):
        return (a,b) if a < b else (b,a)
    # each edge cosidered just once in ploting delaunay triangulation
    for (s0, s1, s2, s3) in triangulation.simplices:
        edges.add(sort(s0,s1))
        edges.add(sort(s0,s2))
        edges.add(sort(s0,s3))
        edges.add(sort(s1,s2))
        edges.add(sort(s1,s3))
        edges.add(sort(s2,s3))
    return edges
    
def random_input():
    global points
    try:
        num=int(e1.get())
    except:
        label=Label(root, text="number of points must be integer",fg="red") 
        label.grid(row=6,columnspan=3,sticky=W+E)
        return
    try:
        range=float(e2.get())
    except: 
        label=Label(root, text="range of coordinates must be float",fg="red") 
        label.grid(row=6,columnspan=3,sticky=W+E)
        return
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) == 7 or int(label.grid_info()["row"]) == 6:
            label.grid_remove()
    x = np.around(range * np.random.rand(num),decimals=2) 
    y = np.around(range * np.random.rand(num),decimals=2)
    z = np.around(range * np.random.rand(num),decimals=2)
    RandomPoints = np.vstack([x, y, z]).T
    if len(points)==0:
        points=RandomPoints
    else:
        points=np.unique(np.vstack([points, RandomPoints]), axis=0)
    text.delete("1.0","end")
    text.insert(END, f"points:\n{points}") 

    
def open_file():
    global points
    filename =filedialog.askopenfilename(
        initialdir="",
        title="Open A File",
        filetype=(("xlsx files","*.xlsx"),("All Files","*.*"))
    )
    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_excel(filename)
            x =np.array(df['x'].values, dtype='float')
            y = np.array(df['y'].values, dtype='float')
            z = np.array(df['z'].values, dtype='float')
            FilePoints = np.vstack([x, y, z]).T
            for label in root.grid_slaves():
                if int(label.grid_info()["row"]) == 7 or int(label.grid_info()["row"]) == 6:
                    label.grid_remove()
            if len(points)==0:
                points=FilePoints
            else:
                points=np.unique(np.vstack([points, FilePoints]), axis=0)
            text.delete("1.0","end")
            text.insert(END, f"points:\n{points}")

        except:
            label=Label(root, text="File content isn't supported",fg="red") 
            label.grid(row=6,columnspan=3,sticky=W+E)

def add_point(x,y,z):
    global points
    try:
        x=np.array(float(x))
    except:
        label=Label(root, text="x must be float",fg="red") 
        label.grid(row=6,columnspan=3,sticky=W+E)
        return
    try:
        y=np.array(float(y))
    except:
        label=Label(root, text="y must be float",fg="red") 
        label.grid(row=6,columnspan=3,sticky=W+E)
        return
    try:
        z=np.array(float(z))
    except:
        label=Label(root, text="z must be float",fg="red") 
        label.grid(row=6,columnspan=3,sticky=W+E)
        return
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) == 7 or int(label.grid_info()["row"]) == 6:
            label.grid_remove()
    NewPoint = np.vstack([x, y, z]).T
    if len(points)==0:
        points=NewPoint
    else:
        points=np.unique(np.vstack([points, NewPoint]), axis=0)
    text.delete("1.0","end")
    text.insert(END, f"points:\n{points}")

def reset():
    global points
    for label in root.grid_slaves():
        if int(label.grid_info()["row"]) == 7 or int(label.grid_info()["row"]) == 6:
            label.grid_remove()
    points=np.array([])
    text.delete("1.0","end")
    text.insert(END, f"points:\n{points}")
               
root = Tk() 
root.resizable(0, 0)
root.title('3d delaunay triangulation')

frame1 = Frame(root, highlightbackground="white", highlightthickness=2,borderwidth = 4,relief="sunken", width=700, height=250)
frame1.grid(row=0,sticky=W+E)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=1)
frame1.grid_columnconfigure(2, weight=1)

frame2 = Frame(root, highlightbackground="white", highlightthickness=2,borderwidth = 4,relief="sunken")
frame2.grid(row=1,sticky=W+E)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(2, weight=1)


frame3 = Frame(root, highlightbackground="white", highlightthickness=2,borderwidth = 4,relief="sunken")
frame3.grid(row=5,sticky=W+E)
frame3.grid_columnconfigure(0, weight=50)
frame3.grid_columnconfigure(1, weight=1)

label=Label(frame1, text="Enter number of random points:") 
label.grid(row=0,column=0,sticky=W)

e1=Entry(frame1,width=40)
e1.grid(row=0,column=1,sticky=W+E) 

label=Label(frame1, text="Enter coordinates range of random points:") 
label.grid(row=1,column=0,sticky=W) 

e2=Entry(frame1,width=40)
e2.grid(row=1,column=1,sticky=W+E)

myButton = Button(frame1, text="Add random points",command=lambda: random_input(),fg="white",bg="blue",width=20)
myButton.grid(row=0,rowspan=2,column=2,sticky=N+S+E)

label=Label(frame2, text="x:",width=32) 
label.grid(row=0,column=0,sticky=W)

e3=Entry(frame2,width=40) 
e3.grid(row=0,column=1,sticky=W+E)

label=Label(frame2, text="y:",width=32) 
label.grid(row=1,column=0,sticky=W)

e4=Entry(frame2,width=40) 
e4.grid(row=1,column=1,sticky=W+E)

label=Label(frame2, text="z:",width=32) 
label.grid(row=2,column=0,sticky=W)

e5=Entry(frame2,width=40) 
e5.grid(row=2,column=1,sticky=W+E)

button=Button(frame2, text="Add point",width=20,command=lambda: add_point(e3.get(),e4.get(),e5.get()),fg="white",bg="blue") 
button.grid(row=0,column=2,rowspan=3,sticky=N+S+E)

myButton = Button(root, text="Draw", command=lambda: plot_triangulation(),fg="white",bg="blue")
myButton.grid(row=2,sticky=W+E)

myButton = Button(root, text="Open a file",command=lambda: open_file(),fg="white",bg="blue")
myButton.grid(row=3,sticky=W+E)

myButton = Button(root, text="Reset", command=lambda: reset(),fg="white",bg="Red")
myButton.grid(row=4,sticky=W+E)

text = Text(frame3,height=5)
text.pack(side="left")

scroll_y = Scrollbar(frame3, orient="vertical",command=text.yview)
scroll_y.pack(side="left", expand=True, fill="y")

text.configure(yscrollcommand=scroll_y.set)
text.insert(END,"points:")
root.mainloop()







