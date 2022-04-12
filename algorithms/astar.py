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
                listSuccessors.append(CrossingNode(i,self.nodes[i],currentNode, currentNode.g + self.costsMatrix[currentNode.id][i],
                                                   self.listH[i]))
        return listSuccessors

    def ifScope(self, currentNode):
        for scope in scopes:
            if scope == currentNode.info:
                return True
        return False

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def astar(gr, nrSearchedSolutions):
    startNode = CrossingNode(gr.indexNode(gr.start), gr.start, None, 0, gr.calculateHNode(gr.start))
    queue = [startNode]

    while len(queue) > 0:

        currentNode = queue.pop(0)
        if gr.ifScope(currentNode):
            print("Solution:")
            print(currentNode.getPath())
            nrSearchedSolutions -= 1
            if nrSearchedSolutions == 0:
                return
        successors = gr.generateSuccessors(currentNode)
        for successor in successors:
            foundPlace = False
            for i in range(len(queue)):
                if successor.f < queue[i].f: #will eliminiate from open and then add the current node in open
                   foundPlace = True
                   break
            if foundPlace == True:
                queue.insert(i, successor)
            else:
                queue.append(successor)



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
# exemplu de euristica banala (1 daca nu e nod scop si 0 daca este)
listH = [0, 10, 3, 7, 8, 0, 14, 3, 1, 2]

gr = Graph(nodes, matrix, costsMatrix, start, scopes, listH)
#print(gr)
astar(gr, 2)

