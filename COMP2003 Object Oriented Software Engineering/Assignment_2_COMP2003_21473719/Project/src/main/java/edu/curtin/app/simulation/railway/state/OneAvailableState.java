package edu.curtin.app.simulation.railway.state;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.Town;
import edu.curtin.app.simulation.railway.Railway;

public class OneAvailableState implements RailwayState{
    @Override
    public int getAvailableRailways() {
        return 1;
    }

    @Override
    public void dailyRun(Railway railway) {
        if (railway.getRailwaysInUse() == 1 || railway.getCDaysLeft() - 1 == 0) {
            railway.setRailwaysInUse(0);
            railway.setState(new TwoAvailableState());
        } else if (railway.getRailwaysInUse() != 0) {
            throw new AssertionError("The Railway should not have any railways in use in use if it is a single railway while in the OneAvailableState. It should have one railway in use is a dual railway and in this state. If there's any other value, something's wrong");
        }

        railway.lowerCDaysDuringC();
    }

    @Override
    public boolean sendStock(Railway railway, Town from) {
        if (!railway.getDirection().equals(from) || railway.getRailwaysInUse() == 1) {
            railway.reverseDirection();
            railway.setRailwaysInUse(railway.getRailwaysInUse() + 1);
            railway.setState(new InUseState());

            return true;
        }

        return false;
    }

    @Override
    public boolean upgradeRailway(Railway railway) {
        if (railway.getRailwaysInUse() == 0) {
            railway.setCDaysLeft(5);
            return true;
        }

        return false;
    }
}
