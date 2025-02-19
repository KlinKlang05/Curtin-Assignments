package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

import java.security.InvalidParameterException;

public class FloodRisk extends GridUnitDecorator {
    private final double risk;

    public FloodRisk(GridUnit gridUnit, double risk) {
        super(gridUnit);

        if (risk < 0d || risk > 100d) {
            throw new InvalidParameterException("the risk value must be between 0 and 100 inclusive.");
        }
        this.risk = risk;
    }

    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = next.test(structure);

        if (result.isBuildable()) {
            if (structure.getFloorCount() < 2) {
                result.setBuildable(false);
                result.addReason("The structure must be at least two floors to be built in a flood-risk zone.");
            } else {
                result.addMultiplier(1 + (risk / 50));
                result.addReason("The structure has at least two floors, and can be built on a high flood risk zone.");
            }
        }

        return result;
    }
}
