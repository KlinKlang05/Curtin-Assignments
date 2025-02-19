# Criteria

### a) General code quality
No PMD errors. No major code quality issues. 

### b) Clear and distinct package/class/interface/method responsibilities
Packages are divided into the responsibilities of each group of classes. The observer interface is in its own package for clarity. 
The state classes are in a sub-package of the package where the Railway class is. 
All of the classes that run the "simulation" are in its own package. This is because the classes in that package 
implement the observer class and operate based on the output of the MainLoop class.

### c) Appropriate error handling and logging
There are logging statements placed in relevant and appropriate locations in the program.
Exceptions are handled gracefully. Some exceptions are used in the program to display the reason for 
invalid messages. The exceptions are logged and the program continues to operate.

### d) Implementation of dependency injection
All classes except state classes are instantiated using a Factory class. 
The Factory class is instantiated in the Main class, allowing for easy overriding when testing.
All classes that require the factory keep an instance of the factory as a field. That Association is obvious and it seems unnecessary to include that in the UML diagram. 

### e) Appropriate use of the observer pattern
The observer interface is called DayCompletedObserver. The MainLoop class will call the single method in the interface, dayCompleted(). This method is called every time a loop 
is completed and all the messages for the "day" are received. 

The Method takes one parameter, a boolean lastDay. when lastDay is true, it signals that the the "final" day has arrived an allows the implementing observer to perform any actions it might need
to at the end of the Program's life. The observer is implemented in the TownTradeSimulation class, which uses an anonymous class
to add an observer to MainLoop. when lastDay is true, TownTradeSimulation will export simoutput.dot.

This implementation of the observer pattern uses a callback mechanism which allows the implementing observer to 
call methods from the Subject class (MainLoop) and recieve useful data. In the case of this implementation, each Event type 
can be recieved in a different method. These methods provide the data required for the TownTradeSimulation to perform 
its respective functionality.

### f) Appropriate use of the state pattern 

The state pattern is demonstrated using the Railway class. The railway has 4 states:

- InitialConstructionState: The class remains there for 5 loops of the mainloop, aka dailyRun should be called 5 times.
After exiting the In construction state, a railway does not return to that state. This state allows all sending of goods 
to be blocked. and does not allow any method calls to the railway to cause it to leave that state until 5 "days" have passed.
- OneAvailableState: Whenever there is only one free railway to send on, the railway is in this state. This could be either
when a singe track railway has no goods being sent, or a dual track railway has one railway being used to send goods.
- TwoAvailableState: Whenever there is a dual track railway with both railways free, the railway is in this state.
- InUseState: Whenever either a dualtrack or single track railway has its railways fully occupied for the day, the 
class is in this state. 

Please see the State diagram for more information on how the class moves between states.
