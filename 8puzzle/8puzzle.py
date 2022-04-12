import copy
import sys


class CrossingNode:
    def __init__(self, info, parent, g, h):
        self.info = info
        self.parent = parent
        self.g = g #the cost until this node
        self.f = g + h #h is estimation until final node
    def getPath(self):
        path = [self]
        currentNode = self
        while currentNode.parent != None:
            path.insert(0, currentNode.parent)
            currentNode = currentNode.parent
        return path

    def inPath(self, infoNewNode): #the label of the node to check
        path = self.getPath()
        for node in path:
            if node.info == infoNewNode:
                return True
        return False

    def printPath(self, printCost = False, printLgPath = False):
        path = self.getPath()
        for i, node in enumerate(path):
            print(i + 1,")\n", str(node), sep="")
        if printCost:
            print("Cost: ", self.g)
        if printLgPath:
            print("Lenght: ", len(path))
        return len(path)


    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return(sir)

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
            sir +="\n"
            return sir

class Graph:
    def __init__(self, fileName):
        f = open(fileName)
        strFile = f.read()
        self.start = []
        try:
            lines = strFile.strip().split("\n")
            for line in lines:
                line = line.replace(" ", '')
                line = [int(x) for x in line]
                self.start.append(line)
            self.scopes = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        except:
            print("Parse error!")
            sys.exit(0) #iese din program

    def ifScope(self, currentNode):
        return currentNode in self.scopes

    def generateSuccessors(self, currentNode, euristic ="basic"):
        successors = []
        #move the empty space
        for emptyLine in range(len(currentNode.info)): #for each line we will search 0
            try:
                emptyCol = currentNode.info[emptyLine].index(0)
                break
            except:
                pass
        #all possible moves:
        possibleMoves = [[emptyLine, emptyCol + 1], [emptyLine, emptyCol - 1], [emptyLine + 1, emptyCol],[emptyLine - 1, emptyCol] ]
        for newLine, newCol in possibleMoves :
            if 0 <= newCol < 3 and 0 <= newLine < 3: #if it's still in matrix
                copyMatrix = copy.deepcopy(currentNode.info)
                copyMatrix[emptyLine][emptyCol] = copyMatrix[newLine][newCol] #swap them
                copyMatrix[newLine][newCol] = 0
                if not currentNode.inPath(copyMatrix): #to avoid cycles
                    #the cost from a state to another is +1
                    successors.append(CrossingNode(copyMatrix, currentNode, currentNode.g + 1, self.calculateHNode(copyMatrix) ))
        return successors

    def calculateHNode(self, infoNode, euristic = " basic"):
        if infoNode in self.scopes:
            return 0
        if euristic == "basic":
            return 1
        h = 0
        dim = len(infoNode[0]) # the dimension of the board
        for lineCell in range(dim):
            for colCell in range(dim):
                cell = infoNode[lineCell][colCell]
                goodLine = (cell - 1) // dim #the line where the cell should be
                goodCol = (cell - 1) % dim
                h += abs(lineCell - goodLine) + abs(colCell - goodCol) #how much we should shift this cell
        return h
    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)
#
# def astar(gr, nrSearchedSolutions, euristic):
#     startNode = CrossingNode( gr.start, None, 0, gr.calculateHNode(gr.start))
#     queue = [startNode]
#
#     while len(queue) > 0:
#
#         currentNode = queue.pop(0)
#         if gr.ifScope(currentNode):
#             print("Solution:")
#             print(currentNode.getPath())
#             nrSearchedSolutions -= 1
#             if nrSearchedSolutions == 0:
#                 return
#         successors = gr.generateSuccessors(currentNode, euristic)
#         for successor in successors:
#             foundPlace = False
#             for i in range(len(queue)):
#                 if successor.f < queue[i].f: #will eliminiate from open and then add the current node in open
#                    foundPlace = True
#                    break
#             if foundPlace == True:
#                 queue.insert(i, successor)
#             else:
#                 queue.append(successor)
# f = open("puzzleInput.txt")
# strFile = f.read()
# start =[]
# lines = strFile.strip().split("\n")
# for line in lines:
#     line = line.replace(" ", '')
#     line = [int(x) for x in line]
#     start.append(line)

def astar(gr, nrSearchedSolutions, euristic):
    startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start))
    queue = [startNode]

    while len(queue) > 0:
        currentNode = queue.pop(0)
        if gr.ifScope(currentNode):
            print("Solution:")
            print(currentNode.printPath())
            nrSearchedSolutions -= 1
            if nrSearchedSolutions == 0:
                return
        successors = gr.generateSuccessors(currentNode, euristic)
        for successor in successors:
            foundPlace = False
            for i in range(len(queue)):
                if successor.f < queue[i].f:  # will eliminiate from open and then add the current node in open
                    foundPlace = True
                    break
            if foundPlace == True:
                queue.insert(i, successor)
            else:
                queue.append(successor)



gr = Graph("puzzleInput.txt")
startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start))
astar(gr,3,"basic")
# succesors = gr.generateSuccessors(startNode)
# newNode = succesors[0]
# print(repr(newNode))
# succesors = gr.generateSuccessors(newNode)
# print(succesors)
#print(gr.calculateHNode(gr.start))