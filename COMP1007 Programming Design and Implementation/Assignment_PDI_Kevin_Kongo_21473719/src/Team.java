// FILE:            Team.java 
// AUTHOR:          Kevin Kongo
// ID:              21473719    
// UNIT:            COMP1007    
// REFERENCE:       None    
// DESCRIPTION:     Contains the Team class for use in Program two for Assignment 1 COMP1007
// REQUIRES:        None
// LAST MODIFIED:   12/5/24

public class Team 
{
    // Class fields
    private String teamName;
    private Driver driverOne;
    private Driver driverTwo;

    // Constructor with parameters
    public Team(Driver pDriverOne, Driver pDriverTwo)
    {
        this(); // initializes with default values, and attributes are updated after checking
                // if classes are equal. If they are not, values stay default.
        if(pDriverOne.getTeamName().equals(pDriverTwo.getTeamName()))
        {
            teamName = pDriverOne.getTeamName();
            driverOne = pDriverOne;
            driverTwo = pDriverTwo;
        }
    }

    // Copy Constructor
    public Team(Team pTeam)
    {
        teamName = pTeam.getTeamName();
        driverOne = pTeam.getDriverOne();
        driverTwo = pTeam.getDriverTwo();
    }

    // Default Constructor
    public Team()
    {
        teamName = "DefaultTeam";
        driverOne = new Driver();
        driverTwo = new Driver();
    }

    // getter methods
    public String getTeamName()
    {
        return teamName;
    }

    public Driver getDriverOne()
    {
        return driverOne;
    }

    public Driver getDriverTwo()
    {
        return driverTwo;
    }

    // setter methods
    public void setTeamName(String pTeamName)
    {
        if(pTeamName.length() != 0)
        {
            teamName = pTeamName;
        }
    }

    public void setDriverOne(Driver pDriverOne)
    {
        if(pDriverOne != null)
        {
            driverOne = pDriverOne;
        }
    }

    public void setDriverTwo(Driver pDriverTwo)
    {
        if(pDriverTwo != null)
        {
            driverTwo = pDriverTwo;
        }
    }

    // toString method
    public String toString()
    {
        String stringOut = "Team: " + teamName + ", Driver One: " + driverOne.getDriverName() + ", Driver Two: " + driverTwo.getDriverName();
        
        return stringOut;
    }

    // equals method
    public boolean equals(Object inObject)
    {
        boolean isEqual = false;
        if(inObject instanceof Team)
        {
            Team teamObject = (Team)inObject;
            if(teamObject.getTeamName() == teamName)
            {
                if(teamObject.getDriverOne().equals(driverOne))
                {
                    if(teamObject.getDriverTwo().equals(driverTwo))
                    {
                        isEqual = true;
                    }
                }
            }
        }

        return isEqual;
    }

    public int getNumCompleted()
    // Returns the number of drivers who completed the race (integer), i.e. the number of drivers who's
    // PosFinish attribute is not a negative number.
    {
        int numCompleted = 0;
        if(driverOne.getPosFinish() > 0)  // driver one
        {
            numCompleted += 1;
        }
        if(driverTwo.getPosFinish() > 0)  // driver two
        {
            numCompleted += 1;
        }

        return numCompleted;
    }

    public double getLapSum()
    // Returns the sum of both driver's fastest lap (double). If they did not complete the race, their
    // time is assigned as 205.5 seconds.
    {
        double lapSum = 0.0d;
        if(driverOne.getPosFinish() < 0)  // driver one
        {
            lapSum += 205.5d;
        }
        else
        {
            lapSum += driverOne.getFastestLap();
        }

        if(driverTwo.getPosFinish() < 0) // driver two
        {
            lapSum += 205.5d;
        }
        else
        {
            lapSum += driverTwo.getFastestLap();
        }

        return lapSum;
    }
}
