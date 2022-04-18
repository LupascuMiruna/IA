# 20 5 2 === cabbages, goats wolves
# 3 4 5 === A B StoreHouse
# 1 1 2 === wolves(how many goats, how many wolves) goats(how many cabbages)
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
        indexNode = 1
        for node in path:
            if node.parent is not None:
                # if node.parent.info[6] == 1:
                #     startBoat = self.__class__.gr.initialShore
                #     finalBoat = self.__class__.gr.finalShore
                # else:
                #     startBoat = self.__class__.gr.finalShore
                #     finalBoat = self.__class__.gr.initialShore
                # print(">>> Boat from shore {} to {} with {} wolves si {} goats.".format(startBoat, finalBoat, abs(node.info[0] - node.parent.info[0]), abs(node.info[1] - node.parent.info[1])))
                print(str(indexNode) + str(node)  + "\n")
                indexNode += 1
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
        if self.info["boat"] == 1:
            boatInitialShore = "<boat>"
            boatFinalShore = "      "
        else:
            boatFinalShore = "<boat>"
            boatInitialShore = "      "
        return ("Shore: {} Cabbages: {} Goats: {} Wolves: {} {} ||| Shore: {} Cabbages: {} Goats: {} Wolves: {}. In store there are Cabbages: {} Goats: {} Wolves: {} {}"). format(
            self.gr.initialShore,
            self.info["cabbagesEst"], self.info["goatsEst"], self.info["wolvesEst"], boatInitialShore,
            self.gr.finalShore, self.info["cabbagesWest"], self.info["goatsWest"], self.info["wolvesWest"],
            self.info["cabbagesStored"], self.info["goatsStored"], self.info["wolvesStored"], boatFinalShore)

    def __repr__(self):
        result = ""
        result += str(self.info)
        return(result)

