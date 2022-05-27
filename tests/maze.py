
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
adjMatrix = [[0 for x in range(2*numcolumns)] for y in range(4* numcolumns)]

# Loop over grid 
i = 0
j = 0
diag=False
#while i < numcolumns and j < numrows:
for i in range(numcolumns):
    for j in range(numrows):
    #adjmatrix[0][4]=1 means there is an edge between 0 and 4
        jumpVal = grid[i][j]
    #hitting circle initially
        #if jumpVal<0 and diag == False:
        #    diag = True
    #hitting cirlce second time
        #elif diag == True and jumpVal<0:
        #    diag = False

    #We only want the possitive part of jumpval
        jumpVal = abs(jumpVal)
    
        #if diag == False:
        #Down  (Right?)
        if j+jumpVal < 2* numrows:
            adjMatrix[i][j+jumpVal] = 1
        #Right
        if i+jumpVal < 2*numcolumns:
            adjMatrix[i+jumpVal][j] = 1
        #Left (Down?)
        if i-jumpVal >= 0:
            adjMatrix[i-jumpVal][j] = 1
        #Up
        if j-jumpVal >=0:
            adjMatrix[i][j-jumpVal] = 1
        #else:
    #we go to negative rules
            #down left
        if i-jumpVal>=0 and j+jumpVal < numrows:
            adjMatrix[(i-jumpVal)+numrows][(j+jumpVal)] = 1
        #down right
        if i+jumpVal<numcolumns and j+jumpVal<numrows:
            adjMatrix[(i+jumpVal)+numrows][(j+jumpVal)] = 1
        #up left
        if i-jumpVal>=0 and j-jumpVal>=0:
            adjMatrix[(i-jumpVal)+numrows][(j-jumpVal)+numrows] = 1
        #up right
        if i+jumpVal<numcolumns and j-jumpVal>=0:
            adjMatrix[(i+jumpVal)+numrows][(j-jumpVal)] = 1
#we connect the "real" goal node to the "diagonal" goal
# because reaching either finishes the puzzle
goalUpper = (numcolumns-1)(numrows-1)
goalLower = goalUpper * 2
adjMatrix[][(numrows-1)+numrows]=1
print(adjMatrix)

#Use matrix to create graph


    
#Analyze graph     
        






