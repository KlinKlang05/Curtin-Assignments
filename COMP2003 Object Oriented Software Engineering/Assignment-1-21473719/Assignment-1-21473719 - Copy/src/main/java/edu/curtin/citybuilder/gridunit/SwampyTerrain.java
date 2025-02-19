package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.ConstructionMaterial;
import edu.curtin.citybuilder.FoundationType;
import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

public class SwampyTerrain implements GridUnit {
    private static final double ADD_COST_PER_FLOOR = 20000d;

    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = new StructureTestResult();

        if (structure.getFoundationType() == FoundationType.SLAB) {
            result.setBuildable(false);
            result.addReason("Structures with a slab foundation are not supported in swampy terrain.");
        } else if (structure.getConstructionMaterial() == ConstructionMaterial.WOOD) {
            result.setBuildable(false);
            result.addReason("Structures with a wooden construction material are not supported in swampy terrain.");
        } else {
            double floorCost = structure.getConstructionMaterial().materialCost;
            result.addCost(structure.getFloorCount() * (floorCost + ADD_COST_PER_FLOOR));
        }


        return result;
    }
}
