package edu.curtin.app.simulation.railway.state;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.Town;
import edu.curtin.app.simulation.railway.Railway;

public class InUseState implements RailwayState{
    @Override
    public int getAvailableRailways() {
        return 0;
    }

    @Override
    public void dailyRun(Railway railway) {
        if (railway.getRailwaysInUse() == 2 || railway.getCDaysLeft() - 1 == 0) {
            railway.setRailwaysInUse(0);
            railway.setState(new TwoAvailableState());
        } else if (railway.getRailwaysInUse() == 1) {
            railway.setRailwaysInUse(0);
            railway.setState(new OneAvailableState());
        } else {
            throw new AssertionError("The Railway should never be in InUseState and not have 1 or 2 railways in use.");
        }

        railway.lowerCDaysDuringC();
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
