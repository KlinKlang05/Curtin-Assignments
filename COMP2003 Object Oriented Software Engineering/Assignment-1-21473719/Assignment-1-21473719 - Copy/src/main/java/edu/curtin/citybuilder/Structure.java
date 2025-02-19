package edu.curtin.citybuilder;

import java.security.InvalidParameterException;

public class Structure {
    private int floorCount;
    private FoundationType foundationType;
    private ConstructionMaterial constructionMaterial;

    public Structure(int floorCount1, FoundationType foundationType1, ConstructionMaterial constructionMaterial1) {
        if (floorCount1 == 0 || foundationType1 == null || constructionMaterial1 == null) {
            throw new InvalidParameterException("All parameters must be set when initializing a Structure object");
        }

        floorCount = floorCount1;
        foundationType = foundationType1;
        constructionMaterial = constructionMaterial1;

    }

    public int getFloorCount() {
        return floorCount;
    }

    public FoundationType getFoundationType() {
        return foundationType;
    }

    public ConstructionMaterial getConstructionMaterial() {
        return constructionMaterial;
    }
}
