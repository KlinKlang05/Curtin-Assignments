package edu.curtin.app.observers;

public interface DayCompletedObserver {
    /**
     * call each getter in the MainLoop class to get a 2d array of messages. the first item in each sublist is the name of a town.
     * The second item in each sublist is either another town name or a population. no type checking or error handling is required
     * since MainLoop will have already done that.
     * getInvalidEvents() is a list of invalid messages.
     * @param lastDay true if and only if the mainLoop is broken. It's only ever true once for the lifetime of the program.
     */
    void dayCompleted(boolean lastDay);

}
