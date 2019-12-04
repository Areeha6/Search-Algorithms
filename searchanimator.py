
##
## CS 4222/5222 Artificial Intelligence
## Fall 2019
##
## Lab 2: path finding
##
##

from Tkinter import *
from time import time, sleep
#from pathlab import *
from pathlabsol import *

## Draw the graph on the main canvas
def draw(graph):
    for v in graph.nodes():
        x1,y1 = graph.locations[v]
        y1 = canvas.winfo_reqheight()-y1
        for u in graph.dict[v]:
            x2,y2 = graph.locations[u]
            y2 = canvas.winfo_reqheight()-y2
            canvas.create_line(x1,y1,x2,y2)
    for node in graph.locations:
        x,y = graph.locations[node]
        y = canvas.winfo_reqheight()-y
        canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "gray" )
        canvas.create_text(x-10,y-10,text=node)

## Trace the path (list of nodes) in red on the canvas
def draw_path(graph,path):
    coords = map(lambda v: graph.locations[v.state],path)
    x,y = coords[0]
    y = canvas.winfo_reqheight() - y
    canvas.create_rectangle( x-5, y-5, x+5, y+5, fill = "red" )
    for xnext,ynext in coords[1:]:
        ynext = canvas.winfo_reqheight()-ynext            
        canvas.create_line(x,y,xnext,ynext,width=4,fill="red")
        x,y = xnext,ynext

## Retrieve the solution from the path, calculate its cost and display
def get_solution(graph,path):
    cost=0;
    statePath = map(lambda v: v.state,path)
    statePath.reverse()
    for i in range(len(statePath)-1):
        cost = cost+graph.get(statePath[i],statePath[i+1])
    pathCostStr.set(str(cost))

## Mark all the nodes in the fringe set with blue
def draw_fringe(graph,fringe):
    coords = map(lambda v: graph.locations[v.state],fringe)
    for x,y in coords:
        y = canvas.winfo_reqheight()-y
        canvas.create_rectangle( x-5, y-5, x+5, y+5, fill = "blue" )

## Mark all the nodes in the closed set with black
def draw_closed(graph,closed):
    coords = map(lambda state: graph.locations[state],closed)
    for x,y in coords:
        y = canvas.winfo_reqheight()-y
        canvas.create_rectangle( x-5, y-5, x+5, y+5, fill = "black" )

## Display the number of nodes generated since search began
def display_nodecount():
    nodeCountStr.set(str(Node.nodecount))

## Callback registered with search algorithm to be called in each
## iteration to display the search state
def callback(graph,node,fringe,closed,halt):
    canvas.delete("all")
    draw(graph)
    draw_fringe(graph,fringe)
    draw_path(graph,node.path())
    draw_closed(graph,closed)
    display_nodecount()
    if halt: get_solution(graph,node.path())
    root.update_idletasks()
    sleep(1)

## Create a search problem on the graph, with initial state and goal,
## and run the selected search algorithm
def run(graph):
    prob = SearchProblem(start.get(),goal.get(),graph)
    pathCostStr.set("")
    if algo.get() == "graph search":
        graph_search(prob,[],callback)
    elif algo.get() == "BFS":
        breadth_first_graph_search(prob,callback)
    elif algo.get() == "DFS":
        depth_first_graph_search(prob,callback)
    elif algo.get() == "greedy best-first":
        best_first_graph_search(prob, prob.h, callback)
    elif algo.get() == "A*":
        astar_search(prob, callback)
    else:
        exit("Unknown algorithm selected")

