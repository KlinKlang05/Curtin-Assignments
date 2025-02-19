package edu.curtin.citybuilder;

public enum ConstructionMaterial {
    WOOD(10000d),
    STONE(50000d),
    BRICK(30000d),
    CONCRETE(20000d);

    public final double materialCost;

    ConstructionMaterial(double cost) {
        this.materialCost = cost;
    }
}
