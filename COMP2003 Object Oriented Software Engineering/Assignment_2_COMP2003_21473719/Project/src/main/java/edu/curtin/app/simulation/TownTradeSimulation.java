package edu.curtin.app.simulation;

import edu.curtin.app.MainLoop;
import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.simulation.railway.Railway;

import java.util.*;
import java.util.logging.Logger;

public class TownTradeSimulation {
    private final TownSimFactory factory;
    private static final Logger log = Logger.getLogger(Town.class.getName());
    private final Map<String, Town> allTowns = new HashMap<>(); // Map used for easy search of a Town based on its name.
    private final Map<String, Railway> allRailways = new HashMap<>(); // Map used for easy search of a Railway based on the name of the two destination towns. key stored in the format "{townA} | {townB};
    private int day = 0;
    private GraphModelling model;

    public TownTradeSimulation(TownSimFactory factory) {
        this.factory = factory;
    }

    public void setUp(MainLoop mainLoop) {
        this.model = factory.getGraphModellingInstance();

        mainLoop.addObserver(finished -> {    // Set up an anonymous observer
            if (finished) {     // If the simulation is over, build the graph and return.
                model.buildGraph();
                return;
            }

            day++;
            dailyRun(); // Tick all Towns and Railways first
            StringBuilder messages = new StringBuilder();

            String currentEvent = "";
            String currentMsgA = "";
            String currentMsgB = "";
            try {

                for (List<String> message : mainLoop.getFoundingEvents()) {
                    currentEvent = "town-founding";
                    currentMsgA = message.get(0);
                    currentMsgB = message.get(1);
                    addNewTown(message.get(0), Integer.parseInt(message.get(1)));
                    messages.append(String.format("%s %s %s\n", "town-founding", message.get(0), message.get(1)));
                }
                for (List<String> message : mainLoop.getPopulationEvents()) {
                    currentEvent = "town-population";
                    currentMsgA = message.get(0);
                    currentMsgB = message.get(1);
                    updateTownPopulation(message.get(0), Integer.parseInt(message.get(1)));
                    messages.append(String.format("%s %s %s\n", "town-population", message.get(0), message.get(1)));
                }
                for (List<String> message : mainLoop.getConstructionEvents()) {
                    currentEvent = "railway-construction";
                    currentMsgA = message.get(0);
                    currentMsgB = message.get(1);
                    addNewRailway(message.get(0), message.get(1));
                    messages.append(String.format("%s %s %s\n", "railway-construction", message.get(0), message.get(1)));
                }
                for (List<String> message : mainLoop.getDuplicationEvents()) {
                    currentEvent = "railway-duplication";
                    currentMsgA = message.get(0);
                    currentMsgB = message.get(1);
                    upgradeRailway(message.get(0), message.get(1));
                    messages.append(String.format("%s %s %s\n", "railway-duplication", message.get(0), message.get(1)));
                }
                for (String message : mainLoop.getInvalidEvents()) {
                    messages.append(String.format("INVALID: %s\n", message));
                }
            } catch (NumberFormatException e) {
                throw new AssertionError("NumberFormatException caused even though the string is known to be a number value.", e);
            } catch (IllegalStateException | IllegalArgumentException e) {
                log.warning(e::getMessage);
                messages.append(String.format("INVALID: %s %s %s -- Reason: %s\n", currentEvent, currentMsgA, currentMsgB, e.getMessage()));
            }

            Map<String, Integer> sentGoods = sendAllTownGoods(); // Send all the goods based on the amount in the stockpile
            displayDailyResult(sentGoods, messages.toString());
        });
    }

    private Map<String, Integer> sendAllTownGoods() {
        Map<String, Integer> totalGoodsSent = new HashMap<>();

        for (Town town : allTowns.values()) {
            int sentGoods = town.sendGoods();
            totalGoodsSent.put(town.getName(), sentGoods);
        }

        return totalGoodsSent;
    }

    public void addNewTown(String name, int initialPop) {
        if (initialPop < 0) {
            throw new IllegalArgumentException("Initial population cannot be below zero");
        }
        addNewTown(factory.getTownInstance(name, initialPop));
    }

