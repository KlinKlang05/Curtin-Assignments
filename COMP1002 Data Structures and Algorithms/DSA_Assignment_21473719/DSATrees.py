from LinkedListDEDL import DSALinkedList as LinkedList # imported code taken from Practical 4 work by Kevin Kongo 21473719 

class DSATreeNode():
    def __init__(self, inKey, inValue) -> None:
        self._key = inKey
        self._value = inValue
        self._left = None
        self._right = None

    def __str__(self):
        return ("Key: " + str(self._key) + " Value: " + str(self._value))
    
    def setLeft(self, inNode):
        self._left = inNode

    def getValue(self):
        return self._value

    def setRight(self, inNode):
        self._right = inNode

class DSABinarySearchTree(): 
    def __init__(self):
        self.root = None

    def find(self, key):
        """Returns a DSATreeNode class instance. To get the value from the node, call getValue() on the returned object.
        Raises ValueError if no value was found. """
        result = self._findrec(key, self.root)
        return result

    def _findrec(self, key, cur: DSATreeNode):
        value = None
        if cur == None:
            raise ValueError("Key " + str(key) + " not found")

        elif key == cur._key:
            value = cur

        elif key < cur._key:
            value = self._findrec(key, cur._left)

        else: 
            value = self._findrec(key, cur._right)

        return value

    def insert(self, key, value): 
        self.root = self._insertrec(key, value, self.root)

    def _insertrec(self, key, data, cur: DSATreeNode):
        updateNode = cur
        if cur == None:
            newNode = DSATreeNode(key, data)
            updateNode = newNode

        elif key == cur._key:
            pass
        elif key < cur._key:
            cur.setLeft(self._insertrec(key, data, cur._left))
        else:
            cur.setRight(self._insertrec(key, data, cur._right))

        return updateNode
        
    def delete(self, key):
        self._deleteRec(key, self.root)

    def deletenode(self, key, delNode: DSATreeNode):
        updatenode = None
        if delNode._left == None and delNode._right == None:
            updatenode = None
        elif delNode._left != None and delNode._right == None:
            updatenode = delNode._left
        elif delNode._left == None and delNode._right != None:
            updatenode = delNode._right
        else:
            updatenode = self._promoteSuccessor(delNode._right)
            if updatenode != delNode._right:
                updatenode.setRight(delNode._right)
            updatenode.setLeft(delNode._left)

        return updatenode

    def _promoteSuccessor(self, cur: DSATreeNode):
        successor = cur

        if cur._left != None:   
            successor = self._promoteSuccessor(cur._left)
            if successor == cur._left:
                cur.setLeft(successor._right) 

        return successor


    def _deleteRec(self, key, cur: DSATreeNode):
        updatenode = cur
        if cur == None:
            pass
        elif key == cur._key:
            updatenode = self.deletenode(key, cur)
        elif key < cur._key: 
            cur.setLeft(self._deleteRec(key, cur._left))
        elif key > cur._key: 
            cur.setRight(self._deleteRec(key, cur._right))

        return updatenode

    def _minRec(self, curNode):
        if (curNode._left != None): 
            minKey = self._minRec(curNode._left) 
        else:
            minKey = curNode._key
        return minKey

    def _maxRec(self, curNode: DSATreeNode):
        if (curNode._right != None): 
            maxKey = self._maxRec(curNode._right) 
        else:
            maxKey = curNode._key
        return maxKey
    
    def max(self):
        return self._maxRec(self.root)
    
    def min(self):
        return self._minRec(self.root)

    def height(self):
        return self._heightRec(self.root)
    
    def _heightRec(self, curNode: DSATreeNode):
        leftHt = 0
        rightHt = 0
        if curNode == None: 
            htSoFar = -1
        else:
            print(curNode._key)
            leftHt = self._heightRec(curNode._left) 
            rightHt = self._heightRec(curNode._right) 
        if leftHt > rightHt:
            htSoFar = leftHt + 1
        else:
            htSoFar = rightHt + 1
        return htSoFar
    
    def balance(self):
        diff = self._heightRec(self.root._right) / self._heightRec(self.root._left)
        print(f"ratio of the right side of tree to the left side is {diff}")

    def _displayInRec(self, cur: DSATreeNode, output:LinkedList=None):
        if cur == None:
            return

        self._displayInRec(cur._left, output)
        
        if output != None:
            output.insertLast(cur._value)
        else:
            print(cur._key, end=" ")

        self._displayInRec(cur._right, output)

    def _displayPreRec(self, cur: DSATreeNode):
        if cur == None:
            return
        
        print(cur._key, end=" ")
        self._displayPreRec(cur._left)
        self._displayPreRec(cur._right)

    def _displayPostRec(self, cur: DSATreeNode):
        if cur == None:
            return
        
        self._displayPostRec(cur._left)
        self._displayPostRec(cur._right)
        print(cur._key, end=" ")

    def displayInOrder(self):
        print("Displaying Tree In order Traversal: ", end="")
        self._displayInRec(self.root)

    def getInOrder(self):
        """Allows the in-order traversal to be returned as a linked list of the values in each node"""
        self.out = LinkedList()
        self._displayInRec(self.root, self.out)
        return self.out 

    def displayPreOrder(self):
        print("Displaying Tree Pre order Traversal: ", end="")
        self._displayPreRec(self.root)

    def displayPostOrder(self):
        print("Displaying Tree Post order Traversal: ", end="")
        self._displayPostRec(self.root)