class Graph:
    '''
    we can not memorate just one shore because the number of products may change (to eat each oher)

    currentNode.info = dictionary: {cabbagesEst, goatsEst, wolvesEst, boat, cabbagesWest, goatsWest, wolvesWest, cabbagesStored, goatsStored, wolvesStored)
                                    {0, 1, 2, 3, 4, 5, 6, 7, 8)
    info startNode = {cabbages, goats, wolves,(initially all the products on the start shore) 1(est), 0, 0, 0 (nothing on the west shore), 0, 0, 0(nothing in the storeHouse)}
    typeStored = -1 cabbages
                 0 goats
                 1 wolves
    '''
    def __init__(self, fileName):
        f = open(fileName)
        lines = f.readlines()

        self.__class__.initialShore = "Est"
        self.__class__.finalShore = "West"

        startInput = lines[0].strip().split()
        containers = lines[1].strip().split()
        eating = lines[2].strip().split()
        final = lines[3].strip().split()

        self.__class__.cabbages = int(startInput[0])
        self.__class__.goats = int(startInput[1])
        self.__class__.wolves = int(startInput[2])


        self.start = {"cabbagesEst" : self.__class__.cabbages, "goatsEst": self.__class__.goats, "wolvesEst": self.__class__.wolves,
                      "boat": 1,
                     "cabbagesWest": 0, "goatsWest": 0, "wolvesWest": 0,
                      "cabbagesStored": 0, "goatsStored": 0, "wolvesStored": 0
                      }

        self.__class__.A = int(containers[0])
        self.__class__.B = int(containers[1])
        self.__class__.StoreHouse = int(containers[2])

        self.__class__.wolvesEatGoats = int(eating[0])
        self.__class__.wolvesEatWolves = int(eating[1])
        self.__class__.goatsEatCabbages = int(eating[2])

        self.__class__.finalCabbages = int(final[0])
        self.__class__.finalGoats = int(final[1])
        self.__class__.finalWolves = int(final[2])

        self.trueInput = self.veifyInput()

        #self.final = {"finalCabbages": self.finalCabbages, "finalGoats": finalGoats, "finalWolves": finalWolves}

        #location boat = 1 --> initial shore, 0 --> final shore
    def veifyInput(self):
        '''
        check if we have enough products
        :return:
        '''
        if self.__class__.cabbages < self.__class__.finalCabbages:
            return 0
        if self.__class__.goats < self.__class__.finalGoats:
            return 0
        if self.__class__.wolves < self.__class__.finalWolves:
            return 0
        return 1 #it might be possible to reache the output desired

    def calculateHNode(self, infoNewNode, euristic, currentNode):
        if euristic == "basic":
            if self.ifScope(infoNewNode):
                return 0
            return 1

    def ifScope(self, infoNode):
        return infoNode["cabbagesWest"] + infoNode["cabbagesStored"] >= self.finalCabbages and \
               infoNode["goatsWest"] + infoNode["goatsStored"] >= self.finalGoats and \
               infoNode["wolvesWest"] + infoNode["wolvesStored"] >= self.finalWolves

    def generateSuccessors(self, currentNode, euristic = "basic"): #generates a list of nodes
        #current Shore = shore with boat; opposite shore = without boat
        def getCostSucc(cabbagesA, goatsA, wolvesA, cabbagesB, goatsB, wolvesB, boat):
            return 1
        
        def areEnoughProducts(info):
            #for cabbages
            if info["cabbagesWest"] + info["cabbagesStored"] + info["cabbagesEst"] < Graph.finalCabbages:
                return 0
            if info["goatsWest"] + info["goatsStored"] + info["goatsEst"] < Graph.finalGoats:
                return 0
            if info["wolvesWest"] + info["wolvesStored"] + info["wolvesEst"] < Graph.finalWolves:
                return 0
            return 1

        '''
        calculate number of products on the shore where THERE IS NOT the man
        '''
        def eat(info, newShoreMan):
            newDict = info.copy()
            if newShoreMan == 1:
                '''
                The man is on the est shore --> calculate on the west shore
                '''
                #if there are enough products --> each goat will eat as many cabbage as it needs, otherwise --> cabbages = 0
                #goats eat cabbages
                newCabbages = max( 0, info["cabbagesWest"] - Graph.goatsEatCabbages * info["goatsWest"])
                newGoats = max(0, info["goatsWest"] - Graph.wolvesEatGoats * info["wolvesWest"])
                newWolves = info["wolvesWest"]
                '''
                 #####################################
                  #####################################
                  #####################################
                '''
                newDict["cabbagesWest"] = newCabbages
                newDict["goatsWest"] = newGoats
                newDict["wolvesWest"] = newWolves
            else:
                '''
                The man is on the west shore --> calculate on the estshore
                '''
                newCabbages = max(0, info["cabbagesEst"] - Graph.goatsEatCabbages * info["goatsEst"])
                newGoats = max(0, info["goatsEst"] - Graph.wolvesEatGoats * info["wolvesEst"])
                newWolves = info["wolvesEst"]
                '''
                 #####################################
                  #####################################
                  #####################################
                '''
                newDict["cabbagesEst"] = newCabbages
                newDict["goatsEst"] = newGoats
                newDict["wolvesEst"] = newWolves
            return newDict

        '''
        if the man leave EST : generates the combinations that we can put in the store
                        WEST : generates he combinations of elem to have the desired boat
        '''
        def generateCombinationsStore(cabbagesA, cabbagesB, goatsA, goatsB, wolvesA, wolvesB, currentNode, euristic = "basic"):
            if currentNode.info["boat"] == 1:
                newCabbagesEst = currentNode.info["cabbagesEst"] - (cabbagesA + cabbagesB)
                newGoatsEst = currentNode.info["goatsEst"] - (goatsA + goatsB)
                newWolvesEst = currentNode.info["wolvesEst"] - (wolvesA + wolvesB)

                '''
                try each possibility for the store
                '''
                maxCabbageStore = min(Graph.StoreHouse, cabbagesA + cabbagesB + currentNode.info["cabbagesWest"]) # the new number on the west shore
                for nrCabbagesStore in range(maxCabbageStore + 1):
                    if nrCabbagesStore == 0:
                        maxGoatsStore = min(Graph.StoreHouse, goatsA + goatsB + currentNode.info["goatsWest"])
                    else:
                        maxGoatsStore = 0
                    for nrGoatsStore in range(maxGoatsStore + 1):
                        if nrGoatsStore == 0 and nrCabbagesStore == 0:
                            maxWolvesStore = min(Graph.StoreHouse, wolvesA + wolvesB + currentNode.info["wolvesWest"])
                        else:
                            maxWolvesStore = 0

                        for nrWolvesStore in range(maxWolvesStore + 1):
                            newCabbagesWest = cabbagesA + cabbagesB + currentNode.info["cabbagesWest"] - nrCabbagesStore
                            newGoatsWest = goatsA + goatsB + currentNode.info["goatsWest"] - nrGoatsStore
                            newWolvesWest = wolvesA + wolvesB + currentNode.info["wolvesWest"] - nrWolvesStore

                            infoBeforeEating = {"cabbagesEst" : newCabbagesEst, "goatsEst": newGoatsEst, "wolvesEst": newWolvesEst,
                                            "boat": 0,
                                            "cabbagesWest": newCabbagesWest, "goatsWest": newGoatsWest, "wolvesWest": newWolvesWest,
                                            "cabbagesStored": nrCabbagesStore, "goatsStored": nrGoatsStore, "wolvesStored": nrWolvesStore
                                              }
                            infoAfterEating = eat(infoBeforeEating, 0)

                            if not areEnoughProducts(infoAfterEating):
                                continue
                            costSuccessor = getCostSucc(cabbagesA, goatsA, wolvesA, cabbagesB, goatsB, wolvesB, currentNode.info["boat"])
                            listSuccessors.append(CrossingNode(infoAfterEating, currentNode, g = currentNode.g + costSuccessor,
                                                               h = CrossingNode.gr.calculateHNode(infoAfterEating, euristic, currentNode))
                                                  )

            else:
                newCabbagesEst = currentNode.info["cabbagesEst"] + (cabbagesA + cabbagesB)
                newGoatsEst = currentNode.info["goatsEst"] + (goatsA + goatsB)
                newWolvesEst = currentNode.info["wolvesEst"] + (wolvesA + wolvesB)

                if currentNode.info["cabbagesStored"] > 0:
                    maxCabbagesFromStore = min(currentNode.info["cabbagesStored"], cabbagesA + cabbagesB)
                    if currentNode.info["cabbagesWest"] - (cabbagesA + cabbagesB) < 0:
                        minCabbagesFromStore = (cabbagesA + cabbagesB) - currentNode.info["cabbagesWest"]
                    else:
                        minCabbagesFromStore = 0
                else:
                    maxCabbagesFromStore = 0
                    minCabbagesFromStore = 0
                for nrCabbages in range(minCabbagesFromStore, maxCabbagesFromStore + 1):
                    if currentNode.info["goatsStored"] > 0:
                        maxGoatsFromStore = min(currentNode.info["goatsStored"], goatsA + goatsB)
                        if currentNode.info["goatsWest"] - (goatsA + goatsB) < 0:
                            minGoatsFromStore = (goatsA + goatsB) - currentNode.info["goatsWest"]
                        else:
                            minGoatsFromStore = 0
                    else:
                        minGoatsFromStore = 0
                        maxGoatsFromStore = 0
                    for nrGoats in range(minGoatsFromStore, maxGoatsFromStore + 1):
                        if currentNode.info["wolvesStored"] > 0:
                            maxWolvesFromStore = min(currentNode.info["wolvesStored"], wolvesA + wolvesB)
                            if currentNode.info["wolvesWest"] - (wolvesA + wolvesB) < 0:
                                minWolvesFromStore = (wolvesA + wolvesB) - currentNode.info["wolvesWest"]
                            else:
                                minWolvesFromStore = 0
                        else:
                            minWolvesFromStore = 0
                            maxWolvesFromStore = 0
                        for nrWolves in range(minWolvesFromStore, maxWolvesFromStore + 1):
                            newCabbagesWest = currentNode.info["cabbagesWest"] - (cabbagesA + cabbagesB - nrCabbages)
                            newGoatsWest = currentNode.info["goatsWest"] - (goatsA +goatsB - nrGoats)
                            newWolvesWest = currentNode.info["wolvesWest"] - (wolvesA + wolvesB - nrWolves)

                            infoBeforeEating = {"cabbagesEst": newCabbagesEst, "goatsEst": newGoatsEst,
                                                "wolvesEst": newWolvesEst,
                                                "boat": 1,
                                                "cabbagesWest": newCabbagesWest, "goatsWest": newGoatsWest,
                                                "wolvesWest": newWolvesWest,
                                                "cabbagesStored": currentNode.info["cabbagesStored"] - nrCabbages,
                                                "goatsStored": currentNode.info["goatsStored"] - nrGoats,
                                                "wolvesStored": currentNode.info["wolvesStored"] - nrWolves
                                                }
                            infoAfterEating = eat(infoBeforeEating, 1)

                            if not areEnoughProducts(infoAfterEating):
                                continue
                            costSuccessor = getCostSucc(cabbagesA, goatsA, wolvesA, cabbagesB, goatsB, wolvesB, currentNode.info["boat"])
                            listSuccessors.append(
                                CrossingNode(infoAfterEating, currentNode, g = currentNode.g + costSuccessor,
                                             h=CrossingNode.gr.calculateHNode(infoAfterEating, euristic, currentNode))
                                )
        '''
        GenerateSuccessors calculates all the possibilities of obj that we can put in boat
        After that we will call generateCombinationsStore to find how the storeHouse looks like to have all the info about currentNode
        '''
        listSuccessors = []
        boat = currentNode.info["boat"]
        if boat == 1: #it's on initial shore(est)
            cabbagesCurrentShore = currentNode.info["cabbagesEst"]
            goatsCurrentShore = currentNode.info["goatsEst"]
            wolvesCurrentShore = currentNode.info["wolvesEst"]
        else: # we have also the obj from store house
            cabbagesCurrentShore = currentNode.info["cabbagesWest"] + currentNode.info["cabbagesStored"]
            goatsCurrentShore = currentNode.info["goatsWest"] + currentNode.info["goatsStored"]
            wolvesCurrentShore = currentNode.info["wolvesWest"] + currentNode.info["wolvesStored"]

        maxCabbagesBoat = min(cabbagesCurrentShore, Graph.A + Graph.B)
        for nrCabbagesBoat in range(maxCabbagesBoat + 1):
            if nrCabbagesBoat == 0:
                maxGoatsBoat = min(goatsCurrentShore, Graph.A + Graph.B)
            elif nrCabbagesBoat >= Graph.B and nrCabbagesBoat >= Graph.A: # we have in both A and B cabbages
                maxGoatsBoat = 0
            else:
                '''
                even if we start with some bad combinations( cheap and less products in A and more in B)
                in the end we will test and the optimised ones (cabbages(cheap) in B(expensive) and goats(expensive) in A(cheap)
                '''
                if nrCabbagesBoat <= Graph.A:
                    maxGoatsBoat = min(goatsCurrentShore, Graph.B)
                else:
                    maxGoatsBoat = min(goatsCurrentShore, Graph.A)

            for nrGoatsBoat in range(maxGoatsBoat + 1):
                if nrCabbagesBoat == 0 and nrGoatsBoat == 0:
                    maxWolvesBoat = min(wolvesCurrentShore, Graph.A + Graph.B)
                elif (nrGoatsBoat > 0 and nrCabbagesBoat > 0) or (nrGoatsBoat >= Graph.A and nrGoatsBoat >= Graph.B) or (nrCabbagesBoat >= Graph.A and nrGoatsBoat >= Graph.B): #both compartments have obj
                    maxWolvesBoat = 0
                elif nrCabbagesBoat == 0 and nrGoatsBoat > 0:
                    if nrGoatsBoat <= Graph.A:
                        maxWolvesBoat = min(wolvesCurrentShore, Graph.B)
                    else:
                        maxWolvesBoat = min(wolvesCurrentShore, Graph.A)
                elif nrCabbagesBoat > 0 and nrGoatsBoat == 0:
                    if nrCabbagesBoat <= Graph.A:
                        maxWolvesBoat = min(wolvesCurrentShore, Graph.B)
                    else:
                        maxWolvesBoat = min(wolvesCurrentShore, Graph.A)
                for nrWolvesBoat in range(maxWolvesBoat + 1):
                    if nrWolvesBoat == 0 and nrGoatsBoat == 0 and nrCabbagesBoat == 0:
                        generateCombinationsStore(0, 0, 0, 0, 0, 0, currentNode, euristic)
                    # we know that always nrCabbagesBoat + nrGoatsBoat + nrWolvesBoat <= A + B
                    # it's impossible that all three to be > 0
                    # when we have just 1 elem first of all fill A
                    if nrCabbagesBoat > 0 and nrGoatsBoat > 0:
                        if nrCabbagesBoat <= Graph.A and nrGoatsBoat <= Graph.B:
                            generateCombinationsStore(nrCabbagesBoat, 0, 0, nrGoatsBoat, 0, 0, currentNode, euristic)
                        else:
                            generateCombinationsStore(0, nrCabbagesBoat, nrGoatsBoat, 0, 0, 0, currentNode, euristic)
                    elif nrCabbagesBoat > 0  and nrWolvesBoat > 0:
                        if nrCabbagesBoat <= Graph.A and nrWolvesBoat <= Graph.B:
                            generateCombinationsStore(nrCabbagesBoat, 0, 0, 0, 0, nrWolvesBoat, currentNode, euristic)
                        else:
                            generateCombinationsStore(0, nrCabbagesBoat, 0, 0, nrWolvesBoat, 0, currentNode, euristic)
                    elif nrGoatsBoat > 0  and nrWolvesBoat > 0:
                        if nrGoatsBoat <= Graph.A and nrWolvesBoat <= Graph.B:
                            generateCombinationsStore(0, 0, nrGoatsBoat, 0, 0, nrWolvesBoat, currentNode, euristic)
                        else:
                            generateCombinationsStore(0, 0, 0, nrGoatsBoat, nrWolvesBoat, 0, currentNode, euristic)

                    elif nrCabbagesBoat > Graph.A: #JUST 1 ELEM ---> first of all fill A
                        generateCombinationsStore(Graph.A, nrCabbagesBoat - Graph.A, 0, 0, 0, 0, currentNode, euristic)
                    elif nrCabbagesBoat > 0:
                        generateCombinationsStore(Graph.A, 0, 0, 0, 0, 0, currentNode, euristic)

                    elif nrGoatsBoat > Graph.A: #JUST 1 ELEM ---> first of all fill A
                        generateCombinationsStore(0, 0, Graph.A, nrGoatsBoat- Graph.A, 0, 0, currentNode, euristic)
                    elif nrGoatsBoat > 0:
                        generateCombinationsStore(0, 0, nrGoatsBoat, 0, 0, 0, currentNode, euristic)

                    elif nrWolvesBoat > Graph.A:  # JUST 1 ELEM ---> first of all fill A
                        generateCombinationsStore(0, 0, 0, 0, Graph.A, nrWolvesBoat - Graph.A, currentNode, euristic)
                    elif nrWolvesBoat > 0:
                        generateCombinationsStore(0, 0, 0, 0, nrWolvesBoat, 0, currentNode, euristic)
        return  listSuccessors

    def  __repr__(self):
        result = ""
        for(k,v) in self.__dict__.items():
            result += "{} = {}\n".format(k, v)
        return result

