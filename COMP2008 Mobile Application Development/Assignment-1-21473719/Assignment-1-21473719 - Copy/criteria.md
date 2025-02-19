# Adherence to criteria: Kevin Kongo 21473719 
# OOSE 2024 semester 2

## a) Code quality
You'll find that the linting tool PMD returns no errors. 

## b) Appropriate use of containers
The main container used in this assignment is a two-dimensional array. It makes the most sense
given the city grid is static and once read from the file, does not need to be further manipulated. 
That array is only read from after being created. Apart from that, Some ArrayLists are used to store 
other various data types, especially when this list needs to be updated from time to time.

## c) Clear class/interface/method responsibilities.
All of my classes are named appropriate to what their respective functionality is. classes are 
contained inside the edu.curtin.citybuilder.gridunit package in order to separate all the classes
that are part of the decorator pattern.

## d) Appropriate error handling and logging
The program has been tested extensively to ensure it gracefully handles errors, and ensures that 
a user cannot enter an incorrect line that causes the program to crash. I have created two classes that
extend Exception (InvalidFileFormatException and InvalidHeritageException) in order to clearly define when 
the data file has been incorrectly formatted or contains incorrect data.

## e) Appropriate use of the Strategy Pattern and/or Template Method Pattern.
Upon reading the specification for this assignment and creating my UML diagram, it became apparent that 
I could not find a clear place to use the strategy/template method pattern (beyond the polymorphism 
found in the decorator pattern) and actually have methods that implement or extend the pattern to 
demonstrate their use. However, there still is a way to reasonably demonstrate the strategy pattern 
in this assignment. The wrapper Class (BuilderMenuWrapper) is able to store an instance of a class that 
implements CityBuilder. This, in theory would allow future versions of this application to add extra 
implementations of CityBuilder that the wrapper could continue to take advantage of. You'll find that 
BuilderMenuWrapper features polymorphic method calls to CityBuilder, demonstrating the use of the strategy pattern.

The implementing class can store the City Grid and run tests on the grid however the designer sees fit without affecting the way BuilderMenuWrapper 
makes requests to a class that extends CityBuilder. Furthermore, a designer could implement the customBuildCity method in any way they desire
and perform their own grid test (For example, generate structure based on distance from the top left corner, bottom right corner, economic situation, laws..?, pre-made structure data) 
In my case, the implementing class is OOSECityBuilder, which stores a two-dimensional 
array of GridUnit classes, and as per the requirements of the assignment, implements customBuildCity by generating
structures based on their distance from the centre of the grid. 

## f) Appropriate use of the Decorator Pattern.
Here, Each grid square in the city grid can use the decorator pattern to add modifications to the result generated when
testing for the viability of a certain Structure being constructed on a certain GridUnit. All classes in 
edu.city.curtin.citybuilder.gridunit implement GridUnit (except InvalidHeritageException). Our base implementations are 
each of the three terrain types (rocky, swampy, flat) and each have their own effects on the cost per floor, as well as
what structures can be built on the terrain. All the decorators extend GridUnitDecorator. GridUnitDecorator contains a
reference to the next decorator or the base implementation (GridUnitDecorator.next). In this way, as shown around lines 
57-89 in DataFileIO.java, each decorator can be initialized to store extra decorators or the base implementation based 
on the data given after the terrain type in the data file.

when calling test() on a decorated object, each decorator first calls test() the next decorator, all the way to the 
base object. The base object creates an instance of StructureTestResult that is then passed through each decorator. 
Each object runs their respective test and manipulates StructureTestResult accordingly. They can add more cost to the 
StructureTestResult object, add a multiplier to the cost that is calculated when accessing the final cost, or change the
viability of the construction on that grid location by calling setBuildable(). Each decorator first calls isBuildable() 
to check if the previous decorator or the base object has already determined that the structure cannot be built on that
grid location. If the decorator itself finds that the Structure cannot be built, it sets the buildable attribute to false,
and adds a reason why it wasn't buildable by calling addReason(). Any accessing method can then receive the returned
StructureTestResult object and call the respective methods to see if the Structure was able to be built.
