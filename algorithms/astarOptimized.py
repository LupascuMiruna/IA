class CrossingNode:
    def __init__(self, id, info, parent, g, h):
        self.id = id  # number in vector
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

    def showPath(self):
        path = self.getPath()
        print(("->").join(path))
        print("Cost: ", self.g)
        return len(path)

    def inPath(self, infoNewNode): #the label of the node to check
        path = self.getPath()
        for node in path:
            if node.info == infoNewNode:
                return True
        return False

    def __repr__(self):
        return "({} id = {} g= {}  f= {})".format(self.info, self.id, self.g, self.f)

class Graph:
    def __init__(self, nodes, matrix, costsMatrix, start, scopes, listH):
        self.nodes = nodes
        self.matrix = matrix
        self.costsMatrix = costsMatrix
        self.start = start
        self.scopes = scopes
        self.nrNodes = len(nodes)
        self.listH = listH

    def indexNode(self, infoNode):
        return self.nodes.index(infoNode)

    def calculateHNode(self, infoNode):
        return self.listH[self.indexNode(infoNode)]

    def generateSuccessors(self, currentNode): #generates a list of nodes
        listSuccessors = []
        for i in range(self.nrNodes):
            if self.matrix[currentNode.id][i] == 1 and not currentNode.inPath(self.nodes[i]):
                newNode = CrossingNode(i,self.nodes[i],currentNode, currentNode.g + self.costsMatrix[currentNode.id][i],
                                                   self.listH[i])
                listSuccessors.append(newNode)
        return listSuccessors

    def ifScope(self, currentNode):
        return currentNode.info in scopes;

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)

def astarOptimized(gr):
    startNode = CrossingNode(gr.indexNode(gr.start), gr.start, None, 0, gr.calculateHNode(gr.start))
    lopen = [startNode]
    lclose = []
    while len(lopen) > 0:
        currentNode = lopen.pop(0)
        lclose.append(currentNode)
        if gr.ifScope(currentNode):
            print("Solution:")
            print(currentNode.getPath())
            #-1
            #00->return
            return
        successors = gr.generateSuccessors(currentNode)
        for successor in successors:
            foundOpen = False
            for node in lopen:
                if node.info == successor.info:
                    foundOpen = True
                    if successor.f < node.f: #will eliminiate from open and then add the current node in open
                        lopen.remove(node)
                    else:
                        successors.remove(successor)
                    break
            if foundOpen == False: #will search it in lclose
                for node in lclose:
                    if successor.info == node.info:
                        if successor.f < node.f:
                            lclose.remove(node)
                        else:
                            successors.remove(successor)
                        break
            for successor in successors: # add them in lopen as we keep the order --> order ascendinf f && desc g
                foundPlace = False

                for place in range(len(lopen)):
                    if lopen[place].f > successor.f or (lopen[place].f == successor.f and lopen[place].g <= successor.g):
                        foundPlace = True
                        break
                if foundPlace == True:
                    lopen.insert(place, successor)

                else:
                    lopen.append(successor)

nodes = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k"]

matrix = [
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
costsMatrix = [
    [0, 3, 9, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 10, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 1, 0, 0, 10, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 7, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
start = "a"
scopes = ["f"]
listH = [0, 10, 3, 7, 8, 0, 14, 3, 1, 2]

gr = Graph(nodes, matrix, costsMatrix, start, scopes, listH)

astarOptimized(gr)

