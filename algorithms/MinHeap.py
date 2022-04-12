inf = 10000
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

def compareNodes(node1, node2):
    if node1.f < node2.f or (node1.f == node2.f and node1.g > node2.g):
        return -1 #first one is smaller
    return 1

#toDo comparation for nodes

class MinHeap:
    def __init__(self):
        #maxsize?
        self.size = 0
        self.heap = []
        self.FRONT = 1

    def parent(self, pos): #returns the position of the parent for the child from this index
        return pos//2

    def leftChild(self, pos):
        return (2 * pos) + 1

    def rightChild(self, pos):
        return (2 * pos) + 2

    def isLeaf(self, pos):
        return 2 * pos >= self.size #has no chlilds

    def swapNodes(self, pos1, pos2): #swap 2 nodes
        self.heap[pos1], self.heap[pos2] = self.heap[pos2], self.heap[pos1]


    def heapify(self, pos):
        #if it's non-leaf and greater than any of it's child
        #descend it
        if not self.isLeaf(pos):
            leftChild = self.leftChild(pos)
            rightChild = self.rightChild(pos)
            if self.heap[pos] > self.heap[leftChild]:
                self.swapNodes(pos, leftChild)#swap the child and heapfy the child
                self.heapify(leftChild)
            else:
                if self.heap[pos] > self.heap[rightChild]:
                    self.swapNodes(pos, rightChild)
                    self.heapify(rightChild)

    def insert(self, element):
        #maxsize
        self.size += 1
        self.heap.append(element)
        if self.size > 1:
            current = self.size - 1
            #while is less than it's parent --> swap it
            while self.heap[current] < self.heap[self.parent(current)]:
                self.swapNodes(current, self.parent(current))
                current = self.parent(current)
                if current == 0:
                    return

    def remove(self):
        popped = self.heap[self.FRONT]
        self.heap[self.FRONT] = self.heap[self.size - 1] #swap it with a leaf
        self.size -= 1
        self.heapify(self.FRONT)
        return popped

    def Print(self):
        for i in range(0, (self.size//2)):
            print(" PARENT : "+ str(self.heap[i])+" LEFT CHILD : "+
                                str(self.heap[2 * i + 1])+" RIGHT CHILD : "+
                                str(self.heap[2 * i + 2]))


if __name__ == "__main__":
    print('The minHeap is ')
    minHeap = MinHeap()
    minHeap.insert(5)
    minHeap.insert(3)
    minHeap.insert(17)
    minHeap.insert(10)
    minHeap.insert(84)
    minHeap.insert(19)
    minHeap.insert(6)
    minHeap.insert(22)
    minHeap.insert(9)

    minHeap.Print()
    print("The Min val is " + str(minHeap.remove()))