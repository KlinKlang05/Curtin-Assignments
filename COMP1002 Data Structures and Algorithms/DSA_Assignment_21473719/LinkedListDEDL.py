from __future__ import annotations

class _DSAListNode():
    def __init__(self, inValue:object) -> None:
        self.value = inValue
        self.next = None
        self.prev = None
        
        
    def getValue(self):
        return self.value
    
    def setValue(self, inValue: object):
        self.value = inValue

    # Next Node
    def getNext(self):
        return self.next
    
    def setNext(self, newNext: type[_DSAListNode]):
        self.next = newNext
        
    # Previous Node
    def getPrev(self):
        return self.prev
    
    def setPrev(self, newPrev: type[_DSAListNode]):
        self.prev = newPrev


class DSALinkedList():
    def __init__(self, *entries:object) -> None:
        self.head = None # head points to the first value in the list 
        self.tail = None
        self.length = 0
        if len(entries) > 0:
            for arg in entries:
                self.insertLast(arg)
    
    def remove(self, value):
        removed = False
        curr = self.head
        while curr != None:
            if curr.getValue() == value:
                if curr.getPrev() == None:
                    self.head = curr.getNext()
                else:
                    curr.getPrev().setNext(curr.getNext())
                if curr.getNext() == None:
                    self.tail = curr.getPrev()
                else:
                    curr.getNext().setPrev(curr.getPrev())
                
                removed = True
                self.length -= 1
            
            curr = curr.getNext()

        return removed

    def insertFirst(self, newValue: object):
        newNd = _DSAListNode(newValue) # create the new node
        if self.isEmpty():
            self.head = newNd # First value in the list, head points to it
            self.tail = newNd # And tail, since it's the front and the back
        else: 
            newNd.setNext(self.head) # not first value, sets new node to point to current first node
            self.head.setPrev(newNd)    
            self.head = newNd # Then point head to new node.
        
        self.length += 1

    def insertLast(self, newValue: object):
        newNd = _DSAListNode(newValue)
        if self.isEmpty():
            self.tail = newNd
            self.head = newNd
        else:
            newNd.setPrev(self.tail)
            self.tail.setNext(newNd)
            self.tail = newNd
        
        self.length += 1

    def isEmpty(self):
        empty = self.head == None
        return empty

    def peekFirst(self) -> object:
        if self.isEmpty():
            nodeValue = None
        else:
            nodeValue = self.head.getValue()
        return nodeValue
    
    def peekLast(self) -> object:
        if self.isEmpty():
            nodeValue = None
        else:
            nodeValue = self.tail.getValue()
        
        return nodeValue
    
    def removeFirst(self):
        if self.isEmpty():
            nodeValue = None
        elif self.head == self.tail: # Only one item in the list
            nodeValue = self.head.getValue()
            self.head = None
            self.tail = None
        elif self.head.getNext() == self.tail: # Two items in the list
            nodeValue = self.head.getValue()
            self.tail.setPrev(None)
            self.head = self.tail
        else:                   # Greater than two items in the list 
            nodeValue = self.head.getValue()
            newFront = self.head.getNext()
            newFront.setPrev(None)
            
            self.head = newFront
        
        self.length -= 1
        
        return nodeValue
    
    def removeLast(self):
        if self.isEmpty():
            nodeValue = None
        elif self.tail == self.head: # Only one item in the list
            nodeValue = self.tail.getValue()
            self.head = None
            self.tail = None
        elif self.tail.getPrev() == self.head: # Two items in the list
            nodeValue = self.tail.getValue()
            self.head.setNext(None)
            self.tail = self.head
        else:                   # Greater than two items in the list 
            nodeValue = self.tail.getValue()
            newLast = self.tail.getPrev()
            newLast.setNext(None)

            self.tail = newLast

        self.length -= 1
        
        return nodeValue

    def __str__(self):
        """Printing an instance of this class will reveal the contents of the linked list."""
        curr = self.head
        list_out = ""
        while curr != None:
            if curr.getNext() is None:
                suffix = ""
            else:
                suffix = ", "
        
            list_out += str(curr.getValue()) + suffix
            curr = curr.getNext()
        
        return list_out


    def __getitem__(self, index): 
        """Allow for indexing of the class instance, which will return the relevant value from the linked list."""
        curr = self.head
        if curr == None:
            raise IndexError("Index out of range.")
        for x in range(index):
            curr = curr.getNext()
            if curr == None: 
                raise IndexError("Index out of range.")
        return curr.getValue()
    
    def __setitem__(self, index, value):
        curr = self.head
        for x in range(index):
            curr = curr.getNext()
            if curr == None: 
                raise IndexError("Index out of range.")
        curr.value = value
        #return curr.getValue()

    def __iter__(self):
        self.currentIter = self.head
        return self
    
    def __next__(self):
        temp = self.currentIter
        if temp != None:
            self.currentIter = temp.getNext()
            return temp.getValue()
        else:
            raise StopIteration
        
    def index(self, val):
        curr = self.head 
        exitCondition = False
        count = 0
        while curr != None and not exitCondition:
            if curr.getValue() == val:
                exitCondition = True
            else: 
                curr = curr.getNext()
                count += 1
        else:
            if not exitCondition:
                raise ValueError(f'{val} is not in Linked List')
            
        return count

                



if __name__ == "__main__":
    linked = DSALinkedList()
    linked.insertFirst(12)
    linked.insertLast(15)
    print(linked.peekFirst())
    linked.insertFirst(124)
    print(linked.peekFirst())
    print(linked)
    print(linked[0])
    linked[0] = 69
    print(linked)