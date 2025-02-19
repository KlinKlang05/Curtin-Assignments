package edu.curtin.app.simulation.railway.state;

import edu.curtin.app.simulation.Town;
import edu.curtin.app.simulation.railway.Railway;

public interface RailwayState {
    int getAvailableRailways();
    void dailyRun(Railway railway);

    /**
     * @return true if the Stock was successfully sent.
     */
    boolean sendStock(Railway railway, Town from);

    /**
     * @return true if the Upgrade was successfully started.
     */
    boolean upgradeRailway(Railway railway); 
}