## The graph from the book
romania = UndirectedGraph({
    'Arad':{'Zerind':75, 'Sibiu':140, 'Timisoara':118},
    'Bucharest':{'Urziceni':85, 'Pitesti':101, 'Giurgiu':90, 'Fagaras':211},
    'Craiova':{'Drobeta':120, 'Rimnicu Vilcea':146, 'Pitesti':138},
    'Drobeta':{'Mehadia':75},
    'Eforie':{'Hirsova':86},
    'Fagaras':{'Sibiu':99},
    'Hirsova':{'Urziceni':98},
    'Iasi':{'Vaslui':92, 'Neamt':87},
    'Lugoj':{'Timisoara':111, 'Mehadia':70},
    'Oradea':{'Zerind':71, 'Sibiu':151},
    'Pitesti':{'Rimnicu Vilcea':97},
    'Rimnicu Vilcea':{'Sibiu':80},
    'Urziceni':{'Vaslui':142}})
romania.locations = {
    'Arad':( 91, 492),    'Bucharest':(400, 327),    'Craiova':(253, 288),   'Drobeta':(165, 299), 
    'Eforie':(562, 293),    'Fagaras':(305, 449),    'Giurgiu':(375, 270),   'Hirsova':(534, 350),
    'Iasi':(473, 506),    'Lugoj':(165, 379),    'Mehadia':(168, 339),   'Neamt':(406, 537), 
    'Oradea':(131, 571),    'Pitesti':(320, 368),    'Rimnicu Vilcea':(233, 410),   'Sibiu':(207, 457), 
    'Timisoara':( 94, 410),    'Urziceni':(456, 350),    'Vaslui':(509, 444),   'Zerind':(108, 531)}

        
## Initialize environment
root = Tk()
windowWidth = 900
windowHeight = 400
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("{}x{}".format(windowWidth, windowHeight) + "+{}+{}".format(positionRight, positionDown))
root.title( "Search Animator" )

## Set up canvas for input window
canvas = Canvas( root, width=windowWidth-300, height=windowHeight+200 )
canvas.place(x=0,y=0)

## Set up canvas for control panel
controlFrame = Frame( root, height=windowHeight-180,width=275,borderwidth=2,relief=SUNKEN)
controlFrame.place(x=600,y=200/2);
controlFrame.propagate(0)
control = Canvas(controlFrame)
control.pack(expand=YES,fill=BOTH)

## Go button
go = Button(control,text="Go",width=10,command=lambda : run(romania))
go.grid(row=1,column=1,sticky='w',padx=5,pady=5)
go.propagate(0)

## Start node menu
start = StringVar(root)
start.set("Arad")
startNodeMenu = OptionMenu(control,start,*romania.nodes())
startNodeMenu.grid(row=2,column=2,sticky=W,padx=5,pady=5)
Label(control,text="Start:").grid(row=2,column=1,sticky=E,padx=5,pady=5)

## Goal node menu
goal = StringVar(root)
goal.set("Bucharest")
goalNodeMenu = OptionMenu(control,goal,*romania.nodes())
goalNodeMenu.grid(row=3,column=2,sticky=W,padx=5,pady=5)
Label(control,text="Goal:").grid(row=3,column=1,sticky=E,padx=5,pady=5)

## Algo menu
algos = ["graph search", "BFS", "DFS", "greedy best-first", "A*"]
algo = StringVar(root)
algo.set(algos[0])
algoMenu = OptionMenu(control,algo,*algos)
algoMenu.grid(row=4,column=2,sticky=W,padx=5,pady=5)
Label(control,text="Algo:").grid(row=4,column=1,sticky=E,padx=5,pady=5)


## Nodes generated display
nodeCountStr = StringVar(root)
Label(control,text="Nodes generated:").grid(row=5,column=1,sticky=E,padx=5,pady=5)
Label(control,textvariable=nodeCountStr).grid(row=5,column=2,sticky=W,padx=5,pady=5)
nodeCountStr.set("0")

## Solution cost display
pathCostStr = StringVar(root)
Label(control,text="Solution cost:").grid(row=6,column=1,sticky=E,padx=5,pady=5)
Label(control,textvariable=pathCostStr).grid(row=6,column=2,sticky=W,padx=5,pady=5)
pathCostStr.set("")

## Draw the graph
draw(romania)

## Main loop
if __name__ == "__main__":
    root.mainloop()

