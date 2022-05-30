
from tkinter import *
from tkinter import messagebox
from turtle import window_height 
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import networkx as nx
from graph import dijkstra, readGraph 
import matplotlib.pyplot as plt
import timeit
  

LARGEFONT = ('Helvetica 24 bold')
MEDIUMFONT = ('Helvetica 20 bold')
SMALLFONT = ('Helvetica 14')
VERYSMALLFONT = ('Helvetica 10')

def plot():
    global frGraph
    global filename
    global graph
    global frSrcDest
    global src_entry
    global dest_entry
    global solve_button

    # get input
    filename = filename_entry.get()
    

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

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

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
  
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = frGraph)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   frGraph)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


    # create src dest entries
    src_entry = Entry(master = frSrcDest)
    dest_entry = Entry(master = frSrcDest)


    solve_button = Button(master = frSrcDest, 
                     command = solve,
                     height = 1, 
                     width = 5,
                     text = "Solve",
                     bg='#3399FF',
                      fg='white',
                      font = SMALLFONT)

    Label(frSrcDest, text="Source node:", bg='black', fg='white', font=SMALLFONT).grid(row=0)
    src_entry.grid(row=1)
    Label(frSrcDest, text="Destination node:", bg='black', fg='white', font=SMALLFONT).grid(row=2)
    dest_entry.grid(row=3)
    solve_button.grid(row=4, pady=10)

def solve():
    global frResult

    src = int(src_entry.get())
    dest = int(dest_entry.get())
    iterations = [0]
    try:
        start = timeit.default_timer()
        result = dijkstra(graph, src, iterations)
        end = timeit.default_timer()
        time = end-start
    except:
        messagebox.showinfo(message="invalid source or destination")
        return
    
    frResult.destroy()
    frResult = Frame(frRight, bg='#3399FF')
    frResult.grid(row=5, column=0, pady=10)
    Label(frResult, text="Dijkstra Result", font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=0, sticky=W)
    Label(frResult, text= ("Shortest distance = " + str(result[dest])), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=1, sticky=W)
    Label(frResult, text= ("Total iterations = " + str(iterations[0])), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=2, sticky=W)
    Label(frResult, text= ("Time elapsed = " + str(time) + " s"), font=VERYSMALLFONT, bg='#3399FF', fg='white').grid(row=3, sticky=W)


# the main Tkinter window
window = Tk()

# VARIABLE
filename = ''
graph = []

# read graph
filename = "g1.txt"
graph = readGraph(filename)
  
# setting the title 
window.title('Plotting in Tkinter')
window.config(background='black')
Label(window, text="Dijkstra Shortest Path", font=LARGEFONT, fg='#4255cf', bg="black").pack()
  
# dimensions of the main window
window.geometry("500x200")

frMain = Frame(window, bg='black')
frLeft = Frame(frMain, bg = 'black')
frGraph = Frame(frLeft, bg = 'black')
frRight = Frame(frMain, bg = 'black')
frSrcDest = Frame(frRight, bg = 'black')
frSrcDest.grid(row=3, column=0)
frResult = Frame(frRight, bg = 'black')
frResult.grid(row=4, column=0)

# filename input
Label(frRight, font=SMALLFONT, fg='white', bg='black', text="Filename:").grid(row=0, column=0)
filename_entry = Entry(master = frRight)
filename_entry.grid(row=1, column=0)
  
# button that displays the plot
plot_button = Button(master = frRight, 
                     command = plot,
                     height = 1, 
                     width = 5,
                     text = "Plot",
                     bg='#3399FF',
                     fg='white',
                     font = SMALLFONT)
plot_button.grid(row=2, column=0, pady=10)

frMain.pack(pady=10)
  
# place the button 
# in main window
frRight.grid(row=0, column=1, padx=30, pady=10)





  
# run the gui
window.mainloop()