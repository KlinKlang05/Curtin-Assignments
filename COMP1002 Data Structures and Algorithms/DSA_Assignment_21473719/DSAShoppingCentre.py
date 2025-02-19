from __future__ import annotations
from DSAHash import DSAHashTable
from DSAHeap import DSAHeap
from DSATrees import DSABinarySearchTree
from LinkedListDEDL import DSALinkedList
from QueueStackLinkedList import DSAQueue, DSAStack
from graph import DSAGraph
import csv
import numpy as np


class Shop(object):
    def __init__(self, id:int, name:str, category:str, location:str, rating:int) -> None:
        self.id = id
        self.name = name  
        self.category = category
        self.location = location 
        self.rating = rating 

    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, rating):
        out = rating 
        if rating > 5 or rating < 1:
            raise ValueError("Rating is invalid! It will default to Empty until a correct value is set. Rating should be between 1 and 5.")

        self._rating = out 

    def setcategory(self, newCategory):
        self.category = newCategory

    def setlocation(self, newLocation):
        self.location = newLocation

    def __eq__(self, __value: object) -> bool: # Comparing Shop Objects compares them by their rating by default
        if not isinstance(__value, Shop):
            if __value == None:
                return self.rating == None
            return NotImplemented
        
        return self.rating == __value.rating
    
    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Shop):
            return NotImplemented
        
        return self.rating < __value.rating
    
    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Shop):
            return NotImplemented
        
        return self.rating > __value.rating
    
    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, Shop):
            return NotImplemented
        
        return self.rating >= __value.rating
    
    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, Shop):
            return NotImplemented
        
        return self.rating > __value.rating
    
    def __ne__(self, __value: object) -> bool:
        if not isinstance(__value, Shop):
            if __value == None:
                return self.rating != None
            return NotImplemented
        
        return self.rating != __value.rating
        
    def __str__(self) -> str:
        if self.rating == None: 
            rate = "Empty"
        else: 
            rate = u"\u2605 " * self.rating
        out = f"Name: {self.name}\nID: {self.id}\ncategory: {self.category}\nlocation: {self.location}\nrating: " + rate
        return out 
    
    def __int__(self) -> int: # If being accessed in a heap, the value to sort by will be its ID, therefore calling int() on this object should return the self.id attribute.
        return self.id


