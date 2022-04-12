import copy


class CrossingNode:
    def __init__(self, info, parent, g = 0, h = 0):
        self.info = info    #the matrix with the stacks
        self.parent = parent
        self.g = g #consider cost = 1 for a move
        self.h = h
        self.f = h + g

    def getPath(self):
        result = [self]
        currentNode = self
        while currentNode.parent != None:
            currentNode = currentNode.parent
            result.insert(0, currentNode)
        return result

    def showPath(self, printCost = False, printLength = False):
        path = self.getPath()
        for node in path:
            print(str(node))
        if printLength:
            print("Length " + len(path))
        if printCost:
            print("Cost " + self.g)

    def inPath(self, infoNewNode):  #
        path = self.getPath()
        for nod in path:
            if nod.info == infoNewNode:
                return True
        return False
    def __str__(self):
        return str(self.info)

class Graph:
    def __init__(self, name_file):
        def takeStakes(str):
            stacks = str.strip().split("\n")
            listStacks = [strStack.strip().split() if strStack != "#" else [] for strStack in stacks]
            return listStacks


        f = open(name_file, "r")
        contentFile = f.read()#all the input
        states = contentFile.split("final states")
        self.start = takeStakes(states[0])
        self.scopes = []
        finalStates = states[1].strip().split("---")
        for scope in finalStates:
            self.scopes.append(takeStakes(scope))
        print("Initial state: ", self.start)
        print("Final states: ", self.scopes)

    def generateSuccesors(self, currentNode):
        listSuccessors = []
        currentStacks = currentNode.info
        nrStacks = len(currentStacks)
        for i in range(nrStacks): #for each stack we try to move the first block
            if len(currentStacks[i]) == 0: #we don't have any block
                continue
            auxStacks = copy.deepcopy(currentStacks)
            block = auxStacks[i].pop() #take the head of the stack  ---> just the letters on the block
            for j in range(nrStacks): #search a place to put it
                if j == i:  #we can not put it in the same place
                    continue
                intermStacks = copy.deepcopy(auxStacks) #new list of stacks that will be modified
                intermStacks[j].append(block)
                costMove = 1 + ord(block) - ord("a")
                listSuccessors.append(intermStacks)
                if not currentNode.inPath(intermStacks):    #TO SEE IF IT WAS NOT A PREVIOUS CONFIGURATION
                    newNode = CrossingNode(intermStacks,currentNode,currentNode.g + costMove, self.calculateH)
                    listSuccessors.append(newNode)
        return listSuccessors


graph = Graph("inputBlocks.txt")


