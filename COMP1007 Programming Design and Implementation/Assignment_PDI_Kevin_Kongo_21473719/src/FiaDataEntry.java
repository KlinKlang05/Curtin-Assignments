// FILE:            FiaDataEntry.java 
// AUTHOR:          Kevin Kongo
// ID:              21473719    
// UNIT:            COMP1007    
// REFERENCE:       None    
// DESCRIPTION:     Contains the main method for program one as well as some helper methods.
// REQUIRES:        Driver.java, InputUtils.java
// LAST MODIFIED:   13/5/24

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;

public class FiaDataEntry 
{
    public static void main(String[] args)
    {
        // initialize Scanner 
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to the FIA F1 Data Entry Program.\n");
        int numTeams = 0;
        do  // Get the number of drivers to save into file, by entering the number of teams. Perform error checking on entered value.
        {
            System.out.print("Select number of Teams to save (remember two drivers per team): ");
            numTeams = InputUtils.getCorrectInt(scanner);   
        }
        while(numTeams < 1);
        
        int numDrivers = numTeams * 2;                  // get number of Drivers after asking for number of teams. Two drivers per team.
        Driver [] driverArray = new Driver[numDrivers]; // initialize Driver array

        // The following lines are used to gather user input to fill the fields in each entry of the Driver array
        String tempTeamName = null;
        String tempCarCode = null;

        System.out.println("\nPlease Enter the following: ");
        String grandPrix = InputUtils.promptForString(scanner, "Enter the Grand Prix the teams are racing in: ", "Please Enter a valid Grand Prix: ");

        for(int i = 0; i < numDrivers; i++)
        {
            driverArray[i] = new Driver();
            if(i % 2 == 0)
            {
                System.out.println("\n---Team " + (i+1) + "---");
                tempTeamName = InputUtils.promptForString(scanner, "Enter Team name: ", "Please enter a valid team name: ");
                tempCarCode = InputUtils.promptForString(scanner, "Car code: ", "Please enter a valid car code: ");
            }
            else 
            {
                System.out.println("\nPlease enter the details for Driver Two in Team " + tempTeamName + ", Car Code " + tempCarCode);
            }

            driverArray[i].setTeamName(tempTeamName);
            driverArray[i].setCarCode(tempCarCode);
            driverArray[i].setDriverName(InputUtils.promptForString(scanner, "Driver name: ", "Please enter a valid driver name: "));
            driverArray[i].setGrandPrix(grandPrix);
            driverArray[i].setPosFinish(promptForPos(scanner));
            driverArray[i].setFastestLap(promptForTime(scanner));
        }

        // Display currently entered data and ask if user wants to make edits.
        System.out.println("This is the current data: ");
        for(int i = 1; i <= numDrivers; i++)
        {
            System.out.println("Driver " + i + ": " + driverArray[i-1].toString());
        }

        System.out.print("If you would like to edit any data before saving to CSV, enter the driver number. Otherwise, enter 0.");
        int editSelection = InputUtils.getCorrectInt(scanner);
        while(editSelection < 0 || editSelection > numDrivers){
            System.out.print("please enter an actual Driver number from the list above: ");
            editSelection = InputUtils.getCorrectInt(scanner);
        }

        while(editSelection != 0)
        {
            System.out.print("enter 1 to edit Team Name, 2 to edit Car Code, 3 to edit Driver Name, 4 to edit Finishing Position, 5 to edit Fastest Lap, 6 to edit Grand Prix for all drivers: ");
            int fieldSelection = InputUtils.getCorrectInt(scanner);
            
            switch(fieldSelection)  // Edit the relevant attribute in the instance of the requested Driver.
            {
                case 1:
                    driverArray[editSelection - 1].setTeamName(InputUtils.promptForString(scanner, "Enter Team name: ", "Please enter a valid team name: "));
                    break;
                case 2:
                    driverArray[editSelection - 1].setCarCode(InputUtils.promptForString(scanner, "Car code: ", "Please enter a valid car code: "));
                    break;
                case 3:
                    driverArray[editSelection - 1].setDriverName(InputUtils.promptForString(scanner, "Driver name: ", "Please enter a valid driver name: "));
                    break;
                case 4:
                    driverArray[editSelection - 1].setPosFinish(promptForPos(scanner));
                    break;
                case 5:
                    driverArray[editSelection - 1].setFastestLap(promptForTime(scanner));
                    break;
                case 6:
                    String newGrandPrix = InputUtils.promptForString(scanner, "Grand Prix: ", "Please Enter a valid Grand Prix: ");
                    for(int i = 0; i < numDrivers; i++)
                    {
                        driverArray[i].setGrandPrix(newGrandPrix);
                    }
                    break;
                default:
                    System.out.println("Invalid selection. Try again. ");
                }
                System.out.print("If you would like to edit any more data before saving to CSV, enter the driver number. Otherwise, enter 0.");
                editSelection = InputUtils.getCorrectInt(scanner);
                while(editSelection < 0 || editSelection > numDrivers){
                    System.out.print("please enter an actual Driver number from the list above: ");
                    editSelection = InputUtils.getCorrectInt(scanner);
            }
        }

        String csvName = InputUtils.promptForString(scanner, "Enter CSV file name: ", "Please enter a valid CSV file name: ") + ".csv"; // Get name of CSV File.
        System.out.println("Writing...");
        writeOneRow(csvName, "TeamName", "CarCode", "DriverName", "GrandPrix", "PositionFinished", "FastestLap");   // Write the header into the CSV
        for(int i = 0; i < numDrivers; i++) // Loop through the whole driver array
        {
            writeOneRow(csvName, driverArray[i].getTeamName(), driverArray[i].getCarCode(), 
            driverArray[i].getDriverName(), driverArray[i].getGrandPrix(), 
            Integer.toString(driverArray[i].getPosFinish()), Double.toString(driverArray[i].getFastestLap()));      // Write attributes from one Driver class into the CSV.
        }

    }

