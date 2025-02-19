package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

public class RockyTerrain implements GridUnit {
    private static final double BASE_COST = 50000d;

    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = new StructureTestResult();

        result.setBuildable(true);

        double floorCost = structure.getConstructionMaterial().materialCost;
        result.addCost(BASE_COST + (structure.getFloorCount() * floorCost));

        return result;
    }
}
