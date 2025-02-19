package edu.curtin.app;

import com.sun.tools.javac.Main;
import edu.curtin.app.factory.TownSimFactory;
import edu.curtin.app.observers.DayCompletedObserver;

import java.io.IOException;
import java.sql.Array;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.logging.Logger;
import java.util.regex.Pattern;

public class MainLoop {
    private final TownSimFactory factory;
    private static final Logger log = Logger.getLogger(MainLoop.class.getName());
    private final List<DayCompletedObserver> observers = new ArrayList<>();
    private final List<List<String>> foundingEvents = new ArrayList<>();
    private final List<List<String>> populationEvents = new ArrayList<>();
    private final List<List<String>> constructionEvents = new ArrayList<>();
    private final List<List<String>> duplicationEvents = new ArrayList<>();
    private final List<String> invalidEvents = new ArrayList<>();


    public MainLoop(TownSimFactory factory) {
        this.factory = factory;
    }

    public void mainLoop(){ // Driver method
        Pattern posIntPattern = Pattern.compile("^(0|[1-9]\\d*)$");     // Match any positive integer
        Pattern letUndPattern = Pattern.compile("^[A-Za-z_]+$");        // Match any upper or lower case letter and underscore
        TownsInput inp = factory.getTownsInputInstance();
//        inp.setErrorProbability(0.0);       // SET PROBABILITY

        try {
            while(System.in.available() == 0) {
                // Wait 1 second
                try {
                    Thread.sleep(1000);
                }
                catch(InterruptedException e) {
                    throw new AssertionError(e);
                }

                String msg = inp.nextMessage();
                while(msg != null) {
                    String finalMsg = msg;
                    log.fine(() -> "Debug Raw Message: " + finalMsg + "\n");
                    boolean invalidMessage = false;
                    String[] splitMsg = msg.split(" ");
                    if (splitMsg.length == 3) {
                        switch (splitMsg[0].toLowerCase()) {
                            case "town-founding" -> {
                                if (letUndPattern.matcher(splitMsg[1]).matches() && posIntPattern.matcher(splitMsg[2]).matches()) {
                                    foundingEvents.add(List.of(splitMsg[1], splitMsg[2]));
                                } else {
                                    invalidMessage = true;
                                }
                            }
                            case "town-population" -> {
                                if (letUndPattern.matcher(splitMsg[1]).matches() && posIntPattern.matcher(splitMsg[2]).matches()) {
                                    populationEvents.add(List.of(splitMsg[1], splitMsg[2]));
                                } else {
                                    invalidMessage = true;
                                }
                            }
                            case "railway-construction" -> {
                                if (letUndPattern.matcher(splitMsg[1]).matches() && letUndPattern.matcher(splitMsg[2]).matches()) {
                                    constructionEvents.add(List.of(splitMsg[1], splitMsg[2]));
                                } else {
                                    invalidMessage = true;
                                }
                            }
                            case "railway-duplication" -> {
                                if (letUndPattern.matcher(splitMsg[1]).matches() && letUndPattern.matcher(splitMsg[2]).matches()) {
                                    duplicationEvents.add(List.of(splitMsg[1], splitMsg[2]));
                                } else {
                                    invalidMessage = true;
                                }
                            }
                            default -> invalidMessage = true;
                        }
                    } else {
                        invalidMessage = true;
                    }

                    if (invalidMessage) {                   // all invalid or incorrectly formatted messages are passed. Though they don't need to be used,
                        invalidEvents.add(msg);            // they are kept for the purpose of displaying the message after the day is completed, as the assignment requests.
                    }

                    msg = inp.nextMessage();
                }
                notifyObservers(false);

                foundingEvents.clear();  // Clear the values to fill with the next day's events
                constructionEvents.clear();
                populationEvents.clear();
                duplicationEvents.clear();
                invalidEvents.clear();


            }

            notifyObservers(true); // MainLoop is finished, notify observers.
        }
        catch(IOException e) {
            System.out.println("Error reading user input");
        }
    }

    public List<List<String>> getFoundingEvents() {
        return foundingEvents;
    }

    public List<List<String>> getPopulationEvents() {
        return populationEvents;
    }

    public List<List<String>> getConstructionEvents() {
        return constructionEvents;
    }

    public List<List<String>> getDuplicationEvents() {
        return duplicationEvents;
    }

    public List<String> getInvalidEvents() {
        return invalidEvents;
    }

    public void addObserver(DayCompletedObserver observer) {
        observers.add(observer);
    }

    public void removeObserver(DayCompletedObserver observer) {
        observers.remove(observer);
    }

    public void notifyObservers(boolean finalDay) {
        for (DayCompletedObserver observer : observers) {
            observer.dayCompleted(finalDay);
        }
    }

}
