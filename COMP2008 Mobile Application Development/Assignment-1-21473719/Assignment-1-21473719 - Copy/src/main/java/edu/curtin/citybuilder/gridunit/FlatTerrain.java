package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

public class FlatTerrain implements GridUnit {
    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = new StructureTestResult();

        result.setBuildable(true);

        double floorCost = structure.getConstructionMaterial().materialCost;
        result.addCost(structure.getFloorCount() * floorCost);

        return result;
    }
}
