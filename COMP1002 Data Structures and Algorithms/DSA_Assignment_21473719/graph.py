from __future__ import annotations
from LinkedListDEDL import DSALinkedList as LinkedList # credit: Practical 3 by Kevin Kongo
import numpy as np
from QueueStackLinkedList import DSAQueue as Queue, DSAStack as Stack


class DSAGraphVertex():
    def __init__(self, inLabel) -> None:
        self.label = inLabel
        self.links = LinkedList()
        self.linkCount = 0
        self.visited = False

    def getLabel(self):
        return self.label

    # have not included a value

    def getAdjacent(self):
        adjacent = []
        curr = self.links.head
        for x in range(self.linkCount):
            if curr != None:
                adjacent.append(curr.getValue())
                curr = curr.getNext()
        return adjacent
    
    def addEdge(self, vertex: type[DSAGraphVertex]):
        """Returns one if there were duplicate paths, otherwise returns None."""
        if vertex in self.links:
            return 1 
        else:
            self.links.insertLast(vertex)
            self.linkCount += 1

    def removeEdge(self, vertex: type[DSAGraphVertex]):
        curr = self.links.head
        while curr != None:
            if curr.getValue() == vertex:
                if self.links.remove(curr.getValue()):
                    self.linkCount -= 1
                return
            curr = curr.getNext()
        else: 
            print(f"edge with label {vertex} was not removed")
    

    def setVisited(self):
        self.visited = True

    def clearVisited(self):
        self.visited = False

    def isVisited(self):
        return self.visited

    # What the heck is toString()?


