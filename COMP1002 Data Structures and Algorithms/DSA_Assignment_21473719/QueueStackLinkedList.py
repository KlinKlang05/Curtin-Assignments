# Majority of code adapted from Practical 3 by Kevin Kongo

from LinkedListDEDL import DSALinkedList as LinkedList

class DSAStack():
    def __init__(self):
        self.stack = LinkedList()
    
    def isEmpty(self):
        return self.stack.head == None

    def push(self, val):
        self.stack.insertLast(val)

    def pop(self):
        topVal = self.top()
        if topVal != None:
            self.stack.removeLast()
        return topVal
    

    def top(self):
        if self.isEmpty():
            return None
        else:
            return self.stack.peekLast()
    
    def viewStack(self) -> None:
       """calling this function prints the current list. Don't print this."""
       print(self.stack)

class DSAQueue():
    def __init__(self):
        self.queue = LinkedList()
    
    def isEmpty(self):
        return self.queue.head == None
    
    def enqueue(self, val):
        self.queue.insertLast(val)

    def dequeue(self):
        frontVal = self.peek()
        if frontVal != None:
            self.queue.removeFirst()

        return frontVal
        
    def peek(self):
        if self.isEmpty():
            return None
        return self.queue.peekFirst()
    
    def viewQueue(self) -> None:
       """calling this function prints the current list. Don't print this."""
       print(self.queue)



if __name__ == "__main__":
    print('\n\n ----------------Stack test---------------- \n\n')
    myStack = DSAStack()
    myStack.push(12)
    myStack.push(13)
    myStack.push(14)
    print(myStack.isEmpty())
    print(myStack.pop())
    print(myStack.pop())
    print(myStack.pop())
    

    print('\n\n ----------------queue test---------------- \n\n')

    myQueue = DSAQueue()
    myQueue.enqueue(12)
    myQueue.enqueue(13)
    myQueue.viewQueue()
    myQueue.enqueue(14)
    myQueue.enqueue(15)
    print(myQueue.peek())
    print(myQueue.dequeue())
    myQueue.viewQueue()
    print(myQueue.peek())
    myQueue.enqueue(16)
    myQueue.viewQueue()
    print(myQueue.dequeue())
    myQueue.viewQueue()





