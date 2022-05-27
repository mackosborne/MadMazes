import networkx as nx
import matplotlib.pyplot as plt
import scipy
from pyvis.network import Network
#--------------------SETUP and READ INPUT -----------------------------
f = open("input.txt", "r")
firstline = f.readline()
numrows = int(firstline[0])
numcolumns = int(firstline[2])
grid = []
diaggrid = []
axisgrid = []
negative = False
i=0
while i < numrows:
    ithline = f.readline()
    line = []
    for item in ithline: 
        if item == '-':
            negative = True
        elif item == '\n':
            break
        elif item != ' ' and negative == False:
            line.append(int(item))
        elif item !=  ' ' and negative == True:
            line.append(-abs(int(item)))
            negative = False  
    diaggrid.append(line)
    axisgrid.append(line)
    i=i+1
for line in axisgrid:
    grid.append(line)
for line in diaggrid:
    grid.append(line)
#-----------------------------------------------------------------------------------
edges = []
#----------COLLECT ALL EDGES FOR THE NORMAL ZONE --------------------------
#- Notice we ignore negative values, we address those later in the special-
#- cases. Same goes for the diagonal zone.                                -
#--------------------------------------------------------------------------
for i in range(numcolumns):
    for j in range(numrows):
        if grid[i][j] >= 0:
            val = abs(grid[i][j])
            nodeA = (i,j)
        #----- CAN WE GO RIGHT? -----
            if j + val < numcolumns:
                nodeB = (i,j+val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #----- CAN WE GO LEFT? ----
            if j - val >= 0:
                nodeB = (i,j-val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO DOWN? ----
            if i+val < numrows:
                nodeB = (i+val,j)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO UP? ------
            if i-val >= 0:
                nodeB = (i-val,j)
                edge = (nodeA, nodeB)
                edges.append(edge)

#---------------- COLLECT ALL EDGES FOR THE DIAGONAL ZONE ---------------
#-   Remember, j will remain the same but i is increased by the         -
#- size of the graph (numrows) to put it in the lower zone              -
#------------------------------------------------------------------------
for i in range(numcolumns):
    for j in range(numrows):
        if grid[i][j] >= 0:
            val = abs(grid[i][j])
            loweri = i +numrows
            nodeA = (loweri,j)
        #---- CAN WE GO UP LEFT? ----
            if i-val >= 0 and j-val >=0:
                nodeB = (loweri-val, j-val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO UP RIGHT? ----
            if i-val >= 0 and j + val < numcolumns:
                nodeB = (loweri-val, j+val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO DOWN LEFT? ---
            if i+val < numrows and j-val >= 0:
                nodeB = (loweri+val, j-val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO DOWN RIGHT? --
            if i+val < numrows and j + val < numcolumns:
                nodeB = (loweri+val, j+val)
                edge = (nodeA, nodeB)
                edges.append(edge)

#------------ COLLECT ALL OF THE SCPECIAL CASE EDGES ---------------
#- 1) If we hit a negative in the "normal zone" we must diagonally -
#-    connect to "diagonal zone"                                   -
#- 2) If we hit a negative in the "diagonal zone" we must axis     -
#-    connect to the "normal zone"                                 -
#- 3) We must connect the goal in both "zones" as hitting either   -
#-    completes the maze                                           -
#-------------------------------------------------------------------
#-------------- CASE 1 ---------------------------------------------
for i in range(numcolumns):
    for j in range(numrows):
        if grid[i][j] < 0:
            val = abs(grid[i][j])
            loweri = i +numrows
            nodeA = (i,j)
        #---- CAN WE GO UP LEFT? ----
            if i-val >= 0 and j-val >=0:
                nodeB = (loweri-val, j-val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO UP RIGHT? ----
            if i-val >= 0 and j + val < numcolumns:
                nodeB = (loweri-val, j+val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO DOWN LEFT? ---
            if i+val < numrows and j-val >= 0:
                nodeB = (loweri+val, j-val)
                edge = (nodeA, nodeB)
                edges.append(edge)
        #---- CAN WE GO DOWN RIGHT? --
            if i+val < numrows and j + val < numcolumns:
                nodeB = (loweri+val, j+val)
                edge = (nodeA, nodeB)
                edges.append(edge)
#----------------- CASE 2  -----------------------------------
for i in range(numcolumns):
    for j in range(numrows):
        if grid[i][j] < 0:
            val = abs(grid[i][j])
            loweri = i +numrows
            nodeA = (loweri,j)
    #----- CAN WE GO RIGHT? -----
            if j + val < numcolumns:
                nodeB = (i,j+val)
                edge = (nodeA, nodeB)
                edges.append(edge)
    #----- CAN WE GO LEFT? ----
            if j - val >= 0:
                nodeB = (i,j-val)
                edge = (nodeA, nodeB)
                edges.append(edge)
    #---- CAN WE GO DOWN? ----
            if i+val < numrows:
                nodeB = (i+val,j)
                edge = (nodeA, nodeB)
                edges.append(edge)
    #---- CAN WE GO UP? ------
            if i-val >= 0:
                nodeB = (i-val,j)
                edge = (nodeA, nodeB)
                edges.append(edge)
#--------------- CASE 3 --------------------------
goalA=(numcolumns-1, numrows-1)
goalB=(2*numcolumns-1, numrows-1)
edge = (goalA,goalB)
edges.append(edge)
#--------------------------------------------------
#Create connected grapgh
G = nx.DiGraph()
G.add_edges_from(edges)
#Implement Dijkstra's
path = nx.dijkstra_path(G,(0,0),goalB)
#print(path)
#---------------------------------------------------
#Interprit path to desired output and print
output = []
for node in path:
    newcoords = []
    for coord in node:
        newcoord = coord
        if newcoord >= numrows:
            newcoord = newcoord - numrows
        newcoord = newcoord+1
        newcoords.append(newcoord)
    newnode = (newcoords[0],newcoords[1])
    output.append(newnode)
output.pop()
print(*output, sep=' ')
#--------------------------------------------------
#----------- GENERATE VISUAL-----------------------

nt = Network('1000px', '1000px')
# populates the nodes and edges 
for edge in edges:
    for node in edge:
        intrep=(node[0]*numrows)+node[1]
        if node in path:
            nt.add_node(intrep, label=node,color = '#dd4b39')
        else:
            nt.add_node(intrep, label=node)
    malA = edge[0]
    malB = edge[1]
    intrepA=(malA[0]*numrows)+malA[1]
    intrepB=(malB[0]*numrows)+malB[1]
    nt.add_edge(intrepA, intrepB, weight=.87)
nt.show('nx.html')
#-------------------------------------------------------------------------    


        

        