class DSAGraph():
    """Create a graph. Maximum number of vertices must be defined on initialization. No duplicate paths are allowed."""
    def __init__(self, n) -> None:
        self.maxVertex = n
        self.matrixkey = LinkedList()
        self.matrix = np.zeros(shape=(n,n), dtype=object)
        self.vertices = LinkedList()

    def addVertex(self, label):
        if self.getVertexCount() == self.maxVertex:
            print('max number of vertices reached. max is ', self.getVertexCount())
        else:
            val = DSAGraphVertex(label)
            self.vertices.insertLast(val)
            
            self.matrixkey.insertLast(label)

    def addEdge(self, label1, label2): 
        """Links label1 to label2.
        Returns 1 if any label could not be found. Otherwise, returns 0."""
        curr = self.vertices.head
        retval = None

        for x in range(self.vertices.length):
            currval = curr.getValue()
            if currval.getLabel() == label1:
                curr2 = self.vertices.head

                for y in range(self.vertices.length):
                    currval2 = curr2.getValue()
                    if currval2.getLabel() == label2:
                        if currval.addEdge(currval2) != 1 and currval2.addEdge(currval) != 1:
                            self.matrix[self.matrixkey.index(label1)][self.matrixkey.index(label2)] += 1
                            self.matrix[self.matrixkey.index(label2)][self.matrixkey.index(label1)] += 1
                        retval = 0 
                    else: 
                        curr2 = curr2.getNext()
            else:
                curr = curr.getNext()
            
        else:
            if retval == None:
                print("could not find labels.")
                retval = 1 

        return retval
    
    def deleteEdge(self, label1, label2):
        curr = self.vertices.head

        for x in range(self.vertices.length):
            if curr.getValue().getLabel() == label1:
                curr2 = self.vertices.head
                for y in range(self.vertices.length):
                    if curr2.getValue().getLabel() == label2:
                        curr.getValue().removeEdge(curr2.getValue())
                        curr2.getValue().removeEdge(curr.getValue())

                        temp = self.matrix[self.matrixkey.index(label1)][self.matrixkey.index(label2)]
                        if temp > 0:
                            temp -= 1
                            self.matrix[self.matrixkey.index(label2)][self.matrixkey.index(label1)] -= 1
                        return
                    else: 
                        curr2 = curr2.getNext()
            else:
                curr = curr.getNext()
        
        else: 
            return 1
            # print('could not find labels. ')

    def deleteVertex(self, label):
        curr = self.vertices.head
        for x in range(self.vertices.length):
            if label == curr.getValue().getLabel():
                l = curr.getValue().getAdjacent()
                for vertex in l:
                    # print(vertex.getLabel())
                    # print(curr.getValue().getLabel())
                    vertex.removeEdge(curr.getValue())
                self.vertices.remove(curr.getValue())

                temp = self.matrix[self.matrixkey.index(label)]
                for i in range(len(temp)):
                    temp[i] = 0
                    self.matrix[i][self.matrixkey.index(label)] = 0
                self.matrixkey.remove(label)

                return
            else: 
                curr = curr.getNext()
        else:
            print('label was not found. ')

    def hasVertex(self, label):
        cond = False
        curr = self.vertices.head
        for x in range(self.vertices.length):
            if curr.getValue().getLabel() == label:
                cond = True
            curr = curr.getNext()
        return cond
    
    def getVertexCount(self):
        return self.vertices.length
    
    def getEdgeCount(self): # TO DO 

        return 1 
    
    def isAdjacent(self, label1, label2): # TO DO

        return True
    
    def getEdges(self, label) -> LinkedList:
        """Returns all nodes that are adjecent to the given node, as a linked list of labels."""
        curr = self.vertices.head
        for x in range(self.vertices.length):
            if curr != None:
                if curr.getValue().getLabel() == label:
                    output = LinkedList()
                    for item in curr.getValue().links:
                        output.insertLast(item.getLabel())
                    return output 
            curr = curr.getNext()
        
        else:
            print("Node was not found.")
    
    def displayAsList(self):
        curr = self.vertices.head
        for x in range(self.vertices.length):
            if curr != None:
                sub_curr = curr.getValue().links.head
                print(curr.getValue().getLabel(), end=": ")
                for b in range(curr.getValue().links.length):
                    if sub_curr == None:
                        print("", end="")
                    else:
                        print(sub_curr.getValue().getLabel(), end=" ")
                        sub_curr = sub_curr.getNext()
                
                print()
                curr = curr.getNext()
    
    def displayAsMatrix(self):
        print("Adjacency matrix: ")
        print(" ", end=" ")
        for count in range(len(self.matrix)):
            if count > self.matrixkey.length - 1:
                print('_', end=" ")
            else:
                print(self.matrixkey[count], end=" ")
        print()
        for c1, i in enumerate(self.matrix):
            if c1 > self.matrixkey.length - 1:
                print('_', end=" ")
            else:
                print(self.matrixkey[c1], end=" ")
            for z in i:
                print(z, end=" ")
            print()
        print()

    def breadthFirstSearch(self, start=None) -> LinkedList:
        T = Queue()
        Q = Queue()

        for v in self.vertices:
            v.clearVisited()

        v = None
        if start == None:
            v = self.vertices.head.getValue()
        else:
            for node in self.vertices:
                if node.getLabel() == start:
                    v = node
            else:
                if v == None:
                    # print("Starting node was not found. ")
                    return None

        v.setVisited()
        Q.enqueue(v)
        while not Q.isEmpty():
            v = Q.dequeue()
            for x in range(len(v.getAdjacent())):
                lowest_alphabet = None
                for w in v.getAdjacent():
                    if not w.isVisited():
                        if lowest_alphabet == None:
                            lowest_alphabet = w
                        elif w.getLabel() < lowest_alphabet.getLabel():
                            lowest_alphabet = w 

                if lowest_alphabet != None:
                    T.enqueue(v)
                    T.enqueue(lowest_alphabet)
                    lowest_alphabet.setVisited()
                    Q.enqueue(lowest_alphabet)
        
        # print('printing search: ')
        vertex = T.dequeue()
        searchOut = LinkedList()
        while vertex != None:
            searchOut.insertLast(vertex.getLabel())
            vertex = T.dequeue()
            
        # print(searchOut)
        return searchOut

    def depthFirstSearch(self, start=None) -> LinkedList:
        T = Queue()
        S = Stack()

        for v in self.vertices:
            v.clearVisited()
    
        v = None
        if start == None:
            v = self.vertices.head.getValue()
        else:
            for node in self.vertices:
                if node.getLabel() == start:
                   v = node
            else:
                if v == None:
                    # print("Starting node was not found. ")
                    return None
                

        v.setVisited()
        S.push(v)
        while not S.isEmpty(): 
            while any([not x.isVisited() for x in v.getAdjacent()]):
                w = [w for w in v.getAdjacent() if not w.isVisited()]
                lowest_alphabet = None
                for z in w:
                    if lowest_alphabet == None:
                        lowest_alphabet = z
                    elif z.getLabel() < lowest_alphabet.getLabel():
                        lowest_alphabet = z 
                T.enqueue(v)
                T.enqueue(lowest_alphabet)
                lowest_alphabet.setVisited()
                S.push(lowest_alphabet)
                v = lowest_alphabet
            v = S.pop()

        # print('printing search: ')
        vertex = T.dequeue()
        searchOut = LinkedList()
        while vertex != None:
            searchOut.insertLast(vertex.getLabel())
            vertex = T.dequeue()
            
        # print(searchOut)
        return searchOut





if __name__ == "__main__":
    pass

