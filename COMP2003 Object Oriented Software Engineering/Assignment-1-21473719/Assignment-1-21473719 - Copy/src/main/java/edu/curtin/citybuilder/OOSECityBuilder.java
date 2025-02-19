package edu.curtin.citybuilder;

import edu.curtin.citybuilder.gridunit.GridUnit;

import java.security.InvalidParameterException;
import java.util.List;
import java.util.Random;

public class OOSECityBuilder implements CityBuilder {
    private static final int RANDOM_MAX_FLOORS = 20; // I feel like a 20-story building is quite reasonable
    private final GridUnit[][] cityGrid;

    @Override
    public int getX() {
        return cityGrid.length;
    }

    @Override
    public int getY() {
        return cityGrid[0].length;
    }

    public OOSECityBuilder(GridUnit[][] grid) {
        if (grid != null) {
            if (grid.length != 0) {
                cityGrid = grid;
                return;
            }
        }
        throw new InvalidParameterException("GridUnit[][] must not be null and must not be empty.");
    }

    @Override
    public StructureTestResult buildStructure(int x, int y, int floorCount, FoundationType foundationType, ConstructionMaterial material) {
        Structure str = new Structure(floorCount, foundationType, material);
        buildStructure(x, y, str);
        return null;
    }

    @Override
    public List<StructureTestResult> buildCity(int floorCount, FoundationType foundationType, ConstructionMaterial material) {
        Structure str = new Structure(floorCount, foundationType, material);
        buildCity(str);
        return null;
    }

    @Override
    public StructureTestResult buildStructure(int x, int y, Structure structure) {
        return cityGrid[x][y].test(structure);
    }

    @Override
    public StructureTestResult[][] buildCity(Structure structure) {
        StructureTestResult[][] results = new StructureTestResult[cityGrid.length][cityGrid[0].length];

        for (int i = 0; i < cityGrid.length; i++) {
            for (int j = 0; j < cityGrid[0].length; j++) {
                results[i][j] = cityGrid[i][j].test(structure);
            }
        }
        return results;
    }

    @Override
    public StructureTestResult[][] customBuildCity() {
        double height = cityGrid.length;
        double width = cityGrid[0].length;
        StructureTestResult[][] results = new StructureTestResult[cityGrid.length][cityGrid[0].length];

        for (double i = 0; i < cityGrid.length; i++) {
            for (double j = 0; j < cityGrid[0].length; j++) {
                double firsthalf = Math.pow((i - ((height - 1d) / 2d)), 2);
                double secondhalf = Math.pow((j - ((width - 1d) / 2d)), 2);

                double distance = Math.sqrt(firsthalf + secondhalf);

                int nFloors = (int) Math.round(distance);

                ConstructionMaterial material;
                if (distance <= 2) {
                    material = ConstructionMaterial.CONCRETE;
                } else if (distance > 2 && distance <= 4) {
                    material = ConstructionMaterial.BRICK;
                } else if (distance > 4 && distance <= 6) {
                    material = ConstructionMaterial.STONE;
                } else {
                    material = ConstructionMaterial.WOOD;
                }

                Structure testStructure = new Structure(nFloors, FoundationType.SLAB, material);

                results[(int) i][(int) j] = cityGrid[(int) i][(int) j].test(testStructure);
            }
        }
        return results;
    }

    @Override
    public String getCustomBuilderTitle() {
        return "Test city build using structures generated based on distance from the centre of the grid.";
    }

    @Override
    public StructureTestResult[][] randomBuildCity() {
        Random random = new Random();
        StructureTestResult[][] results = new StructureTestResult[cityGrid.length][cityGrid[0].length];

        for (int i = 0; i < cityGrid.length; i++) {
            for (int j = 0; j < cityGrid[0].length; j++) {
                int floorCount = random.nextInt(1, RANDOM_MAX_FLOORS);
                int foundationIndex = random.nextInt(FoundationType.values().length);
                int materialIndex = random.nextInt(ConstructionMaterial.values().length);

                Structure randomStructure = new Structure(floorCount, FoundationType.values()[foundationIndex], ConstructionMaterial.values()[materialIndex]);

                results[i][j] = cityGrid[i][j].test(randomStructure);
            }
        }
        return results;
    }
}
