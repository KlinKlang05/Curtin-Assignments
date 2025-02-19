from getchar import getch
from DSAShoppingCentre import ShoppingCentre
from LinkedListDEDL import DSALinkedList as LL
from TextManipulation import TextEffects
import os

def dummyFunction():
    print(TextEffects.cursorToLine2)
    print(TextEffects.clearAfterCursor)

class ShopMenuSystem(ShoppingCentre): # User has the option of calling this class, which provies a GUI to manipulate and access Shopping Centre data, 
    def __init__(self) -> None:       # or can directly call the ShoppingCentre class and use it in their own functions
        self._mainFuncs = LL(self.showAll, self.menuFindID, self.menuFindName, self.menuFindCategory, self.menuShowCategories, self.menuGetPath, self.showAdjacency, self.export, self._selectionLoopExtras, self._finish)
        self._settingsFuncs = LL(self.menuAddShop, self.menuRemoveShop, self.menuUpdateEntry, self.menuAddPath, self.menuRemovePath, self.showRemaningFree, self._finish)
        self._mainMenu = LL('Show all Shops', 'Search by ID', 'Search by Name', 'Search by Category', 'Show Categories', 'Find Path Between Stores', 'Show Store Adjacency List', 'Export Data', 'Extras', 'Exit')
        self._settingsMenu = LL('Add Store', 'Remove Store', 'Update Store Details', 'Add Path Between Stores', 'Remove Path Between Stores', 'Show Remaining Spaces Available', 'Back')
    
    def menuAddShop(self):
        try:
            id = int(input("ID? -> "))
            name = input("name? -> ")
            category = input("category? -> ")
            location = input("location? -> ")
            rating = int(input("rating? -> "))
        except ValueError:
            print("Invalid entry! Please ensure ID and rating are integers. ID should be between 1 and 5.")
        else:
            if self.addShop(id, name, category, location, rating) == None:
                error_status = 3
            else:   
                error_status = 0

            return error_status

    def menuRemoveShop(self):
        selection = input("remove using name or ID? ")
        if selection.lower() == "name":
            removed = self.removeShop(name = input("insert name: "))
        elif selection.lower() == 'id':
            try:
                removed = self.removeShop(id = int(input("insert ID: ")))
            except ValueError:
                print("Invalid ID! Try again.")
        else:
            print("invalid selection! Enter ID or Name (case insensitive)")
            return
        
        print("\nRemoved the following:\n")
        print(removed)

    def menuFindID(self):
        try:
            shop = self.find(id = int(input("insert ID: ")))
        except ValueError:
            print("Invalid ID! Please try again.")
        else: 
            if shop != None: 
                print(TextEffects.cursorToLine2 + TextEffects.clearAfterCursor)
                print(shop)
            else: 
                print("No shop found.")
    
    def menuFindName(self):
        shop = self.find(name = input("insert name: "))
        if shop != None:
            print(TextEffects.cursorToLine2 + TextEffects.clearAfterCursor)
            print(shop)
        else:
            print("No shop found.")
    
    def menuFindCategory(self):
        cat = input("select category: ")
        if self.findCategory(cat) != 1:
            print("\nResults are descending, as the highest rated stores will be seen first. Scroll up to see descending ratings.")

    def menuUpdateEntry(self): 
        selection = input("Select shop to edit using name or ID? ")
        if selection.lower() == "name":
            selection = self.find(name = input("insert name: "))
        elif selection.lower() == 'id':
            try:    
                selection = self.find(id = int(input("insert ID: ")))
            except ValueError:
                print("Invalid ID! Please try again.")
                selection = None
        else: 
            selection = None
            print("Please enter 'Name' or 'ID'! Case insensitive. ")
        
        if selection != None:
            print("\nInsert New Values:\n")
            try:
                id = int(input("ID? -> "))
                name = input("name? -> ")
                category = input("category? -> ")
                location = input("location? -> ")
                rating = int(input("rating? -> "))
                self.updateShop(selection, id, name, category, location, rating)
            except ValueError:
                print("Invalid input! try again.")

    
    def menuAddPath(self):
        print("Please note: Paths can only be added using ID numbers, not names.\n")
        try:
            start = int(input("select starting point (ID): "))
            finish = int(input("select linking point (ID): "))
            if self.addPath(start, finish) == 1:
                print("The two shops could not be linked. Please try again.")
            else: 
                print("The two shops were successfully linked.")
        except ValueError:
            print("Invalid ID numbers! Try again.")

    def menuRemovePath(self):
        print("Please note: Paths can only be removed using ID numbers, not names.\n")
        try:
            start = int(input("select first point (ID): "))
            finish = int(input("select second point (ID): "))
            if self.removePath(start, finish) == 1:
                print("The path between the two shops could not be removed. ID's likely don't exist. Please try again.")
            else: 
                print("The two shops were successfully un-linked.")
        except ValueError:
            print("Invalid ID numbers! Try again.")

    def menuGetPath(self):
        try:
            start = int(input("enter starting point ID: ")) 
            finish = int(input("Enter finishing point ID: "))
            self.getPath(start, finish)
        except ValueError:
            print("Invalid input! Try again")

    def showRemaningFree(self):
        print("Total spaces: " + str(self.maxSize))
        print("Spaces used: " + str(self.currentSize))
        print("Remaining spaces: " + str(self.maxSize - self.currentSize))
    
    def menuShowCategories(self):
        self.categoryTable.printAll(keyOnly=True)

    def _finish(self):
        print(TextEffects.cursorVisible)
        return 1
    
    def _printMenu(self, MenuPos:int, menu:LL):
        print(TextEffects.cursorInvisible)
        print(TextEffects.cursorToHome, end="")
        print(TextEffects.BLUE + "Data Structures And Algorithms Shopping Centre Manager 2023. By Kevin Kongo, 21473719. Controls: W = up, S = down, Enter = Select" + TextEffects.ENDC)
        print()
        for option in menu:
            if MenuPos == menu.index(option):
                print(TextEffects.HighlightWhite + option + TextEffects.ENDC)
            else:
                print(option)
    
    def _selectionLoop(self, menuText:LL, menuFunctions:LL): 
        optionCount = menuText.length
        exit_state = 0
        choice = 0

        print(TextEffects.clearScreen)
        self._printMenu(choice, menuText)
        while exit_state != 1:
            exit_state = 0
            keyIn = getch()

            if os.name == 'nt':
                keyIn = int.from_bytes(keyIn)
            else:
                keyIn = ord(keyIn)

            if keyIn == 119: # w key
                choice = (choice - 1) % optionCount 
                self._printMenu(choice, menuText)
            elif keyIn == 115: # s key
                choice = (choice + 1) % optionCount
                self._printMenu(choice, menuText)

            elif keyIn == b'\r' or keyIn == 13:   # enter key 
                print(TextEffects.cursorToLine2 + TextEffects.clearAfterCursor)
                exit_state = menuFunctions[choice]() # Where the logic is executed, calls necessary functions.
                
                
                if exit_state != 1 and exit_state != 2: # no need to execute this if the intention is to leave the program, or returning from a submenu
                    print(TextEffects.cursorVisible)
                    print('\nPress any key to continue: ', end="")
                    getch()
                    print(TextEffects.clearScreen)
                    self._printMenu(choice, menuText)
                elif exit_state != 1:  # Only _selectionLoop and _selectionLoopExtras returns 2. This is to ensure that going back on the menu doesn't require a keypress to continue.
                    print(TextEffects.clearScreen)
                    self._printMenu(choice, menuText)

        return 2 # this function is ran recursively, so returning 2 ensures exiting out of the second layer of this function doesn't prematurely exit out of the first layer as well. The return value is passed to exit_state.

    def _selectionLoopExtras(self): # wrapper code so _selectionLoop doesn't have to pass values in, adding unecessary checks to see which function is being called and if it needs parameters.
        exit_state = self._selectionLoop(self._settingsMenu, self._settingsFuncs)
        return exit_state

    def openMenu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        size = -1
        while size < 0:
            try:
                size = int(input("select the maximum number of stores in the shopping Centre. Enter '0' if you are importing shopping centre data: "))
                if size == 0:
                    path = input("Enter File path/name: ")
                    super().__init__(size, path)
            except ValueError:
                print('Invalid Size!')
            except FileNotFoundError:
                print('Invalid file name or path!')
                size = -1
    

        if size != 0:
            super().__init__(size)
        
        self._selectionLoop(self._mainMenu, self._mainFuncs)


Carousel = ShopMenuSystem()

Carousel.openMenu()














            
     


