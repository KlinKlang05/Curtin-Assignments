package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

public class Contamination extends GridUnitDecorator {
    public Contamination(GridUnit gridUnit) {
        super(gridUnit);
    }

    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = next.test(structure);
        if (result.isBuildable()) {
            result.addMultiplier(1.5);
        }

        return result;
    }
}
