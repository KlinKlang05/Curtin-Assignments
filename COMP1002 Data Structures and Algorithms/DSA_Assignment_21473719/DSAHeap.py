import numpy as np      
import numpy.typing as npt
import csv

class DSAHeapEntry():
    def __init__(self, priority:int, value:object) -> None:
        self.priority = priority
        self.value = value

    def getPriority(self):
        return self.priority
    
    def setPriority(self, priority):
        self.priority = priority

    def getValue(self):
        return self.value
    
    def setValue(self, value:object):
        self.value = value


class DSAHeap():
    """Ensure that you specify the sizeInit argument if using the heap for anything other than sorting.
    If using DSAHeap to sort, sizeInit does not need to be specified. It will default to 3, then resize when the input array size is calculated."""
    def __init__(self, sizeInit=3) -> None:
        self.count = 0 
        self.heapArray = np.empty(sizeInit+1, dtype=DSAHeapEntry)

    def add(self, priority:int, value:object):
        if self.count == self.heapArray.size:
            print("Heap is full!")
        else:
            entry = DSAHeapEntry(priority, value)
            self.heapArray[self.count] = entry
            self._trickleUp(self.count)
            self.count += 1 

    def remove(self) -> DSAHeapEntry:
        root = None
        if self.count == 0: 
            print("Heap is currently empty.")
        else:
            self.count -= 1
            root = self.heapArray[0]
            if self.count != 1:
                self.heapArray[0] = self.heapArray[self.count]
                self.heapArray[self.count] = None
                self._trickleDown(0) 
            else:
                self.heapArray[0] = None 

        return root 

    def display(self):
        count = 0
        item = self.heapArray[count]
        while item != None: 
            print(str(count) + ": Priority is: " + str(item.getPriority()) + ", Value is: " + str(item.getValue())) # This line requires knowing the type of the value object otherwise you can't print the value. 
            count += 1 
            item = self.heapArray[count]

        print()

    def _heapify(self, inArray:np.array, numItems:int) -> np.array:
        if not isinstance(inArray[0], DSAHeapEntry): # This will not be done if imported by a CSV, as that automatically converts the values in the array into type DSAHeapEntry and puts them into the heap.
            self.heapArray = np.empty(numItems+1, dtype=DSAHeapEntry)
            for c, value in enumerate(inArray):
                self.heapArray[c] = DSAHeapEntry(value, value)
        
        for ii in range((numItems//2) - 1, -1, -1):
            self._trickleDown(ii, numItems)
    
    def heapSort(self, arr:np.array, numItems:int) -> npt.NDArray: # haven't handled case where numItems is not equal to the size of imported array
        """numItems should be the number of elements in the array."""
        self._heapify(arr, numItems)
        for ii in range(numItems-1, 0, -1):
            temp = self.heapArray[0]
            self.heapArray[0] = self.heapArray[ii]
            self.heapArray[ii] = temp
            self._trickleDown(0, ii)
        outArray = np.empty(numItems, dtype=object)
        for c, item in enumerate(self.heapArray):
            if item != None:
                outArray[c] = item.getValue()
        return outArray
        
            
    def _trickleUp(self, index):
        parentIdx = (index-1)//2
        if index > 0:
            if self.heapArray[index].getPriority() > self.heapArray[parentIdx].getPriority():
                temp = self.heapArray[parentIdx]
                self.heapArray[parentIdx] = self.heapArray[index]
                self.heapArray[index] = temp
                self._trickleUp(parentIdx)
                

    def _trickleDown(self, index, numItems=None):
        if numItems is None: 
            numItems = self.count
        lChildIdx = index * 2 + 1
        rChildIdx = lChildIdx + 1

        if lChildIdx < numItems:
            largeIdx = lChildIdx
            if rChildIdx < numItems:
                if self.heapArray[lChildIdx].getPriority() < self.heapArray[rChildIdx].getPriority():
                    largeIdx = rChildIdx
            if self.heapArray[largeIdx].getPriority() > self.heapArray[index].getPriority():
                temp = self.heapArray[largeIdx]
                self.heapArray[largeIdx] = self.heapArray[index]
                self.heapArray[index] = temp
                self._trickleDown(largeIdx, numItems)

    def SortCSV(self, file, size):
        """Ensure size is the amount of entries in your CSV. col 1: priority, col 2: Value"""
        importArray = np.empty(size, dtype=DSAHeapEntry)
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for c, row in enumerate(reader):
                importArray[c] = DSAHeapEntry(int(row[0]), row[1])

        self.heapArray = importArray

        self.heapSort(importArray, size) 


if __name__ == "__main__":
    # heap = DSAHeap(10)
    # heap.add(1, 'a')
    # heap.add(2, 'b')
    # heap.add(3, 'c')
    # heap.add(4, 'd')
    # heap.add(8, 'e')
    # heap.add(6, 'f')
    # heap.add(2, 'g')
    # heap.display()
    # print("removed: " + str(heap.remove().getPriority()))
    # heap.display()
    heap2 = DSAHeap()
    # heap2.SortCSV('RandomNames.csv', 7000)
    # heap2.display()
    arr = np.array([3,4,5,1,5,2,1])
    out = heap2.heapSort(arr,arr.size)
    print(out)