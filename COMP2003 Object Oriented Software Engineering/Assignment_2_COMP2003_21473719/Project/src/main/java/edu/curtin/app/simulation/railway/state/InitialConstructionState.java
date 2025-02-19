package edu.curtin.app.simulation.railway.state;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.Town;
import edu.curtin.app.simulation.railway.Railway;

public class InitialConstructionState implements RailwayState{
    @Override
    public int getAvailableRailways() {
        return 0; 
    }

    @Override
    public void dailyRun(Railway railway) {
        int daysRemaining = railway.getCDaysLeft()-1;

        if (daysRemaining == 0) {
            railway.setDirection(railway.getBothTowns()[1]);
            railway.setState(new OneAvailableState());
        }

        railway.setCDaysLeft(daysRemaining);
    }

    @Override
    public boolean sendStock(Railway railway, Town from) {
        return false;
    }

    @Override
    public boolean upgradeRailway(Railway railway) {
        return false;
    }

}
