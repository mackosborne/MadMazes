
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
#def getinput():
from turtle import circle

#---------- Read Input and build arrays----------
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

#If we encounter a negative numer we connect our edge to the other side of the connected graph (+/- 8)
#We need to be sure we do not go across the "8 line" accidentally (add a conditional)
#Adjacency matric is 2n*n in size - look to last project to make this

#----------Build Adj Matrix of same width as Maze and double the lenght-------
adjMatrix = [[0 for x in range(numcolumns)] for y in range(2* numcolumns)]

# Loop over grid 
i = 0
j = 0
diag=False
for i in range(numrows):
    for j in range(numcolumns):
        #adjmatrix[0][4]=1 means there is an edge between 0 and 4
        jumpVal = grid[i][j]
        #hitting circle initially
        if jumpVal<0:
            diag = True
        #hitting cirlce second time
        if diag == True and jumpVal<0:
            diag = False
            goBack = True
    
        if diag == False:
            #Down
            if j+jumpVal < numrows:
                adjMatrix[i][j+jumpVal] = 1
            #G.add_edge(i,i+jumpVal)
        #Right
            if i+jumpVal < numcolumns:
                adjMatrix[i+jumpVal][j] = 1
            #G.add_edge(i+jumpVal,j)
        #Left
            if i-jumpVal >= 0:
                adjMatrix[i-jumpVal][j] = 1
            #G.add_edge(i-jumpVal,j)
        #Up
            if j-jumpVal >=0:
                adjMatrix[i][j-jumpVal] = 1
            #G.add_edge(i,j-jumpVal)
        else:
    #we go to negative rules
        #down left
            if i-jumpVal>=0 and j+jumpVal < numrows:
                adjMatrix[i-jumpVal][2*(j+jumpVal)] = 1
            #G.add_edge(i,j-jumpVal)
        #down right
            if i+jumpVal<numcolumns and j+jumpVal<numrows:
                adjMatrix[i+jumpVal][2*(j+jumpVal)] = 1
            #G.add_edge(i+jumpVal,2*(j+jumpVal))
        #up left
            if i-jumpVal>=0 and j-jumpVal>=0:
                adjMatrix[i-jumpVal][2*(j-jumpVal)] = 1
            #G.add_edge(i-jumpVal,2*(j-jumpVal))
        #up right
            if i+jumpVal<numcolumns and j-jumpVal>=0:
                adjMatrix[i+jumpVal][2*(j-jumpVal)] = 1
            #G.add_edge(i+jumpVal,2*(j-jumpVal))
#we connect the "real" goal node to the "diagonal" goal
# because reaching either finishes the puzzle
adjMatrix[numcolumns-1*numrows-1][numcolumns-1*(numrows-1)*2]=1
#G.add_edge(numcolumns-1*numrows-1,numcolumns-1*(numrows-1)*2)
print(grid)
print(adjMatrix)


nx.draw(G, with_labels=True)
nx.dfs_edges(G,1)
plt.show()