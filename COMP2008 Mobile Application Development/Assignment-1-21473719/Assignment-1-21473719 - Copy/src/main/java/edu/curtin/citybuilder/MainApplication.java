package edu.curtin.citybuilder;

/**
 * Entry point into the application. To change the package, and/or the name of this class, make
 * sure to update the 'mainClass = ...' line in build.gradle.
 */
public class MainApplication {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Please add a filename to the arguments for the program.");
        } else {
            try {
                DataFileIO dataReader = new DataFileIO();
                OOSECityBuilder builder = dataReader.generateCityFromFile(args[0]);

                if (builder != null) {
                    BuilderMenuWrapper mainMenu = new BuilderMenuWrapper(builder);
                    mainMenu.displayMenu();
                } else {
                    System.out.println("\n\nCity could not be generated.");
                }

            } catch (InvalidFileFormatException e) {
                System.out.println("File format incorrect:\n\n" + e.getMessage());
            }
        }
    }
}