    public void addNewTown(Town town) {
        if (allTowns.containsKey(town.getName())) {
            throw new IllegalStateException("The new Town already exists in the Simulation (Same name)");
        } else {
            allTowns.put(town.getName(), town);
        }

        model.addNode(town);
    }

    public void updateTownPopulation(String name, int newPopulation) {
        if (newPopulation < 0) {
            throw new IllegalArgumentException("Initial population cannot be below zero");
        }

        Town townToUpdate = allTowns.get(name);

        if (townToUpdate != null) {
            townToUpdate.setPopulation(newPopulation);
        } else {
            throw new IllegalStateException("The provided name does not have a reference to an existing Town. The Town doesn't exist.");
        }
    }

    public void addNewRailway(String townA, String townB) {
        if (!(allRailways.containsKey(townA + " | " + townB) || allRailways.containsKey(townB + " | " + townA))) {
            Town townAIn = allTowns.get(townA);
            Town townBIn = allTowns.get(townB);

            if (townAIn != null && townBIn != null) {
                Railway railway = factory.getRailwayInstance(townAIn, townBIn);
                townAIn.buildRailway(railway);
                townBIn.buildRailway(railway);
                allRailways.put(townA + " | " + townB, railway);

                model.addEdge(railway);
            } else {
                throw new IllegalStateException("at least one of the provided town names does not have a reference to an existing Town. The Town doesn't exist.");
            }
        }
    }

    public void addNewRailway(Railway railway) {
        Town[] towns = railway.getBothTowns();
        Town townAIn = towns[0];
        Town townBIn = towns[1];

        if (!(allRailways.containsKey(townAIn.getName() + " | " + townBIn.getName()) ||
                allRailways.containsKey(townBIn.getName() + " | " + townAIn.getName()))) {

            townAIn.buildRailway(railway);
            townBIn.buildRailway(railway);
            allRailways.put(townAIn.getName() + " | " + townBIn.getName(), railway);

            model.addEdge(railway);
        }
    }

    public void upgradeRailway(String townA, String townB) {
        String format1 = townA + " | " + townB;
        String format2 = townB + " | " + townA;


        Railway toUpgrade;

        if (allRailways.containsKey(format1)) {
            toUpgrade = allRailways.get(format1);
        } else if (allRailways.containsKey(format2)) {
            toUpgrade = allRailways.get(format2);
        } else {
            throw new IllegalStateException("The Towns provided do not have a Railway connecting them.");
        }

        if (toUpgrade != null) {
            model.removeEdge(toUpgrade);
            boolean result = toUpgrade.upgradeRailway();
            model.addEdge(toUpgrade);

            if (!result) {
                throw new IllegalStateException("The Railway is currently under initial construction");
            }
        }

    }

    private void displayDailyResult(Map<String, Integer> sentGoods, String allMessages) {
        System.out.printf("---\nday %d:\n\nMessages: \n", day);

        System.out.println(allMessages);
        System.out.println();
        for (Town town : allTowns.values()) {
            System.out.printf("%s -> pop: %d | single_r: %d | double_r: %d | stockpile: %d | transported: %d | single_c: %d | double_c: %d\n",
                    town.getName(),
                    town.getPopulation(),
                    town.getSingleLinkedTowns().size(),
                    town.getDualLinkedTowns().size(),
                    town.getStockPile(),
                    sentGoods.get(town.getName()),
                    town.getInCSingleRailways().size(),
                    town.getInCDualRailways().size()
            );
        }
    }

    /**
     * The order in which the simulation is run is as follows: <br>
     * Call this method {@code dailyRun()} first. <br><br>
     * Then Update the population of all towns with {@code setPopulation()} and {@code upgradeLink()} as many times as required IF required. <br><br>
     * Then {@code sendGoods()}, and you can get the amount sent in a day with the return value.
     */
    private void dailyRun() {                    // Given the assignment spec says that "Goods are all produced right at the start of each day",
        for (Town town : allTowns.values()) {   // The very first daily task will be to update the town population.
            town.produceGoods();                // If the town population changes, the change in goods production will be reflected the next day.
        }

        for (Railway railway : allRailways.values()) {
            model.removeEdge(railway);
            railway.dailyRun();
            model.addEdge(railway);
        }
    }
}