    // The following static methods are used to get input from the user based on specific prompts. 
    // 12/5/24: After writing the pseudocode, I realised that I can combine a few of the static methods
    // and just pass the strings as arguments as that's all that's changing between 4 of the 6 methods.
    // 13/5/24: The aforementioned methods were moved to the InputUtils Class. This makes them accessible 
    // by both the FiaAnalysis Program and the FiaDataEntry program.

    private static int promptForPos(Scanner pScanner)
    {
        int posFinish = 0;
        do
        {   
            System.out.print("Position Finished: ");
            posFinish = InputUtils.getCorrectInt(pScanner);
        }
        while(posFinish == 0);
        return posFinish;
    }

    private static double promptForTime(Scanner pScanner)
    {
        double lapTime = -1.0d;
        do
        {
            System.out.print("Fastest Lap Time (Seconds): ");
            try
            {
                lapTime = Double.parseDouble(pScanner.nextLine());
            }
            catch(NumberFormatException exception)
            {
            System.out.println("Please ensure you are entering a positive number.");
            }
        }
        while(lapTime < 0);
        return lapTime;
    }


    // This method is used to write a single CSV line to the file. Uses the append mode of the FileOutputStream to add to the end of the file.
    private static void writeOneRow(String pFileName, String pTeamName, String pDriverName, String pCarCode, String pGrandPrix, String pPosFinish, String pFastestLap)
    {
        FileOutputStream fileStream = null;
        PrintWriter pw;
        try
        {
            fileStream = new FileOutputStream(pFileName, true);
            pw = new PrintWriter(fileStream);
            pw.println(pTeamName + "," + pDriverName + "," + pCarCode + "," + pGrandPrix + "," + pPosFinish + "," + pFastestLap);
            pw.close();
        }
        catch(IOException e)
        {
            System.out.println("Error in writing to file: " + e.getMessage());
        }
    }
}