def a_star(gr, nrSearchedSolutions, euristic):
    #in queue just CrossingNodes
    startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start, euristic, None))
    queue = [startNode]

    while len(queue) > 0:
        currentNode = queue.pop(0)
        #print(currentNode)
        if gr.ifScope(currentNode.info):
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

# fileName = "input.txt"
# f = open(fileName)
# lines = f.readlines()
# start = lines[0].strip().split()
# containers = lines[1].strip().split()
# eating = lines[2].strip().split()
# final = lines[3].strip().split()
#
# cabbages = int(start[0])
# goats = int(start[1])
# wolves = int(start[2])
#
#
# A = int(containers[0])
# B = int(containers[1])
# StoreHouse = int(containers[2])
#
# wolvesEatGoats = int(eating[0])
# wolvesEatWolves = int(eating[1])
# goatsEatCabbages = int(eating[2])
#
# finalCabbages = int(final[0])
# finalGoats = int(final[1])
# finalWolves = int(final[2])
gr = Graph("input.txt")
CrossingNode.gr = gr
nrSearchedSolution = 3
a_star(gr, nrSearchedSolutions = nrSearchedSolution, euristic = "basic")
# startNode = CrossingNode(gr.start, None, 0, gr.calculateHNode(gr.start, "basic", None))
# print(startNode)
# path = gr.generateSuccessors(startNode)

# path = gr.generateSuccessors(succesor)
# print(len(path))
