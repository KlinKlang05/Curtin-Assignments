package edu.curtin.app.factory;

import edu.curtin.app.MainLoop;
import edu.curtin.app.TownsInput;
import edu.curtin.app.simulation.*;
import edu.curtin.app.simulation.railway.Railway;
import edu.curtin.app.simulation.railway.state.InUseState;
import edu.curtin.app.simulation.railway.state.InitialConstructionState;
import edu.curtin.app.simulation.railway.state.OneAvailableState;
import edu.curtin.app.simulation.railway.state.TwoAvailableState;

public class TownSimFactory {
    public MainLoop getMainLoopInstance() {
        return new MainLoop(this);
    }

    public TownsInput getTownsInputInstance() {
        return new TownsInput();
    }

    public Town getTownInstance(String name, int initialPop) {
        return new Town(name, initialPop, this);
    }


    public TownTradeSimulation getTownTradeSimulationInstance() {
        return new TownTradeSimulation(this);
    }

    public GraphModelling getGraphModellingInstance() {
        return new GraphModelling();
    }

    public Railway getRailwayInstance(Town a, Town b) {
        return new Railway(a, b);
    }   

    //TODO: Add methods to UML diagram
}


