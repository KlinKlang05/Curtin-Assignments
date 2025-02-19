package edu.curtin.app.simulation.railway.state;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.Town;
import edu.curtin.app.simulation.railway.Railway;

public class TwoAvailableState implements RailwayState {
    @Override
    public int getAvailableRailways() {
        return 2;
    }

    @Override
    public void dailyRun(Railway railway) {
    }

    @Override
    public boolean sendStock(Railway railway, Town from) {
        railway.setDirection(from);     // By setting the direction to the town that just sent the stock,
        // it guarantees that the direction will be set up in a way that allows the town on the other end to send stock
        // (since when the Railway is in the One Available state, it checks if the direction is set to the opposite town.
        // the direction is only really important when the railway is single, so this ensures that both towns
        // will always be able to send along the railway and not get blocked by a mis-set direction.)
        railway.setRailwaysInUse(railway.getRailwaysInUse() + 1);
        railway.setState(new OneAvailableState());

        return true;
    }

    @Override
    public boolean upgradeRailway(Railway railway) {
        return false;
    }
}