class ShoppingCentre():
    def __init__(self, size, *arg:str) -> None:
        """setting size to '0' and including an appropriate CSV file as a second argument will import Shopping Centre data.
        Importing a CSV will allocate enough space to hold the Shop entries plus extra space for 10 more stores."""
        self.currentSize = 0 
        if size == 0 and len(arg) == 1:
            self._importShoppingCentre(arg[0])
        elif size == 0: 
            raise ValueError('size argument must be greater than zero if not importing from CSV. The path to a file was not included.')
        else:
            self.network = DSAGraph(size)
            self.categoryTable = DSAHashTable(size)
            self.idTree = DSABinarySearchTree()    # One tree used to check the existence of a store via ID number
            self.nameTree = DSABinarySearchTree()  # Another tree used to check the existence of a store via name.
            self.maxSize = size

    def showAll(self):
        print('showing all:\n')
        for shop in self.idTree.getInOrder(): 
            print(shop)
            print("\n")
    
    def showAdjacency(self):
        print("showing Network of shopping centre as an adjacency list: \n\n")
        self.network.displayAsList()

    def addShop(self, id:int, name:str, category:str, location:str, rating:int):
        """Returns 1 if there was a ValueError, Returns 2 if there was any other unknown error. Returns None if successful."""
        retval = None
        try:
            entries = DSALinkedList(self.find(id=id), self.find(name=name))
            if entries[0] != None or entries[1] != None:                        # check for duplicates
                print('\n\n\nName/ID already used! No duplicates are allowed.')
                text = DSALinkedList("\nMatching name: \n", "\nMatching ID: \n")
                for e, t in zip(entries, text):
                    print(t)
                    if e == None:
                        print("No match found")
                    else: 
                        print(e)
            elif self.maxSize - self.currentSize == 0:
                print("maximum capacity is reached. Consider exporting current data and re-importing it, to have 10 extra free spaces.")
            else:
                entry = Shop(id, name, category, location, rating)

                category = category.lower()
                categoryList = self.categoryTable.get(category, False)
                if categoryList == -1:
                    categoryList = DSALinkedList(entry)
                    self.categoryTable.put(category, categoryList)
                else:
                    categoryList.insertLast(entry)
                    self.categoryTable.remove(category)
                    self.categoryTable.put(category, categoryList)

                self.network.addVertex(int(id))
                self.idTree.insert(id, entry)
                self.nameTree.insert(name.lower(), entry)

                self.currentSize += 1
        except ValueError:
            print('Invalid Values! Note ID and rating must be integer values. Rating must be bewteen 1 and 5.')
            retval = 1 
        except:
            print('An unknown error occured while adding shop data. Please try again.')
            retval = 2

        return retval


    def find(self, id=None, name=None, printResult=False) -> Shop:
        """Searches for a store by id number (id=<id>) or name (name=<name>). If both id and name are specified, search by ID will be prioritised.
        Returns None if no shop was found. 
        Returns a Shop object if a shop was found"""
        shopOut = None
        if id == None and name == None:
            print('Enter either the id number (id=<id>) or the name (name=<name>) of the Shop')
        else:
            try:
                if id == None:
                    shopOut = self.nameTree.find(name.lower()).getValue()
                else:
                    shopOut = self.idTree.find(id).getValue()
            except ValueError:
                if printResult:
                    print("shop could not be found. Please try again.")
                shopOut = None
            except AttributeError:
                shopOut = None 

        if shopOut != None and printResult:
            print(shopOut.getValue())
        
        return shopOut
    
    def findCategory(self, category:str):
        """Returns 1 if there was an error."""
        categoryList = self.categoryTable.get(category.lower())
        if categoryList != -1:
            arr = np.empty(categoryList.length, dtype=object)
            for c, shop in enumerate(categoryList):
                arr[c] = shop
            arranger = DSAHeap(categoryList.length)
            out = arranger.heapSort(arr, categoryList.length)
            for shop in out:
                print()
                print(shop)
        else: 
            print("Category was not found. Please try again.")
            return 1

    def removeShop(self, id=None, name=None):
        """Returns the shop if None."""
        shop = self.find(id, name)
        retval = None
        if shop != None:
            shopName = shop.name
            shopID = shop.id
            self.network.deleteVertex(shopID)
            self.idTree.delete(shopID)
            self.nameTree.delete(shopName)

            category = shop.category.lower()
            categoryList = self.categoryTable.get(category, printResult=False)
            categoryList.remove(shop)
            self.categoryTable.remove(category)
            self.categoryTable.put(category, categoryList)

            retval = shop
            self.currentSize -= 1
        else:
            print("shop was not found.")

        return retval
    
    def updateShop(self, oldShop:type[Shop], newID:int, newName, newCat, newLocation, newRating:int):
        """Automatically maintains previous connections with other shops."""
        edges = self.network.getEdges(oldShop.id) # Get all edges
        self.removeShop(id=oldShop.id) # Remove the selected shop to allow the updated one to replace it.
        
        if self.addShop(newID, newName, newCat, newLocation, newRating) != None: # Add updated Values here
            print("Unsuccessful removal, please try again.")
            self.addShop(oldShop.id, oldShop.name, oldShop.category, oldShop.location, oldShop.rating)
        else:
            for node in edges:
                if self.addPath(newID, node) == 1:
                    print(f"Something went wrong re-linking the node ({newID}) to {node}. Please try again.")
            print("Update was successful. The updated node maintains the connections with the rest of the network.")

    def addPath(self, initial, final):
        """Returns 1 if unsuccessful."""
        if self.network.addEdge(initial, final) == 1: # Unsuccessful linking
            return 1
    
    def removePath(self, initial, final):
        """Returns 1 if unsuccessful."""
        if self.network.deleteEdge(initial, final) == 1:
            return 1

    def getPath(self, start:int, finish:int):                                                     # Wrapper for self._findPath. This doesn't necessarily find THE shortest path from one node to the other, 
        """Start and Finish parameters should be integers representing the ID's of the stores.""" # but returns the shortest path after performing the two graph search algorithms covered in DSA.
        p1 = self.network.breadthFirstSearch(start)
        p2 = self.network.depthFirstSearch(start)
        
        if p1 != None and p2 != None:
            self._breadthPath = DSALinkedList()
            self._depthPath = DSALinkedList()

            self._findPath(start, finish, p1.length-1, p1, self._breadthPath)
            self._findPath(start, finish, p2.length-1, p2, self._depthPath)

            if self._breadthPath.peekLast() != None and self._depthPath.peekLast() != None:
                if self._breadthPath.length < self._depthPath.length:
                    final = self._breadthPath
                else:
                    final = self._depthPath

                print(final)

                print("Start -> ", end="")
                for store in final:
                    print(self.find(store).name, end="")
                    print(" -> ", end="")
                print("Finish")

            else: 
                print("There is no path that links the two specified stores.")
        else:
            print("The starting or finishing ID does not exist.")

    def export(self):
        toExport = self.idTree.getInOrder()   # get all nodes
        try:
            with open('shopping_centre_export.csv', 'w',newline='') as out:
                writer = csv.writer(out, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["ID","name","category","Location","Rating","Connections"])
                for item in toExport:                                       
                    row = DSALinkedList(item.id, item.name, item.category, item.location, item.rating) # Add the data from each node to a temporary list
                    for link in self.network.getEdges(item.id): # Add the ID from all shops linked to that node to the temporary list
                        row.insertLast(link)  
                    writer.writerow(row) # Write to the CSV
        except:
            print("unknown error has occurred.")
        else:
            print("Exported final with the name 'shopping_centre_export.csv'.")
            

    def _findPath(self, start, finish, currIndex, searchTraversal:DSALinkedList, output:DSALinkedList()):  # pass the output location by reference, makes it much easier to get a value out of a recursive function
        if currIndex < 0:                                                           #NEED TO CHECK IF THIS IS WORKING THE WAY I THINK IT IS 
            output.insertLast(None)
            return
        if searchTraversal[currIndex] == finish:
            output.insertFirst(finish)
            if searchTraversal[currIndex - 1] == start: 
                output.insertFirst(start)
                return
            else:
               self._findPath(start, searchTraversal[currIndex - 2], currIndex, searchTraversal, output) 
        else:
            self._findPath(start, finish, currIndex - 2, searchTraversal, output)

    def _importShoppingCentre(self, filename):
        with open(filename, 'r') as csvforcounting:   # Iterate over the file the first time to get the number of entries in the CSV
            size = -1 # start at negative one to disregard header in CSV
            counter = csv.reader(csvforcounting)
            for i in counter:
                size += 1

        self.network = DSAGraph(size + 10)    # allow for 10 more shops to be added.
        self.categoryTable = DSAHashTable(size + 10)
        self.idTree = DSABinarySearchTree()  
        self.nameTree = DSABinarySearchTree()
        self.maxSize = size

        with open(filename, 'r') as csvfile: # Iterate the second time to add each entry
            reader = csv.reader(csvfile)
            next(reader) # skip header in CSV
            for row in reader:
                if self.addShop(int(row[0]), row[1], row[2], row[3], int(row[4])) != None:
                    print("an error occured while trying to import store with ID: " + row[0] + ", Name: " + row[1])
        
        with open(filename, 'r') as csvfile: # Iterate the third time to add the connections between stores. This needs to be done seperately as the Nodes must already be created.
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                for link in row[5:]:
                        if self.addPath(int(row[0]), int(link)) == 1:
                            raise Exception("something happened lol ")

        self.maxSize += 10


if __name__ == "__main__":
    out = Shop(123, "hello", "housing", "top floor", 4)
    print(out)

    GardenCity = ShoppingCentre(10)
    GardenCity.addShop(123, "hello", "housing", "top floor", 4)
    print(GardenCity.idTree.find(123))

