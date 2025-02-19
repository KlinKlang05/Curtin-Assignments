// FILE:            FiaAnalysis.java 
// AUTHOR:          Kevin Kongo
// ID:              21473719    
// UNIT:            COMP1007    
// REFERENCE:       None    
// DESCRIPTION:     Contains the main method for program two as well as some helper methods.
//                  Due to a lack of detail in the assignment specification, I chose to disregard the "Grand Prix" entry
//                  when organising data. My FiaDataEntry program by default gives all drivers the same grand prix type for the exported CSV.
//                  However, that can be changed easily later on. This program does not seperate races by Grand Prix since the 
//                  assignment does not require that we do so. As such, all entries are considered as being in the same "race" 
//                  regardless of the entry in "GrandPrix", making that value purely symbolic.
// REQUIRES:        Driver.java, Team.java, InputUtils.java, a CSV file with format (TeamName,CarCode,DriverName,GrandPrix,PositionFinished(int),FastestLap(float))
// LAST MODIFIED:   13/5/24

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class FiaAnalysis 
{
    public static void main(String[] args)
    {
        String fileName;
        String[][] csvArray = null;
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to the FIA F1 Analysis Program.");
        if(args.length == 0)
        {
            System.out.print("You did not enter a filename as an argument for the program.\nPlease enter a file to read from (ending in .csv): "); // The user can choose to pass the filename 
            fileName = InputUtils.promptForString(scanner, "", "Please Enter a valid file name ending in .csv: ");             // as an argument when running the program in terminal.
        }
        else 
        {
            fileName = args[0];   // File name can also be passed as an argument when running the program. Choice is user's.
            System.out.println("The file name you entered was: " + fileName);
        }

        csvArray = getCSVData(fileName);        // Import CSV data into a 2d array of strings.

        try
        {
            if(csvArray != null)    // Check if csv was read correctly
            {
                int driverCount = csvArray.length - 1;  // First line is a header. It is not needed.
                if(driverCount % 2 == 0) // Check if the number of entries is even. see "else" statement for explanation
                {
                    Driver[] driverArray = new Driver[driverCount];   // Create array that holds Driver objects.
                    for(int i = 1; i <= driverCount; i++)             // Then create an instance of Driver that holds the data from each line in the CSV and place it into the array.
                    {
                        driverArray[i-1] = new Driver(csvArray[i][0], csvArray[i][1], csvArray[i][2], csvArray[i][3], Integer.parseInt(csvArray[i][4]), Double.parseDouble(csvArray[i][5]));
                    }

                    Team[] teamArray = new Team[driverCount/2];     // Create an array that holds Team objects. Each Team stores two Driver objects.

                    boolean incorrectPairs = false;
                    for(int i = 0; i < driverCount/2; i++)          // This for loop checks that every second entry from the CSV is followed by an entry that holds the same team.
                    {                                               // See the comment next to the "else" statement after if(!incorrectPairs) is checked for more details.
                        if(driverArray[i*2].getTeamName().equals(driverArray[i*2+1].getTeamName())) 
                        {
                            teamArray[i] = new Team(driverArray[i*2], driverArray[i*2+1]);   // This is only executed if the above condition is met - no point placing it into the array 
                        }                                                                    // since the program is going to close if incorrectPairs becomes true.
                        else
                        {
                            System.out.println(driverArray[i*2].getTeamName() + " " + driverArray[i*2+1].getTeamName());
                            incorrectPairs = true;
                        }
                    }

                        if(!incorrectPairs)
                        {
                            sortDriverArray(driverArray);
                            sortTeamArray(teamArray);

                            System.out.print("Enter 1 for all teams analysis or 2 for single team. Enter 0 to exit: ");
                            
                            int selection = InputUtils.getCorrectInt(scanner);
                            while(selection < 0 || selection > 2)
                            {
                                System.out.print("Enter 0/1/2 only.");
                                selection = InputUtils.getCorrectInt(scanner);
                            }

                            while(selection != 0)       // If the selection becomes zero, the user is done analysing the file and the program closes.
                            {
                                if(selection == 1)      // If selection is one, the first set of analysis is presented as required in the assignment spec.
                                {
                                    System.out.println("The following Team Data is displayed in order of fastest to slowest. Each team consists of two drivers.");
                                    for(int i = 0; i < driverCount/2; i++)      
                                    {                                                         // This for loop is responsible for satisfying the FIRST FOUR dot points                                                           
                                        switch(teamArray[i].getNumCompleted())                // under "Data Analysis System" which is under "Program Two" in the assignment spec.                                                  
                                        {                                                                                                             
                                            case 0:
                                                System.out.println("This team did not complete the race: ");
                                                break;
                                            case 1: 
                                                System.out.println("Only One Driver completed the race in this team. The one that did not complete the race was assigened a time of 205.5 seconds: ");
                                                break;
                                            case 2:
                                                System.out.println("Both Drivers completed the race: ");          
                                                break;
                                            default:
                                                System.out.println("It is impossible to print this. How..? You got an error somewhere buddy. ");                   
                                                break;
                                        }
                                        System.out.print("\tDriver One: " + teamArray[i].getDriverOne().toString());
                                        System.out.print("\tDriver Two: " + teamArray[i].getDriverTwo().toString());
                                        System.out.println("\tTime: " + teamArray[i].getLapSum() + "\n");
                                    }

                                    System.out.println("Fastest Drivers descending order. Drivers that did not complete the race are given a time of 205.5 seconds (this isn't reflected in the output): ");
                                    for(int i = 0; i < driverCount; i++)                        
                                    {                                                               // This for loop is responsible for satisfying the SECOND LAST dot point              
                                        System.out.println("\t" + driverArray[i].toString());       // under "Data Analysis System" which is under "Program Two" in the assignment spec.             
                                    }

                                    System.out.println("\nFastest Drivers ascending order. Drivers that did not complete the race are given a time of 205.5 seconds: ");
                                    for(int i = driverCount-1; i >=0; i--)
                                    {                                                              // This for loop is responsible for satisfying the LAST dot point            
                                        System.out.println("\t" + driverArray[i].toString());      // under "Data Analysis System" which is under "Program Two" in the assignment spec. 
                                    }
                                }
                                else if(selection == 2)     // If selection is two, the user will select a car code to filter by. This is the equivalent of searching for a particular team
                                {                           // since, based on my limited knowledge of F1, I am assuming each team has a different car code. 
                                    System.out.print("Enter team car code to filter by: ");
                                    String carCodeSelection = InputUtils.promptForString(scanner, "", "Please enter a valid car code: ");
                                    
                                    boolean foundSomething = false;
                                    for(int i = 0; i < driverCount; i++)
                                    {                                                               // This for loop satisfies the ONLY dot point under "Team Analysis" Which is under "Program Two"
                                        if(driverArray[i].getCarCode().equals(carCodeSelection))    // in the assignment spec.
                                        {
                                            foundSomething = true;
                                            System.out.println(driverArray[i].toString());      // Prints straight from the Driver array. This is because the Driver array was already sorted
                                        }                                                       // earlier. So going through the array sequentially and picking out matching car codes 
                                    }                                                           // will by default display the fastest car first. 
                                    
                                    if(!foundSomething)             // This displays to the user if the car code they entered was not found across all the drivers.
                                    {
                                        System.out.println("\nCould not find any drivers with that car code.\n");
                                    }
                                }
                                
                                System.out.print("Enter 1 for all teams analysis or 2 for single team. Enter 0 to exit: ");     // Check if the user wants to continue analysis.
                                
                                selection = InputUtils.getCorrectInt(scanner);
                                while(selection < 0 || selection > 2)
                                {
                                    System.out.print("Enter 0/1/2 only: ");
                                    selection = InputUtils.getCorrectInt(scanner);
                                }
                            }
                        }
                        else    // Each driver in a team should be placed next to each other in the array. The FiaDataEntry program does that by default.
                        {
                            System.out.println("Each consecutive pair of entries should be of the same team. No single driver teams. Ensure team members are not scattered around the CSV. Try importing a correct CSV.");
                        }
                }
                else    // CSV should have an even number of entries (Not including the header) As there are always two drivers per team.
                {
                    System.out.println("Uneven entries in CSV file. This indicates there are not two drivers per team in the CSV. Try Importing a Correct CSV.");
                }
            }
        }
        catch(NumberFormatException exception)  // The number values in the CSV were not numbers.
        {
            System.err.println("Please ensure PositionFinished is an integer in your CSV file (and is not empty). Ensure FastestLap is a positive decimal number.");
            scanner.close();
        }
        catch(Exception exception2)             // Some other exception that occured. This is mainly to close the scanner if an error occurs.
        {
            System.err.println("An unknown Error occured. Details: \n\n" + exception2.getMessage() + "\nOccured on Line: " + exception2.getStackTrace()[0].getLineNumber() +"\n");
            
            scanner.close();
        }
        
        scanner.close();
    }
    
    // Used to get the length of the file. Adapted from COMP1007 Module 8 Slideshow Page 30.
    // RETURNS null if there was an issue.
    private static String[][] getCSVData(String pFileName)
    {                   
        FileInputStream fileStream = null;
        InputStreamReader isr;
        BufferedReader bufRdr; 
        int lineCount;
        String line;
        String[][] arrayOut = null;

        try                                   
        {                     
            fileStream = new FileInputStream(pFileName);    // Create first stream
            isr = new InputStreamReader(fileStream);
            bufRdr = new BufferedReader(isr);
            lineCount = 1;                  // Initialize lineCount to 1 because we're incrementing lineCount for the first time AFTER the second line is read.
            line = bufRdr.readLine();       // get the first line to know EOF state

            boolean hitWhiteSpace = false;
            while(line != null)             // This loop is to get number of lines in the file.
            {   
                if(!hitWhiteSpace)
                {
                    line = bufRdr.readLine();
                    if(line.length() == 0)
                    {
                        hitWhiteSpace = true;     // Check if this is an empty line of whitespace in the CSV. Stop reading in lines if this is the case. 
                    }                             
                    else 
                    {
                        lineCount++;
                    }
                }                                 // I'd call break here because we don't need to be reading from the file anymore but... not allowed :sobbing:
                else
                {
                    line = bufRdr.readLine();
                }
            }
            fileStream.close();

            String[][] csvArray = new String[lineCount][6];  // Initialize the array using the now-known number of lines in the file.

            fileStream.close();                              // Close the old stream..
            fileStream = new FileInputStream(pFileName);     // Then create a new stream to reset the buffer.
            isr = new InputStreamReader(fileStream);
            bufRdr = new BufferedReader(isr);

            boolean incorrectEntries = false;
            for(int i = 0; i < lineCount; i++)      // Loop through the file again, splitting each line and placing it into csvArray
            {
                line = bufRdr.readLine();
                line.strip();                       // Strip the line of any trailing and leading white space.
                csvArray[i] = line.split(",");      // Split each line by every comma and place the returned array into each entry of csvArray
                if (csvArray[i].length < 6)         // Ensures that each line contains six unique entries separated by commas...
                {   
                    System.out.println("Your CSV file does not have at least 6 unique entries per line. Please import a CSV following the correct format.");
                    incorrectEntries = true;        // ... and sets incorrectEntries to true if that is not the case.
                }
                else
                {
                    for(int j = 0; j < 6; j++) // Loop through the subarray in csvArray...
                    {
                        if(csvArray[i][j].strip().isEmpty()) // ...and check if each entry has a String that isn't empty or filled with only whitespace.
                        {
                            System.out.println("Your CSV file has unpopulated entries. Please ensure each entry is filled.");
                            incorrectEntries = true;         
                        }
                    }
                }
            }
            fileStream.close();

            if(!incorrectEntries)                   // Only if there are no incorrect entries is csvArray copied into arrayOut which is returned,
            {                                       // otherwise arrayOut remains as null and is returned as such, allowing the program to quit.
                arrayOut = csvArray;
            }
        }
        catch(IOException errorDetails)             // error handling if the file does not exist or there were issues reading it.
        {
            if(fileStream != null) 
            {
                try
                {
                    fileStream.close();
                }
                catch(IOException ex2) 
                { }
            }
            System.out.println("Error in Processing file: " + errorDetails.getMessage() + ". Please try again.");
        }

        return arrayOut;
    }
    
    // Used to sort the Team array via bubble sort. Does so by getting the sum of whatever is returned by
    // getFastestLap() on the driverOne and driverTwo attributes.
    private static void sortTeamArray(Team[] pTeamArray)
    {
        int length = pTeamArray.length;
        for(int i = 0; i < length; i++)
        {
            for(int j = 0; j < (length - i-1); j++)
            {
                if(pTeamArray[j].getLapSum() > pTeamArray[j+1].getLapSum())    // Bubble sort
                {
                    Team temp = pTeamArray[j];
                    pTeamArray[j] = pTeamArray[j+1];
                    pTeamArray[j+1] = temp;
                }
            }
        }

    }

    // Used to sort the Driver array via bubble sort. Sorts based on what is returned by getFastestLap(). 
    // However, it first checks if the driver finished the race using getPosFinish(). If The Driver did 
    // not finish the race (getPosFinish returns a negative value), then the Driver is sorted based on an allocated time of 205.5s
    private static void sortDriverArray(Driver[] pDriverArray)
    {
        double timeA;
        double timeB;
        int length = pDriverArray.length;
        for(int i = 0; i < length; i++)
        {
            for(int j = 0; j < (length - i-1); j++)
            {
                if(pDriverArray[j].getPosFinish() < 0)
                {
                    timeA = 205.5d;                     // Give first driver a time of 205.5 seconds if they didn't finish the race...
                }
                else 
                {
                    timeA = pDriverArray[j].getFastestLap();    // ...Otherwise use their fastest lap
                }

                if(pDriverArray[j+1].getPosFinish() < 0)
                {
                    timeB = 205.5d;                    // Same for the second driver.
                }
                else
                {
                    timeB = pDriverArray[j+1].getFastestLap();
                }

                if(timeA > timeB)       // Basic bubble sort
                {
                    Driver temp = pDriverArray[j];
                    pDriverArray[j] = pDriverArray[j+1];
                    pDriverArray[j+1] = temp;
                }
            }
        }
    }
}
