from queue import Queue

class CrossingNode():
    def __init__(self, id, info, parent):
        self.id = id #number in vector
        self.info = info #the label ot the node
        self.parent = parent

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

    # def __repr__(self):
    #     str = "({} id = {} path = {})".format(self.info, self.id, self.getPath())
    #     return str
    def __repr__(self):
        return "({} id = {})".format(self.info, self.id)


class Graph:
    def __init__(self, nodes, matrix, start, scopes):
        self.nodes = nodes
        self.matrix = matrix
        self.start = start
        self.scopes = scopes
        self.nrNodes = len(nodes)

    def indexNode(self, infoNode):
        return self.nodes.index(infoNode)

    def generateSuccessors(self, currentNode): #generates a list of nodes
        listSuccessors = []
        for i in range(self.nrNodes):
            if self.matrix[currentNode.id][i] == 1 and not currentNode.inPath(self.nodes[i]):
                listSuccessors.append(CrossingNode(i,self.nodes[i],currentNode))
        return listSuccessors

    def ifScope(self, currentNode):
        for scope in scopes:
            if scope == currentNode.info:
                return True
        return False

    def __repr__(self):
        str = ""
        for(k, v) in self.__dict__.items():
            str += "{} = {}\n".format(k, v)
        return str

def BF(gr, nrSearchedSolutions = 1):
    startNode = CrossingNode(gr.indexNode(gr.start), gr.start, None)
    queueNodes = [startNode]
    while len(queueNodes) != 0:
        print("Actual queue: " + str(queueNodes))
        currentNode = queueNodes.pop()
        if(gr.ifScope(currentNode)):
            print("Solution:")
            print(currentNode.getPath())
            nrSearchedSolutions -= 1
            if nrSearchedSolutions == 0:
                return
        succesors = gr.generateSuccessors(currentNode)
        queueNodes.extend(succesors)

def DF(currentNode, nrSearchedSolutions = 1):
    startNode = CrossingNode(gr.indexNode(gr.start), gr.start, None)
    stackNodes = [startNode]
    if gr.ifScope(currentNode):
        print("Solution:")
        print(currentNode.getPath())
        nrSearchedSolutions -= 1
        if nrSearchedSolutions == 0:
            return nrSearchedSolutions
    successors = gr.generateSuccessors(currentNode)
    for successor in successors:
        if nrSearchedSolutions != 0:
            nrSearchedSolutions = DF(successor, nrSearchedSolutions)
    return nrSearchedSolutions

def depth_first_iterative(currentNode, depth, nrSearchedSolutions = 1):
    if depth == 1 and gr.ifScope(currentNode):  #at the last step for the current searched depth
        print("Solution:")
        print(currentNode.getPath())
        nrSearchedSolutions -= 1
        if nrSearchedSolutions == 0:
            return nrSearchedSolutions
    if depth > 1:
        succesors = gr.generateSuccessors(currentNode)
        for succesor in succesors:
            if nrSearchedSolutions != 0:
                nrSearchedSolutions = depth_first_iterative(succesor, depth - 1, nrSearchedSolutions)
    return nrSearchedSolutions

# dfs but with a maximum depth --> combination with bfs
# it will remake all the previous trees but at least we will not have problems with the memory
def DFI(gr, nrSearchedSolutions):
    for depth in range(1, gr.nrNodes + 1): #the maximum length
        if nrSearchedSolutions == 0: #at the previous call we have finished all the the searches
            return
        print("Maximum depth:", depth)
        startNode = CrossingNode(gr.indexNode(gr.start), gr.start, None)
        nrSearchedSolutions = depth_first_iterative(startNode, depth, nrSearchedSolutions)



nodes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

matrix = [
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

start = "a"
scopes = ["f", "j"]
gr = Graph(nodes, matrix, start, scopes)
startNode =CrossingNode(gr.indexNode(gr.start), gr.start, None)
# print(gr.generateSuccessors(startNode))

DFI(gr,4)