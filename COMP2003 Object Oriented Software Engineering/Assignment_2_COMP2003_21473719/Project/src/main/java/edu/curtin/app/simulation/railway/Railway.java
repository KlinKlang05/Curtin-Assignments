package edu.curtin.app.simulation.railway;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.Town;
import edu.curtin.app.simulation.railway.state.InitialConstructionState;
import edu.curtin.app.simulation.railway.state.RailwayState;

public class Railway {
    private RailwayState state;
    private int cDaysLeft;
    private final Town townA;
    private final Town townB;
    private Town direction = null;
    private int railwaysInUse = 0;

    public Railway(Town townA, Town townB) {
        this.townA = townA;
        this.townB = townB;
        this.cDaysLeft = 5;
        this.state = new InitialConstructionState();
    }

    public void setState(RailwayState state) {
        this.state = state;
    }

    public Town[] getBothTowns() {
        return new Town[]{townA, townB};
    }

    public void setCDaysLeft(int days) {
        cDaysLeft = days;
    }

    public int getCDaysLeft() {
        return cDaysLeft;
    }

    public void lowerCDaysDuringC() { 
        if (cDaysLeft-1 > 0) {
            cDaysLeft -= 1;
        }
    }

    public int getSize() { // The sum of the railways in use and the available (not in use) railways equals the total railways on a link between towns. 
        return this.railwaysInUse + state.getAvailableRailways();
    }

    public void dailyRun(){
        state.dailyRun(this);
    }

    public boolean sendStock(Town from) {
        return state.sendStock(this, from);
    }

    public Town getDestination(Town town) {
        if (town.equals(townA)) {
            return townB;
        } else if (town.equals(townB)) {
            return townA;
        } else {
            return null;
        }
    }

    public boolean upgradeRailway() {
        return state.upgradeRailway(this);
    }

    /**
     * @return null if the direction has not yet been set. This should only be null during the construction of the single railway.
     */
    public Town getDirection() {
        return direction;
    }

    public void setDirection(Town direction) {
        this.direction = direction;
    }

    public int getRailwaysInUse() {
        return railwaysInUse;
    }

    public void setRailwaysInUse(int railwaysInUse) {
        this.railwaysInUse = railwaysInUse;
    }

    public int getAvailableRailways() {
        return state.getAvailableRailways();
    }

    public void reverseDirection() {
        if (this.direction == null) {
            throw new IllegalStateException("reverse direction is called before the initial railway construction is finished.");
        }

        if (this.direction.equals(townA)) {
            this.direction = townB;
        } else if (this.direction.equals(townB)) {
            this.direction = townA;
        } else {
            throw new AssertionError("Issue swapping directions. the direction is not to either of the Towns the Railway is linking.");
        }
    }
}
