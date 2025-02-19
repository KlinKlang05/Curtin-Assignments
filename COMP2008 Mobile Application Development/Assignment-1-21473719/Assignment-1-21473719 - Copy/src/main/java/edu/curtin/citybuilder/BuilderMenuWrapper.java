package edu.curtin.citybuilder;

import java.util.List;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Wrapper class
 */
public class BuilderMenuWrapper {
    private static final Logger logger = Logger.getLogger("Logger");
    private ConstructionApproach approach = ConstructionApproach.RANDOM;
    private CityBuilder builder;
    private Scanner scanner;

    public BuilderMenuWrapper(CityBuilder builder) {
        this.builder = builder;
        this.scanner = new Scanner(System.in);
    }

    /**
     * Displays the main menu
     */
    public void displayMenu() {
        boolean exitStatus = false;

        try (Scanner scanner = new Scanner(System.in)) {
            while (!exitStatus) {
                System.out.println("Welcome to OOSE city Planner 2024 By Kevin Kongo.\n");


                for (String op : List.of("1. Build Structure", "2. Build City", "3. Configure", "4. Quit")) {
                    System.out.println(op);
                }

                int selection = promptForInt("Please select an option (1-4): ", scanner, 1, 4);

                switch (selection) {
                    case 1:
                        runBuildStruct();
                        break;
                    case 2:
                        runBuildCity();
                        break;
                    case 3:
                        runConfig();
                        break;
                    case 4:
                        System.out.println("Quitting... ");
                        exitStatus = true;
                        break;

                    default:
                        throw new AssertionError("Should not allow the user to enter any other number.");
                }
            }
        }
    }


    private void runBuildStruct() {
        System.out.println("Test the construction of a Structure at a grid location in the City");

        int x = promptForInt(String.format("\nSelect the x position on the City Grid (0 - %d): ", builder.getX() - 1),
                scanner, 0, builder.getX() - 1);

        int y = promptForInt(String.format("\nSelect the y position on the City Grid (0 - %d): ", builder.getY() - 1),
                scanner, 0, builder.getY() - 1);

        Structure attributes = promptForStructure(scanner);

        StructureTestResult result = builder.buildStructure(x, y, attributes);

        System.out.println("\n\nDisplaying results: ");
        if (result.isBuildable()) {
            System.out.printf("The structure can be built on grid location %d, %d, at a cost of $%.2f.\n", x, y, result.getCost());
        } else {
            System.out.printf("The structure cannot be built on grid location %d, %d. Reason:\n %s\n", x, y, result.getReason());
        }

        System.out.printf("Press enter to continue:");
        scanner.nextLine();
    }

    private void runBuildCity() {
        StructureTestResult[][] results = switch (approach) {
            case ConstructionApproach.CUSTOM -> builder.customBuildCity();
            case ConstructionApproach.RANDOM -> builder.randomBuildCity();
            case ConstructionApproach.UNIFORM -> {
                Structure attributes = promptForStructure(scanner);
                yield builder.buildCity(attributes);
            }
            default -> throw new AssertionError("the approach attribute should be set.");
        };

        StringBuilder gridResult = new StringBuilder();
        int successCount = 0;
        double totalCost = 0;

        for (StructureTestResult[] outerResult : results) {
            for (StructureTestResult innerResult : outerResult) {
                if (innerResult.isBuildable()) {
                    gridResult.append("X");
                    successCount += 1;
                    totalCost += innerResult.getCost();
                } else {
                    gridResult.append(" ");
                }
            }
            gridResult.append("\n");
        }

        System.out.printf("\nResults:\nTotal structures able to be built: %d\nTotal cost of buildable structures: $%.2f\n\n %s", successCount, totalCost, gridResult);

        System.out.println("\n\nPress enter to continue: ");
        scanner.nextLine();
    }

    private void runConfig() {
        int selection = promptForInt(String.format("\nPlease select a Construction Approach for the city: \n0. Custom: %s \n1. Random\n2. Uniform\n: ", builder.getCustomBuilderTitle()),
                scanner, 0, 2);

        approach = ConstructionApproach.values()[selection];
        System.out.printf("Value changed to %s\n", approach.name());

        System.out.println("\nPress enter to continue: ");
        scanner.nextLine();

    }

    private static Integer promptForInt(String prompt, Scanner pScanner, int lowerBound, int upperBound) {
        int value = 0;
        boolean firstTry = true;

        System.out.print(prompt);

        do {
            if (!firstTry) {
                System.out.printf("Please enter a valid option between %d and %d: ", lowerBound, upperBound);
            }
            try {
                value = Integer.parseInt(pScanner.nextLine());
            } catch (NumberFormatException exception) {
                logger.log(Level.WARNING, "Incorrect Input, expected an integer.");
            }
            firstTry = false;
        }
        while ((value < lowerBound || value > upperBound));
        return value;
    }

    private static Structure promptForStructure(Scanner scanner) {

        int floorCount = promptForInt("\nSelect the number of floors in the building: ",
                scanner, 1, Integer.MAX_VALUE);
        int fSelection = promptForInt("\nSelect 1 for slab foundation or 2 for stilt foundation: ",
                scanner, 1, 2);
        int cSelection = promptForInt("\nSelect Construction material: \n1. Wood\n2. Stone\n3. Brick\n4. Concrete\n: ",
                scanner, 1, 4);

        FoundationType foundationType = FoundationType.values()[fSelection - 1];
        ConstructionMaterial constructionMaterial = ConstructionMaterial.values()[cSelection - 1];

        return new Structure(floorCount, foundationType, constructionMaterial);
    }
}
