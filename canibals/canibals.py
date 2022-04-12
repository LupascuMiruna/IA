class CrossingNode:
    gr = None
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

    def printPath(self, printCost = False, printLength = False):
        path = self.getPath()
        for node in path:
            if node.parent is not None:
                if node.parent.info[2] == 1:
                    startBoat = self.__class__.gr.initialShore
                    finalBoat = self.__class__.gr.finalShore
                else:
                    startBoat = self.__class__.gr.finalShore
                    finalBoat = self.__class__.gr.initialShore
                print(">>> Boat from shore {} to {} with {} wolves si {} goats.".format(startBoat, finalBoat, abs(node.info[0] - node.parent.info[0]), abs(node.info[1] - node.parent.info[1])))
            print(str(node))
        if printCost:
            print("Cost: ", self.g)
        if printLength:
            print("Length: ", len(path))


    # def showPath(self):
    #     path = self.getPath()
    #     print(("->").join(path))
    #     print("Cost: ", self.g)
    #     return len(path)

    def inPath(self, infoNewNode): #the label of the node to check
        path = self.getPath()
        for node in path:
            if node.info == infoNewNode:
                return True
        return False

    def __str__(self):
        if self.info[2] == 1:
            boatInitialShore = "<boat>"
            boatFinalShore = "      "
        else:
            boatFinalShore = "<boat>"
            boatInitialShore = "      "
        return ("Shore: " + self.gr.initialShore + " Wolves: {} Goats: {} {} ||| Shore: " + self.gr.finalShore + " Wolves: {} Goats: {} {}"). format(self.info[0], self.info[1], boatInitialShore, self.__class__.gr.N - self.info[0], self.__class__.gr.N - self.info[1], boatFinalShore)

    def __repr__(self):
        result = ""
        result += str(self.info)
        return(result)

class Graph:
    def __init__(self, fileName):
        f = open(fileName)
        readText = f.read()
        readList = readText.split()
        self.__class__.N = int(readList[0])
        self.__class__.placesInBoat = int(readList[1])
        self.__class__.initialShore = readList[2]
        self.__class__.finalShore = readList[3]
        self.start = (self.__class__.N, self.__class__.N, 1)
        #memorate just the number from the initial shore
        #location boat = 1 --> initial shore, 0 --> final shore

    def ifScope(self, currentNode):
        return currentNode.info[0] == currentNode.info[1] == 0

    def generateSuccessors(self, currentNode, euristic = "basic"): #generates a list of nodes
        #current Shore = shore with boat; opposite shore = without boat

        def areEating(goats, wolves):
            if goats == 0:
                return False
            return goats < wolves

        listSuccessors = []
        ############################################3#currentNode = ( wolves, goats, boatShore)
        boat = currentNode.info[2]
        if boat == 1: #it is on the initial shore
            wolvesCurrentShore = currentNode.info[0]
            goatsCurrentShore = currentNode.info[1]
            wolvesOppositeShore = Graph.N - wolvesCurrentShore
            goatsOppositeShore = Graph.N - goatsCurrentShore
        else: #it's on the final shore & we know rom the initial shore --> difference
            wolvesOppositeShore = currentNode.info[0]
            goatsOppositeShore = currentNode.info[1]
            wolvesCurrentShore = Graph.N - wolvesOppositeShore
            goatsCurrentShore = Graph.N - goatsOppositeShore

        maxGoatsInBoat = min(Graph.placesInBoat, goatsCurrentShore)
        for numberGoats in range(maxGoatsInBoat + 1):
            if numberGoats == 0:
                maxWolvesInBoat = min(Graph.placesInBoat, wolvesCurrentShore)
                minWolvesInBoat = 1 #the boat can not go alone
            else:   #the rest places
                maxWolvesInBoat = min(Graph.placesInBoat - numberGoats, wolvesCurrentShore, numberGoats) #we can not take more wolves in the boat
                minWolvesInBoat = 0 #the boat will go with at least 1 goat

                #try each possiility
            for numberWolves in range(minWolvesInBoat, maxWolvesInBoat + 1):
                #updated ==> the number of animals after the departure of the boat
                #current --> from where the boat left
                #opposite --> where it goes

                updatedCurrentWolves = wolvesCurrentShore - numberWolves
                updatedCurrentGoats = goatsCurrentShore - numberGoats
                updatedOppositeWolves = wolvesOppositeShore + numberWolves
                updatedOppositeGoats = goatsOppositeShore + numberGoats

                if areEating(updatedOppositeGoats, updatedOppositeWolves) or areEating(updatedCurrentGoats, updatedCurrentWolves):
                    continue #not a valid move --> test for the parent node

                if boat == 1:
                    infoNewNode = (updatedCurrentWolves, updatedCurrentGoats, 0)
                else:
                    infoNewNode = (updatedOppositeWolves, updatedOppositeGoats, 1)
                if not currentNode.inPath(infoNewNode):
                    costSuccessor = 1
                    listSuccessors.append(CrossingNode(infoNewNode, currentNode, currentNode.g + costSuccessor, h = CrossingNode.gr.calculateHNode(infoNewNode, euristic)))

        return listSuccessors

    def calculateHNode(self, infoNewNode, euristic = "basic"):
        if euristic == "basic":
            if not infoNewNode[0] == infoNewNode[1] == 0:
                return 1
            return 0
        else:
            #how many animals we have to move / number of places in boat
            return 2 * math.ceil((infoNewNode[0] + infoNewNode[1])/(self.placesInBoat - 1))+ (1 - infoNewNode[2]) - 1 ##########################333

    def  __repr__(self):
        result = ""
        for(k,v) in self.__dict__.items():
            result += "{} = {}\n".format(k, v)
        return result

def a_star(gr, nrSearchedSolutions, euristic):
    #in queue just CrossingNodes
    startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start))
    queue = [startNode]

    while len(queue) > 0:
        currentNode = queue.pop(0)
        #print(currentNode)
        if gr.ifScope(currentNode):
            print("Solution: ")
            currentNode.printPath(printCost = True, printLength = True)
            print("\n----------------\n")
            input("PRESS ANY KEY FOR THE NEXT SOLUTION")
            nrSearchedSolutions -= 1
            if nrSearchedSolutions == 0:
                return
        listSuccessors = gr.generateSuccessors(currentNode, euristic = euristic)
        for succesor in listSuccessors:
            #print(succesor)
            i = 0
            foundPlace = False
            for i in range(len(queue)):
                if queue[i].f > succesor.f:
                    foundPlace = True
                    break
            if foundPlace:
                queue.insert(i, succesor)
            else:
                queue.append(succesor)

gr = Graph("input.txt")
CrossingNode.gr = gr
nrSearchedSolution = 3
a_star(gr, nrSearchedSolutions = nrSearchedSolution, euristic = "basic")
#print(gr)
# startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start))
# path = gr.generateSuccessors(startNode)
# succesor = path[0]
# print(succesor)
# path = gr.generateSuccessors(succesor)
# print(len(path))