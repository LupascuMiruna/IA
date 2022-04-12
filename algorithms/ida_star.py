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

def ida_star(gr, nrSearchedSolutions):
    startNode = CrossingNode(gr.indexNode(gr.start), gr.start, None, 0, gr.calculateHNode(gr.start))
    limit = startNode.f
    while True: #while we are in the limit and still haven't find the nr of solutions

        nrSearchedSolutions, result = buildPath(gr, startNode, limit, nrSearchedSolutions)
        if result == "finished":
            break
        if result == float('inf'):
            print("No more solutions")
            break
        limit = result


def buildPath(gr, currentNode, limit, nrSearchedSolutions):
    if currentNode.f > limit: #we can not extend this node
        return nrSearchedSolutions, currentNode.f #the new limit --> will choose the highest from all
    if gr.ifScope(currentNode) and currentNode.f == limit:
        print("Solution:")
        print(currentNode.getPath())
        nrSearchedSolutions -= 1
        if nrSearchedSolutions == 0:
            return 0, "finished"
    successors = gr.generateSuccessors(currentNode)
    minim = float('inf')
    for successor in successors: #try to extend every child
        nrSearchedSolutions, result = buildPath(gr, successor, limit, nrSearchedSolutions)
        if result == "finished":
            return 0, "finished" #to go back at the initial call
        if result < minim:
            minim = result #calculate the minim of all limits
    return nrSearchedSolutions, minim


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
listH = [5, 10, 3, 7, 8, 0, 14, 3, 1, 2]

gr = Graph(nodes, matrix, costsMatrix, start, scopes, listH)
#print(gr)
ida_star(gr, 3)


