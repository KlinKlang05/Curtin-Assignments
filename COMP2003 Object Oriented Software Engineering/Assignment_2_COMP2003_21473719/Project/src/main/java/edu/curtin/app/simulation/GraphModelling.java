package edu.curtin.app.simulation;

import edu.curtin.app.MainLoop;
import edu.curtin.app.simulation.railway.Railway;

import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Logger;

public class GraphModelling {   // TODO: update class diagram
    private static final Logger log = Logger.getLogger(MainLoop.class.getName());
    private List<String> nodes;
    private Set<String> edges;

    public GraphModelling() {
        nodes = new ArrayList<>();
        edges = new HashSet<>();
    }

    public void addNode(Town town) {
        nodes.add(town.getName());
    }

    private String buildEdgeString(Railway railway) {
        int totalRailways = railway.getSize();

        String link = "[color=\"red:red\"]"; // Lines will be red if there was an error getting the link. This should never occur

        if (totalRailways == 0) {
            if (railway.getDirection() == null) {   // getDirection returns null if the railway is still constructing a single railway
                link = "[style=\"dashed\"]";                        // Single under construction
            }
        } else if (totalRailways == 1) {
            if (railway.getCDaysLeft() == 0) {
                link = "";                                          // Single track completed
            } else {
                link = "[style=\"dashed\",color=\"black:black\"]";  // Dual under construction
            }
        }
        else if (totalRailways == 2) {
            link = "[color=\"black:black\"]";                       // Dual track completed
        }

        return link;
    }

    public void addEdge(Railway railway) {
        Town[] towns = railway.getBothTowns();

        String link = buildEdgeString(railway);

        edges.add(towns[0].getName() + " -- " + towns[1].getName() + " " + link);
    }

    public void removeEdge(Railway railway) {
        Town[] towns = railway.getBothTowns();

        String link = buildEdgeString(railway);

        edges.remove(towns[0].getName() + " -- " + towns[1].getName() + " " + link);        // Try both arrangements of the town names
        edges.remove(towns[1].getName() + " -- " + towns[0].getName() + " " + link);
    }

    /**
     * Writes the data to the file and then gracefully closes the objects currently writing to the file
     */
    public void buildGraph() {
        File file = new File("simoutput.dot");
        try ( FileWriter writer = new FileWriter(file)){

           writer.write("graph Towns { \n");

           for (String node : nodes) {
               writer.write("\t" + node + "\n");
               log.finest(() -> node);
           }

           writer.write("\n");

           for (String edge : edges) {
               writer.write("\t" + edge + "\n");
               log.finest(() -> edge);
           }

            writer.write("\n}");
        } catch (IOException e) {
            log.warning(() -> "Unknown IO exception:" + e.getMessage());
        }
    }
}
