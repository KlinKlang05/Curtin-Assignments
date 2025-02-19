package edu.curtin.app;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.TownTradeSimulation;

/**
 * Entry point into the application. To change the package, and/or the name of this class, make
 * sure to update the 'mainClass = ...' line in build.gradle.
 */
public class App
{
    public static void main(String[] args) {
        TownSimFactory factory = new TownSimFactory();

        MainLoop mainLoop = factory.getMainLoopInstance();

        TownTradeSimulation simulation = factory.getTownTradeSimulationInstance();
        simulation.setUp(mainLoop); // adds an observer to the MainLoop so it can interact with MainLoop events
                                    // If class is not added as on observer, the loop will still run, just nothing is being done with the information.

        mainLoop.mainLoop();
    }
}
