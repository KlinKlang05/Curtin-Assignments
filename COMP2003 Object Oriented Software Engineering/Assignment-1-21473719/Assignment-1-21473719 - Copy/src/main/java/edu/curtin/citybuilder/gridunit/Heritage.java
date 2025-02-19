package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.ConstructionMaterial;
import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

public class Heritage extends GridUnitDecorator {
    private final ConstructionMaterial heritageMaterial;

    public Heritage(GridUnit gridUnit, ConstructionMaterial heritageMaterial) throws InvalidHeritageException {
        super(gridUnit);
        if (heritageMaterial == ConstructionMaterial.CONCRETE) {
            throw new InvalidHeritageException("Heritage cannot be concrete.");
        }
        this.heritageMaterial = heritageMaterial;
    }

    @Override
    public StructureTestResult test(Structure structure) {
        StructureTestResult result = next.test(structure);

        if (result.isBuildable()) {
            if (structure.getConstructionMaterial() != heritageMaterial) {
                result.setBuildable(false);
                result.addReason(String.format("The construction material of this structure (%s) ", structure.getConstructionMaterial().name()) +
                        String.format("does not match the heritage material required in this zone (%s).", heritageMaterial.name()));
            }
        }

        return result;
    }
}
