// FILE:            InputUtils.java 
// AUTHOR:          Kevin Kongo
// ID:              21473719    
// UNIT:            COMP1007    
// REFERENCE:       None    
// DESCRIPTION:     Contains a few static methods used to get user input. After writing the Pseudocode for this assignment,
//                  it was apparent that there is a significant amount of java-specific code to execute things such as 
//                  gathering User input. For that reason, it made sense to write a new class that performs those actions, 
//                  Allowing it to be shared across both program One and program Two, which both need these methods.
//                  I saw no need to write pseudocode for these methods as the majority of it is java-specifc code.
// REQUIRES:        Nothing
// LAST MODIFIED:   13/5/24

import java.util.Scanner;

public class InputUtils {
    public static String promptForString(Scanner pScanner, String pPromptOne, String pRePrompt) 
    {
        System.out.print(pPromptOne);
        String teamName = pScanner.nextLine();
        while(teamName.length() == 0)
        {
            System.out.print(pRePrompt);
            teamName = pScanner.nextLine();
        }
        return teamName;
    }

    // A private method used to perform error checking to ensure input is an integer.
    public static int getCorrectInt(Scanner pScanner)
    {   
        boolean validInput = false;
        int value = -100;
        while(!validInput)
        {
            try
            {
                value = Integer.parseInt(pScanner.nextLine());
                validInput = true;
            }
            catch(NumberFormatException exception)
            {
                System.out.print("Please enter an integer amount: ");
            }
        }
        return value;
    }
}
