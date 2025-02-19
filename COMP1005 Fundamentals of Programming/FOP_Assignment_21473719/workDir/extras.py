"""
extras.py - contains classes for any extra functionality for the animation

edits:
18/5/23 - added laser class
19/5/23 - refactored laser class to allow for higher flexibility with adjusting properties.
          Due to the need to focus on the things that actually get me marks, like the report, I won't be adding functionality
          to manipulate individual lasers.
        - added laserSeries class
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.collections as cs

class laser():
    """Set up a laser object to manipulate.

    side can be either 'l' or 'r', indicating the laser can be placed on either the right or the left side of the stage.
        
    stage should be an instance of the generate_stage class.
    
    sourceHeight should be between 0 and 500.
    
    split should be between 1 and 20, indicates how many lasers are coming out of the one source
    
    spread is the angle between each light beam, should be between 5 and 60 degrees"""
    def rotate(self, angle):
        '''is only ever called in the background. Not needed by user. Correctly splits the lights and then adjusts the angle of all lights.'''
        for c, y in enumerate(np.linspace(-self.spread, self.spread, self.split)):
            a = mpl.transforms.Affine2D().rotate_deg_around(self.pos[0], self.sourceHeight, float(y + angle))
            self.lasers[c].set_transform(a + self.stage.transData)
    
    def __init__(self, stage, side, sourceHeight, colour, split, spread):
        self.side = side
        self.stage = stage
        self.colour = colour
        self.spread = spread
        self.sourceHeight = sourceHeight
        self.split = split
        
        sources = [(x, sourceHeight + y) for x in [25,38,12] for y in [0, 13, -13]]
        sizes = np.ones(9) * 30

        # plot the laser sources
        if side == 'l':
            self.pos = np.array([0, 700])
            self.collection = cs.CircleCollection(sizes, offsets=sources, transOffset=stage.left.transData, color=colour)
            stage.left.add_collection(self.collection)

        elif side == 'r':
            self.pos = np.array([500, -200])
            self.collection = cs.CircleCollection(sizes, offsets=sources, transOffset=stage.right.transData, color=colour)
            stage.right.add_collection(self.collection)

        else:
            raise NameError("side must be either 'l' or 'r'")
        
        # plot the lasers
        z = np.ones((2, split))*sourceHeight
        self.lasers = stage.centre.plot(self.pos, z, color = self.colour, zorder=8)

        self.rotate(0)



    
class laserSeries():
    '''class used to adjust the lasers. Only supports adjusting colour and direction of all lasers at once.
    to change number of lights, delete the laser object and make a new one.'''
    def __init__(self, allLasers):
        self.allLasers = allLasers
        self.state = True
        try:
            for item in allLasers:
                if item.side == 'l' or item.side == 'r': # This will raise an error if any of the items in the list aren't an instance of the laser class.
                    pass
        except:
            raise TypeError('The argument must be a list of laser objects.')
    
    def setColour(self, colour):
        '''set colour of all lasers'''
        for laserObject in self.allLasers:
            laserObject.collection.set_color(colour)
            for laser in laserObject.lasers:
                laser.set_color(colour)
    
    def setDirection(self, angle):
        '''change the direction of all lasers. Negative angle points lights down. Positive angle points angles up.'''
        for laserObject in self.allLasers:
            ang = [-angle if laserObject.side =='r' else angle]
            laserObject.rotate(ang[0])

    def toggle(self):
        self.state = not self.state
        for laserObject in self.allLasers:
            for laser in laserObject.lasers:
                laser.set_alpha([1 if self.state else 0][0])
    

        
            


