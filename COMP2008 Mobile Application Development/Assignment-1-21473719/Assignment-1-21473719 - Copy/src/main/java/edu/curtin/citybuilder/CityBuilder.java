package edu.curtin.citybuilder;

import java.util.List;

/**
 * this interface allows different implementations of a city builder to be passed to wrapper classes or other calling
 * methods. This allows for the implementing class to implement their own way of storing a city grid
 * (If this was real world software, for OOSE we only have one class implementing this method).
 */
public interface CityBuilder {
    StructureTestResult buildStructure(int x, int y, int floorCount, FoundationType foundationType, ConstructionMaterial material);

    List<StructureTestResult> buildCity(int floorCount, FoundationType foundationType, ConstructionMaterial material);

    StructureTestResult buildStructure(int x, int y, Structure structure);

    /**
     * Test the build of a city using the provided structure data, build the same structure on every grid in the city
     */
    StructureTestResult[][] buildCity(Structure structure);

    /**
     * Test the build of a city using a different randomly generated structure for each grid in the city.
     */
    StructureTestResult[][] randomBuildCity();

    /**
     * Test the build of a city using a special method. Depends on the implementing method.
     */
    StructureTestResult[][] customBuildCity();

    /**
     * Get a string that identifies/describes the customBuildCity() method that the implementing class has chosen.
     */
    String getCustomBuilderTitle();

    /**
     * get the height of the city grid.
     */
    int getX();

    /**
     * get the width of the city grid.
     */
    int getY();
}
