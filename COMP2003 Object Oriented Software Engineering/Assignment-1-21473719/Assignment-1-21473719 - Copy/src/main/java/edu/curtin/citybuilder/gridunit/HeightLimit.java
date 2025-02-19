package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

import java.security.InvalidParameterException;

public class HeightLimit extends GridUnitDecorator {
    private final int heightLimit;

    public HeightLimit(GridUnit gridUnit, int heightLimit) {
        super(gridUnit);

        if (heightLimit < 0) {
            throw new InvalidParameterException("height limit must be positive.");
        }
        this.heightLimit = heightLimit;
    }

    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = next.test(structure);

        if (result.isBuildable()) {
            if (structure.getFloorCount() > heightLimit) {
                result.setBuildable(false);
                result.addReason("This structure's floor count exceeds the floor height limit for this zone. " +
                        String.format("Proposed height: %d floors. zone limit: %d floors", structure.getFloorCount(), heightLimit));
            }
        }

        return result;
    }
}
