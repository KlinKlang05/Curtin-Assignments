package edu.curtin.citybuilder;

import java.util.ArrayList;
import java.util.List;

public class StructureTestResult {
    private boolean buildable;
    private String reason;
    private double cost;
    private List<Double> multipliers;

    public StructureTestResult() {
        this.buildable = true;
        this.reason = "";
        this.cost = 0;
        multipliers = new ArrayList<>();
    }

    public boolean isBuildable() {
        return buildable;
    }

    public String getReason() {
        return reason;
    }

    public double getCost() {
        double finalCost = cost;

        for (Double m : multipliers) {
            finalCost *= m;
        }

        return finalCost;
    }

    /**
     * Once you set Buildable to false, there is no longer any point in calling this method.
     * So it will raise an IllegalStateException.
     *
     * @param buildable boolean
     */
    public void setBuildable(boolean buildable) {
        if (!this.buildable) {
            throw new IllegalStateException("This method should not be called again after setting buildable to false.");
        }

        this.buildable = buildable;
    }

    public void addCost(double cost) {
        this.cost += cost;
    }

    public void addReason(String nextReason) {
        this.reason = this.reason + "\n" + nextReason;
    }

    /**
     * Ensures that multipliers are added at the end of all the other costs.
     * It means that the decorators do not have to be initialized in a particular order.
     */
    public void addMultiplier(double multiplier) {
        multipliers.add(multiplier);
    }
}

