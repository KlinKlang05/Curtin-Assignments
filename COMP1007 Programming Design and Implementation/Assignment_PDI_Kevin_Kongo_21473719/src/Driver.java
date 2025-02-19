// FILE:            Driver.java 
// AUTHOR:          Kevin Kongo
// ID:              21473719    
// UNIT:            COMP1007    
// REFERENCE:       None    
// DESCRIPTION:     Contains the Driver class for use in Program One and Program two for Assignment 1 COMP1007
// REQUIRES:        None
// LAST MODIFIED:   12/5/24

public class Driver 
{
    // Class fields
    private String teamName;
    private String carCode;
    private String driverName;
    private String grandPrix;
    private int posFinish;
    private double fastestLap;

    // Constructor with parameters 
    public Driver(String pTeamName, String pCarCode, String pDriverName, String pGrandPrix, int pPosFinish, double pFastestLap)
    {
        // Performs validation on each parameter and uses default value if it is invalid.
        if(pTeamName.length() != 0)
        {
            teamName = pTeamName;
        }
        else
        {
            teamName = "DefaultTeam";
        }

        if(pCarCode.length() != 0)
        {
            carCode = pCarCode;
        }
        else
        {
            teamName = "DefaultCar";
        }

        if(pDriverName.length() != 0)
        {
            driverName = pDriverName;
        }
        else
        {
            driverName = "DefaultDriver";
        }

        if(pGrandPrix.length() != 0)
        {
            grandPrix = pGrandPrix;
        }
        else
        {
            grandPrix = "DefaultGrandPrix";
        }

        if(pPosFinish != 0)
        {
            posFinish = pPosFinish;
        }
        else
        {
            posFinish = 1;
        }

        if(pFastestLap > 0)
        {
            fastestLap = pFastestLap;
        }
        else
        {
            fastestLap = 0.0;
        }
    }   

    // Copy Constructor
    public Driver(Driver pDriver)
    {
        teamName = pDriver.getTeamName();
        carCode = pDriver.getCarCode();
        driverName = pDriver.getDriverName();
        grandPrix = pDriver.getGrandPrix();
        posFinish = pDriver.getPosFinish();
        fastestLap = pDriver.getFastestLap();
    }

    // Default Constructor
    public Driver()
    {
        teamName = "DefaultTeam";
        carCode = "DefaultCar";
        driverName = "DefaultDriver";
        grandPrix = "DefaultGrandPrix";
        posFinish = 0;
        fastestLap = 0.0d;
    }

    // getter methods
    public String getTeamName()
    {   
        return teamName;
    }

    public String getCarCode()
    {
        return carCode;
    }

    public String getDriverName()
    {
        return driverName;
    }

    public String getGrandPrix()
    {
        return grandPrix;
    }

    public int getPosFinish()
    {
        return posFinish;
    }

    public double getFastestLap()
    {
        return fastestLap;
    }

    // setter methods
    public void setTeamName(String pTeamName)
    {
        if(pTeamName.length() != 0)
        {
            teamName = pTeamName;
        }
    }

    public void setCarCode(String pCarCode)
    {
        if(pCarCode.length() != 0)
        {
            carCode = pCarCode;
        }
    }

    public void setDriverName(String pDriverName)
    {
        if(pDriverName.length() != 0)
        {
            driverName = pDriverName;
        }
    }

    public void setGrandPrix(String pGrandPrix)
    {
        if(pGrandPrix.length() != 0)
        {
            grandPrix = pGrandPrix;
        }
    }

    public void setPosFinish(int pPosFinish)
    {   
        if(pPosFinish != 0)
        {
            posFinish = pPosFinish;
        }
    }

    public void setFastestLap(double pFastestLap)
    {
        if(pFastestLap > 0)
        {
            fastestLap = pFastestLap;
        }
    }

    // toString method
    public String toString()
    {
        String stringOut = "Team: " + teamName + ", Car Code: " + carCode + ", Driver Name: " + 
        driverName + ", Grand Prix: " + grandPrix + ", Position Finished: " + 
        posFinish + ", Fastest Lap (seconds): " + fastestLap + "\n";

        return stringOut;
    }

    // equals method 
    public boolean isEqual(Object inObject)
    {
        boolean isEqual = false;
        if(inObject instanceof Driver)
        {
            Driver inDriver = (Driver)inObject;
            if(inDriver.getTeamName() == teamName)
            {
                if(inDriver.getCarCode() == carCode)
                {
                    if(inDriver.getDriverName() == driverName)
                    {
                        if(inDriver.getGrandPrix() == grandPrix)
                        {
                            if(inDriver.getPosFinish() == posFinish)
                            {
                                if(inDriver.getFastestLap() == fastestLap)
                                {
                                    isEqual = true;
                                }
                            }
                        }
                    }
                }
            }
        }

        return isEqual;
    }
}
