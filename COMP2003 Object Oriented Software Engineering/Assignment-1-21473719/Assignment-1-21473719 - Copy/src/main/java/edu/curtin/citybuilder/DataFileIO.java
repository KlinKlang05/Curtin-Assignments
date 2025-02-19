package edu.curtin.citybuilder;

import edu.curtin.citybuilder.gridunit.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.security.InvalidParameterException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Reads in a file and generates a list with the correct format as well as an array with the x and y values
 * of the dimensions. Call readDataFile() First before calling the getter methods.
 */
public class DataFileIO {
    private static final Logger logger = Logger.getLogger("Logger");
    private int linenum = 1;

    /**
     * Constructor if you want to call readDataFile() later
     */
    public DataFileIO() {
    }

    /**
     * reads a data file. Adds the necessary decorators then places all the GridUnit classes into a CityBuilder class.
     *
     * @param filename
     * @return null if the file was not read correctly. Otherwise, return a CityBuilder object.
     * @throws InvalidFileFormatException if the file exists but the layout of the data in the file is not as expected.
     */
    public OOSECityBuilder generateCityFromFile(String filename) throws InvalidFileFormatException {
        try (var reader = new BufferedReader(new FileReader(filename))) {
            String unsplitLine = reader.readLine();
            if (unsplitLine == null) {
                throw new InvalidFileFormatException("File is empty.");
            }

            String[] firstLine = unsplitLine.split(",");


            if (firstLine.length != 2) {
                throw new InvalidFileFormatException("Your file " + filename + " did not properly define the number of rows and columns.");
            }

            int x = Integer.parseInt(firstLine[0]);
            int y = Integer.parseInt(firstLine[1]);

            if (x == 0 || y == 0) {
                throw new InvalidFileFormatException("The grid dimensions can't be zero.");
            }

            GridUnit[][] gridUnits = new GridUnit[x][y];

            String nextLine = reader.readLine();
            for (int j = 0; j < x; j++) {
                for (int k = 0; k < y; k++) {
                    linenum += 1;
                    if (nextLine == null) {
                        throw new InvalidFileFormatException(String.format("File finished at line %d, expected %d lines", linenum, x * y));
                    }
                    String[] splitLine = nextLine.split(",");

                    GridUnit nextItem = switch (splitLine[0].toLowerCase()) {
                        case "flat" -> new FlatTerrain();
                        case "swampy" -> new SwampyTerrain();
                        case "rocky" -> new RockyTerrain();
                        default ->
                                throw new InvalidFileFormatException(String.format("invalid Terrain Type on line %d", linenum));
                    };

                    for (int i = 1; i < splitLine.length; i++) {
                        String[] subLine = splitLine[i].split("=");

                        nextItem = switch (subLine[0].toLowerCase()) {
                            case "heritage" -> new Heritage(nextItem, matchStringToMaterial(subLine[1]));
                            case "height-limit" -> new HeightLimit(nextItem, Integer.parseInt(subLine[1]));
                            case "flood-risk" -> new FloodRisk(nextItem, Double.parseDouble(subLine[1]));
                            case "contamination" -> {
                                if (subLine.length > 1) {
                                    throw new InvalidFileFormatException(String.format("Contamination should not have any data associated with it, line %d", linenum));
                                } else {
                                    yield new Contamination(nextItem);
                                }
                            }
                            default ->
                                    throw new InvalidFileFormatException(String.format("Invalid Zoning rule on line %d", linenum));
                        };

                    }

                    gridUnits[j][k] = nextItem;

                    nextLine = reader.readLine();
                }
            }

            return new OOSECityBuilder(gridUnits);

        } catch (IOException e) {
            logger.log(Level.WARNING, () -> "File '%s' could not be read properly." + filename);
            System.out.println("File could not be read properly. It may not exist.");
        } catch (NumberFormatException e) { // Tried to convert a string to int and didn't work
            logger.log(Level.WARNING, e::getMessage);
            System.out.printf("Expected a number at line %d in file '%s'", linenum, filename);
        } catch (InvalidHeritageException e) {
            logger.log(Level.WARNING, e::getMessage);
            System.out.printf("Invalid Heritage on line %d in file '%s'", linenum, filename);
        } catch (ArrayIndexOutOfBoundsException e) {
            logger.log(Level.WARNING, e::getMessage);
            System.out.printf("Expected a value after the equals sign on line %d in file '%s'", linenum, filename);
        } catch (InvalidParameterException e) {
            logger.log(Level.WARNING, e::getMessage);
            System.out.printf("error reading line %d: '%s'", linenum, e.getMessage());
        } finally {
            linenum = 1;
        }
        return null;
    }

    private ConstructionMaterial matchStringToMaterial(String s) throws InvalidFileFormatException {
        return switch (s.toLowerCase()) {
            case "wood" -> ConstructionMaterial.WOOD;
            case "stone" -> ConstructionMaterial.STONE;
            case "brick" -> ConstructionMaterial.BRICK;
            default ->
                    throw new InvalidFileFormatException(String.format("Invalid Heritage value at line %d", linenum));
        };
    }
}
