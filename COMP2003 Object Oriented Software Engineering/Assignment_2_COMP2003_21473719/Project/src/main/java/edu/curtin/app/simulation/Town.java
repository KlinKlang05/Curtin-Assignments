package edu.curtin.app.simulation;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Logger;

import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.railway.Railway;

public class Town {
    private final TownSimFactory factory;
    private static final Logger log = Logger.getLogger(Town.class.getName());
    private String name;
    private int population;
    private int stockPile = 0;
    private final Set<Railway> railways = new HashSet<>();

    public Town(String name, int initialPop, TownSimFactory factory) {
        if (initialPop < 0) {
            throw new IllegalArgumentException("Population value must be equal to or greater than zero.");
        }

        this.factory = factory;

        this.name = name;
        this.population = initialPop;
    }

    public void setPopulation(int population) {
        if (this.population >=0 ) {
            this.population = population;
        }
    }

    public int getPopulation() {
        return this.population;
    }

    public void buildRailway(Town to) {
        buildRailway(factory.getRailwayInstance(this, to));
    }

    public void buildRailway(Railway railway) {
        Town[] bothTowns = railway.getBothTowns();
        if (railways.contains(railway)) {
            throw new IllegalStateException("the provided railway already exists.");
        } else if (bothTowns[0].equals(this) || bothTowns[1].equals(this)) {
            railways.add(railway);
        } else {
            throw new IllegalArgumentException("The provided railway does not contain this Town as one of the two destination towns.");
        }
    }

    public List<Town> getSingleLinkedTowns() {
        List<Town> singleRailwayTowns = new ArrayList<>();

        for (Railway railway : railways) {
            if (railway.getSize() == 1) { // This is a single railway
                singleRailwayTowns.add(railway.getDestination(this));
            }
        }

        return singleRailwayTowns;
    }

    public List<Town> getDualLinkedTowns() {
        List<Town> dualRailwayTowns = new ArrayList<>();

        for (Railway railway : railways) {
            if (railway.getSize() == 2) { // This is a dual railway
                dualRailwayTowns.add(railway.getDestination(this));
            }
        }

        return dualRailwayTowns;
    }

    public List<Railway> getInCSingleRailways() {
        List<Railway> singleRailwaysInConstruction = new ArrayList<>();

        for (Railway railway : railways) {
            if (railway.getSize() == 0) {
                singleRailwaysInConstruction.add(railway);
            }
        }

        return singleRailwaysInConstruction;
    }

    public List<Railway> getInCDualRailways() {
        List<Railway> dualRailwaysInConstruction = new ArrayList<>();

        for (Railway railway : railways) {
            if (railway.getCDaysLeft() != 0 && railway.getSize() == 1) {
                dualRailwaysInConstruction.add(railway);
            }
        }

        return dualRailwaysInConstruction;
    }

    public void produceGoods() { // Should be called once daily
        this.stockPile += this.population;
    }

    /**
     * @return the total amount of goods sent along all railways in a day.
     */
    public int sendGoods() { // Should be called once daily
        int totalSent = 0;

        for (Railway railway : railways) {
            if (railway.sendStock(this)) {
                if (stockPile >= 100) {
                    stockPile -= 100;
                    totalSent += 100;
                } else {
                    totalSent += stockPile;
                    stockPile = 0; // return the stockpile to zero for any amount under 100 remaining
                }
            } else {
                log.finest(() -> String.format("The town %s was the last town to send along the railway. Letting the other town have a turn.", this.name));
            }
        }

        return totalSent;
    }

    public int getStockPile() {
        return this.stockPile;
    }

    /**
     * A wrapper method that gets the associated railway and calls upgradeLink(Railway)
     * @throws IllegalStateException if the railway is in use, already in construction, or is already upgraded.
     * @throws IllegalArgumentException if the Town object you're calling this on does not have a link to the provided Town.
     */
    public void upgradeLink(Town to) { // If you don't know the railway or don't know if it exists, call this
        for (Railway railway : railways) {
            if (railway.getDestination(this).equals(to)) {
                if (upgradeLink(railway)) {
                    return;
                } else {
                    throw new IllegalStateException("The Railway to the town provided is either in use, in construction, or is already upgraded. " +
                            "Call getDualLinkedTowns() and check if the town is in there, if you're not sure.");
                }

            }
        }
        throw new IllegalArgumentException("This town does not have an existing railway to the provided town.");
    }

    /**
     * @param railway the railway you want to upgrade. Should be a railway that the Town object is connected to.
     * @return False if the Railway could not be built, either because the railway is currently in use (Which should never actually be the case since this should be called before any goods are sent for the day) <br>
     *  or if the railway is already in construction, or is already upgraded.
     * @throws IllegalArgumentException if the Town object you're calling this on does not have the provided railway as an attribute in its known connected railways.
     */
    public boolean upgradeLink(Railway railway) {       // If you think you know the railway call this
        if (railways.contains(railway)) {
            return railway.upgradeRailway();
        } else {
            throw new IllegalArgumentException("This town is not a destination on either end of the provided railway.");
        }
    }

    public String getName() {
        return name;
    }
}
