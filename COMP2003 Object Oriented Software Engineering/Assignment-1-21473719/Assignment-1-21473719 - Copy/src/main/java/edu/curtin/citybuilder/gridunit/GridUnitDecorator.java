package edu.curtin.citybuilder.gridunit;

import edu.curtin.citybuilder.Structure;
import edu.curtin.citybuilder.StructureTestResult;

public abstract class GridUnitDecorator implements GridUnit {
    protected final GridUnit next;

    public GridUnitDecorator(GridUnit gridUnit) {
        this.next = gridUnit;
    }

    @Override
    public StructureTestResult test(Structure structure) {
        return next.test(structure);
    }

}
