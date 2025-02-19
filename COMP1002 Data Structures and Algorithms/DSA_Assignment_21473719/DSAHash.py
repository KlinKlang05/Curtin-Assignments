from LinkedListDEDL import DSALinkedList as LinkedList
from QueueStackLinkedList import DSAQueue as Queue, DSAStack as Stack
import numpy as np 
import math
import csv                                                                                                                                                                         

class _DSAHashEntry():
    def __init__(self) -> None:
        self.key = str
        self.value = object
        self.state = 0

class DSAHashTable(): # This hash table class uses Open Addressing instead of Seperate Chaining 
    """If importing values from a CSV, ensure the initial tableSize value is not much larger than the size of the CSV.
    The Table will not downsize until importing is finished."""
    def __init__(self, tableSize) -> None:
        self.actualSize = self._nextPrime(tableSize)
        self.hashArray = np.empty(self.actualSize, dtype=_DSAHashEntry)
        for ii in range(self.actualSize):
            self.hashArray[ii] = _DSAHashEntry()
        self.count = 0
        self.suppressDownsize = False
        self.ignoreResizeCheck = False     # any better way of doing this?

    def get(self, inKey, printResult=True):
        "Returns -1 if the specified Key was not found. Otherwise Returns the value associated with the key."

        stepSize = self._stepHash(inKey)
        hashIdx = self._hash(inKey)
        origIdx = hashIdx 
        found = False
        giveUp = False
        retVal = -1

        while not found and not giveUp:
            if self.hashArray[hashIdx] == None:
                giveUp = True
            elif self.hashArray[hashIdx].state == 0: 
                giveUp = True
            elif self.hashArray[hashIdx].key == inKey and self.hashArray[hashIdx].state != -1:
                found = True
            else: 
                hashIdx = (hashIdx + stepSize) % self.actualSize
                if hashIdx == origIdx:
                    giveUp = True

        if not found:
            if printResult:
                print('The specified key was not found! Please try again.')
        else: retVal = self.hashArray[hashIdx].value

        return retVal
    
    def put(self, inKey: str, inValue: object):

        hashIdx = self._hash(inKey)
        stepSize = self._stepHash(inKey)
        entry = _DSAHashEntry()
        entry.key = inKey
        entry.value = inValue
        exit_state = False
        duplicate_found = False

        while not exit_state:
            if self.hashArray[hashIdx] != None:
                if self.hashArray[hashIdx].state != 1:
                   exit_state = True
                elif self.hashArray[hashIdx].key == inKey:      # Checks for duplicates already in the hash table by comparing initial keys.
                    print(f"The Key {inKey} is already in the in the hash table. It will not be added again.")
                    exit_state = True
                    duplicate_found = True
                else:
                    hashIdx = (hashIdx + stepSize) % self.actualSize  # I'm not sure about this method of wrapping. Should I be updating 
            else:                                                     # hashIdx to always stay within the size of the array or keep that 
                exit_state = True                                     # variable seperate to ensure hashIdx always goes up by correct step

        if not duplicate_found:
            self.hashArray[hashIdx] = entry
            self.hashArray[hashIdx].state = 1
            self.count += 1

        if not self.ignoreResizeCheck:
            self._resizeCheck()

    def remove(self, inKey):
        
        hashIdx = self._hash(inKey)
        stepSize = self._stepHash(inKey)
        exit_state = False
        error_state = False

        while not exit_state and not error_state:
            if self.hashArray[hashIdx] != None:
                if self.hashArray[hashIdx].state == 1:
                    if self.hashArray[hashIdx].key == inKey:
                        exit_state = True 
                    else: 
                        hashIdx = (hashIdx + stepSize) % self.actualSize
                elif self.hashArray[hashIdx].state == -1: 
                    hashIdx = (hashIdx + stepSize) % self.actualSize
                elif self.hashArray[hashIdx].state == 0:
                    error_state = True
            else:
                error_state = True

        if error_state:
            print("Key could not be found and was not removed!")
        else:
            self.hashArray[hashIdx].state = -1
            self.count -= 1
        
        if self.count != 0:
            self._resizeCheck()

    def getLoadFactor(self):
        LF = self.count/self.actualSize
        return LF

    def CSVImport(self, filename):
        """Imports the contents of a CSV into the hashtable. format must be key, value"""
        with open(filename, 'r') as csvfile:
            self.suppressDownsize = True
            reader = csv.reader(csvfile)
            for row in reader:
                self.put(row[0], row[1])
            self.suppressDownsize = False

    def printAll(self, keyOnly=False):
        c = 0
        for entry in self.hashArray:
            if entry != None:
                if entry.state == 1:
                    if keyOnly:
                        print(entry.key)
                    else:
                        print(str(c) + ": " + entry.key + " -> " + entry.value) # HOW do I avoid repitition between these two functions?? They're basically the same code..

            c += 1           

    def export(self):
        c = 0
        with open("DSAHashExport.csv", 'a') as f:
            for entry in self.hashArray:
                if entry != None:
                    if entry.state == 1:
                        f.write(str(c) + "," + entry.key + "," + entry.value + "\n")
                c += 1

    def _resizeCheck(self): # wrapper code for _resize.
        exit_state = False

        while not exit_state:
            if self.suppressDownsize == False and self.getLoadFactor() < 0.2:
                self.actualSize = self._nextPrime(int(self.count * 2))
                self._resize()
            else: 
                exit_state = True

            if self.getLoadFactor() > 0.55:
                self.actualSize = self._nextPrime(self.actualSize)
                self._resize()
                exit_state = False

    def _resize(self):
        self.ignoreResizeCheck = True
        old_arr = self.hashArray
        self.hashArray = np.empty(self.actualSize, dtype=_DSAHashEntry)
        self.count = 0
        for entry in old_arr:
            if entry != None:
                if entry.state == 1:
                    self.put(entry.key, entry.value)
        
        self.ignoreResizeCheck = False

    def _hash(self, inKey): # Taken from slide 28 of the lecture 7 slides as suggested in the practical sheet
        a = 63689
        b = 378551
        hashIdx = 0

        for ii in range(len(inKey)):
            hashIdx = (hashIdx * a) + ord(inKey[ii])
            a *= b

        return hashIdx % self.actualSize
    
    def _stepHash(self, inKey):
        MAX_STEP = self.actualSize // 2
        return MAX_STEP - (sum(map(ord,inKey)) % MAX_STEP)

    def _nextPrime(self, startVal):
        if startVal % 2 == 0: 
            primeVal = startVal - 1 
        else:
            primeVal = startVal 

        isprime = False 
        while not isprime:
            primeVal = primeVal + 2
            ii = 3 
            isprime = True
            rootVal = math.sqrt(primeVal)
            while ii <= rootVal and isprime:
                if primeVal % ii == 0:
                    isprime = False
                else:
                    ii = ii + 2

        return primeVal
    


if __name__ == "__main__":
    table = DSAHashTable(3)

    table.put('21473719', "Kevin Kongo")
    table.put('214737191', "Kevin Kongo")
    table.put('214737192', "Kevin Kongo")
    table.put('214737193', "Kevin Kongo")
    table.put('214737194', "Kevin Kongo")
    print(table.count)
    print(table.actualSize)
    # table.CSVImport("RandomNames.CSV")
    
    table.printAll()
    table.remove('21473719')
    table.remove('214737191')
    table.remove('214737192')
    print(table.count)
    print(table.actualSize)
    print("\n\n\n\n\nAfter removal:")
    table.printAll()
    print("\n\n\n\n\n")
    print(table.get("14217792"))
    print(table.get("21473719"))
    table.export()
    print("load factor: " + str(table.getLoadFactor()))
    