# 20 5 2 === cabbages, goats wolves
# 3 4 5 === A B StoreHouse
# 1 1 2 === wolves(how many goats, how many wolves) goats(how mny cabbages)
# 14 7 1 === final state cabbages, goats wolves

#state (final shore, inital shore, location boat, nothing in containers)

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
                if node.parent.info[6] == 1:
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

    def inPath(self, infoNewNode): #the label of the node to check
        path = self.getPath()
        for node in path:
            if node.info == infoNewNode:
                return True
        return False

    def __str__(self):
        if self.info[6] == 1:
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
        lines = f.readlines()

        self.__class__initalShore = "Est"
        self.__class__finalShore = "West"

        start = lines[0].strip().split()
        containers = lines[1].strip().split()
        eating = lines[2].strip().split()
        final = lines[3].strip().split()

        self.__class__.cabbages = int(start[0])
        self.__class__.goats = int(start[1])
        self.__class__.wolves = int(start[2])

        self.start = (0, 0, 0, self.__class__.cabbages, self.__class__.goats, self.__class__.wolves, 1, 0, 0, 0)#final shore, inital shore, location boat, nothing in containers

        self.__class__.A = int(containers[0])
        self.__class__.B = int(containers[1])
        self.__class__.StoreHouse = int(containers[2])

        self.__class__.wolvesEatGoats = int(eating[0])
        self.__class__.wolvesEatWolves = int(eating[1])
        self.__class__.goatsEatCabbages = int(eating[2])

        finalCabbages = int(final[0])
        finalGoats = int(final[1])
        finalWolves = int(final[2])

        self.final =(finalCabbages, finalGoats, finalWolves)

        #location boat = 1 --> initial shore, 0 --> final shore

    def ifScope(self, currentNode):
        return currentNode.info[0] >= currentNode.final[0] and currentNode.info[1] >= currentNode.final[1] and currentNode.info[2] >= currentNode.final[2]

    def generateSuccessors(self, currentNode, euristic = "basic"): #generates a list of nodes
        #current Shore = shore with boat; opposite shore = without boat

        def areEating(goats, wolves):
            if goats == 0:
                return False
            return goats < wolves

        listSuccessors = []
        #############################################currentNode = ( wolves, goats, boatShore)
        boat = currentNode.info[6]
        if boat == 1: #it is on the initial shore
            cabbagesCurrentShore = currentNode.info[0]
            goatsCurrentShore = currentNode.info[1]
            wolvesCurrentShore = currentNode.info[2]

            cabbagesOppositeShore = currentNode.info[3]
            wolvesOppositeShore = currentNode.info[4]
            goatsOppositeShore =currentNode.info[5]
        else: #it's on the final shore & we know rom the initial shore --> difference
            cabbagesCurrentShore = currentNode.info[3]
            goatsCurrentShore = currentNode.info[4]
            wolvesCurrentShore = currentNode.info[5]

            cabbagesOppositeShore = currentNode.info[0]
            wolvesOppositeShore = currentNode.info[1]
            goatsOppositeShore = currentNode.info[2]

        maxGoatsInA = min(Graph.A, goatsCurrentShore)
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
            if not currentNode.info[0] < currentNode.final[0] or currentNode.info[1] < currentNode.final[1] or currentNode.info[2] < currentNode.final[2]:
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

# gr = Graph("input.txt")
# CrossingNode.gr = gr
# nrSearchedSolution = 3
# a_star(gr, nrSearchedSolutions = nrSearchedSolution, euristic = "basic")
#print(gr)
# startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start))
# path = gr.generateSuccessors(startNode)
# succesor = path[0]
# print(succesor)
# path = gr.generateSuccessors(succesor)
# print(len(path))

fileName = "input.txt"
f = open(fileName)
lines = f.readlines()
start = lines[0].strip().split()
containers = lines[1].strip().split()
eating = lines[2].strip().split()
final = lines[3].strip().split()

cabbages = int(start[0])
goats = int(start[1])
wolves = int(start[2])


A = int(containers[0])
B = int(containers[1])
StoreHouse = int(containers[2])

wolvesEatGoats = int(eating[0])
wolvesEatWolves = int(eating[1])
goatsEatCabbages = int(eating[2])

finalCabbages = int(final[0])
finalGoats = int(final[1])
finalWolves = int(final[2])


