
from tkinter import *
from tkinter import messagebox
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import networkx as nx
from graph import MAXVAL, dijkstra, readGraph 
import matplotlib.pyplot as plt
import timeit
from tkinter import filedialog
import os
  

LARGEFONT = ('Helvetica 24 bold')
MEDIUMFONT = ('Helvetica 20 bold')
SMALLFONT = ('Helvetica 14')
VERYSMALLFONT = ('Helvetica 10')

def plot():
    global frGraph
    global filename
    global graph
    global frSrcDest
    global clicked
    global clicked2
    global solve_button

    

    # read graph
    try:
        graph = readGraph(filename)
    except:
        messagebox.showinfo(title="Invalid graph file", message="There's no such a file")
        return



    window.state('zoomed')

    # destroy existing frame
    frGraph.destroy()
    frGraph = Frame(frMain)
    frGraph.grid(row=0, column=0)
    frLeft.grid(row=0, column=0)
  
    # the figure that will contain the plot
    fig = figure(figsize = (8, 6),
                 dpi = 100)
  
  

    G = nx.DiGraph()
    length = len(graph)
    for i in range(length):
        for j in range(length):
            if graph[i][j] != 0:
               G.add_edge(str(i), str(j), weight=graph[i][j])
    
    e = [(u, v) for (u, v, d) in G.edges(data=True)]

    pos = nx.spring_layout(G, seed=7) 
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    # edges
    nx.draw_networkx_edges(
        G, pos, edgelist=e, width=6, edge_color="g", arrowstyle="->", arrowsize=20,
    )
    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)


    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
  
    canvas = FigureCanvasTkAgg(fig,
                               master = frGraph)  
    canvas.draw()
  
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas,
                                   frGraph)
    toolbar.update()
  
    canvas.get_tk_widget().pack()


    # create src dest entries
    options = [
    str(i) for i in range(length)
    ]
    clicked = StringVar()
    clicked2 = StringVar()
    
    # initial menu text
    clicked.set(0)
    clicked2.set(0)
    
    # Create Dropdown menu
    src_drop = OptionMenu(frSrcDest, clicked , *options)
    dest_drop = OptionMenu(frSrcDest, clicked2, *options)


    solve_button = Button(master = frSrcDest, 
                     command = solve,
                     height = 1, 
                     width = 5,
                     text = "Solve",
                     bg='#3399FF',
                      fg='white',
                      font = SMALLFONT)

    Label(frSrcDest, text="Source node:", bg='black', fg='white', font=SMALLFONT).grid(row=0)
    src_drop.grid(row=1)
    Label(frSrcDest, text="Destination node:", bg='black', fg='white', font=SMALLFONT).grid(row=2)
    dest_drop.grid(row=3)
    solve_button.grid(row=4, pady=10)

def browse():
    global filename
    global filename_label
    filename = filedialog.askopenfilename(initialdir = os.getcwd(),
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    filename_label.config(text=os.path.basename(filename))
    

def solve():
    global frResult

    src = int(clicked.get())
    dest = int(clicked2.get())
    iterations = [0]

    try:
        start = timeit.default_timer()
        result, path = dijkstra(graph, src, iterations)
        if result[dest] == MAXVAL:
            raise Exception("error")
        end = timeit.default_timer()
        time = end-start

        frResult.destroy()
        frResult = Frame(frRight, bg='#3399FF')
        frResult.grid(row=5, column=0, pady=10)
        Label(frResult, text="Dijkstra Result", font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=0, sticky=W)
        Label(frResult, text= ("Shortest distance = " + str(result[dest])), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=1, sticky=W)
        Label(frResult, text= ("Shortest path = " + (' - '.join(path[dest]))), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=2, sticky=W)
        Label(frResult, text= ("Total iterations = " + str(iterations[0])), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=3, sticky=W)
        Label(frResult, text= ("Time elapsed = " + str(time) + " s"), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=4, sticky=W)
    except:
        messagebox.showinfo(message="Destination node cant be reached from source")
        return

    
    


# the main Tkinter window
window = Tk()

# VARIABLE
filename = ''
graph = []

  
# setting the title 
window.title('Dijkstra Shortest Path Finder')
window.config(background='black')
Label(window, text="Dijkstra Shortest Path", font=LARGEFONT, fg='#4255cf', bg="black").pack()
  
# dimensions of the main window
window.geometry("500x200")

frMain = Frame(window, bg='black')
frLeft = Frame(frMain, bg = 'black')
frGraph = Frame(frLeft, bg = 'black')
frRight = Frame(frMain, bg = 'black')
frFileFrame = Frame(frRight, bg = 'black')
frSrcDest = Frame(frRight, bg = 'black')
frSrcDest.grid(row=4, column=0)
frResult = Frame(frRight, bg = 'black')
frResult.grid(row=5, column=0)

# filename input
Label(frRight, font=SMALLFONT, fg='white', bg='black', text="Filename:").grid(row=0, column=0)
frFileFrame.grid(row=1, column=0)
filename_label = Label(master = frFileFrame, text="No File Selected", font=VERYSMALLFONT)
filename_label.grid(row=0, column=0)

# browse button
Button(frFileFrame, font=VERYSMALLFONT, height=1, width=5, text="Browse", bg='#3399FF', fg='white', command = browse).grid(row=0, column=1, padx=5)

  
# button that displays the plot
plot_button = Button(master = frRight, 
                     command = plot,
                     height = 1, 
                     width = 5,
                     text = "Plot",
                     bg='#3399FF',
                     fg='white',
                     font = SMALLFONT)
plot_button.grid(row=3, column=0, pady=10)

frMain.pack(pady=10)
  
# place the button 
# in main window
frRight.grid(row=0, column=1, padx=30, pady=10)





  
# run the gui
window.mainloop()