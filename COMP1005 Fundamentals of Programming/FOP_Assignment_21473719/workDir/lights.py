"""
lights.py - Contains class that set up and control lights for main.py 

edits:
30/4/23 - set up light and lightSeries classes.
 1/5/23 - added colour changing functionality to lightSeries
        - modified class light() such that each attribute is a
          data object that contains the information for each object
          that is to be plotted. Essentially allowing support for use
          with matplotlib.animation.FuncAnimation
 2/5/23 - added functionality for setIntensity and setFocus
 4/5/23 - added functionality for setDirection 
        - modified class light() to include two more attributes, self.centre and self.width
          to allow for current position of beam to be updated and accessed, allowing for setDirection and 
          setFocus to work together properly
        - modified setDirection to allow for light.beam, or the polygon object, to pivot around its anchor point,
          allowing for proper rotation of the light instead of replotting the light beam based off different
          positions along the x-axis.
        - removed self.centre and self.width from class light() as the implementation of the polygon rotation means 
          it is not required to have all points of the polygon saved.
        - Ready to use as of 4/5/23
19/5/23 - added support for adding lights on the bottom of the stage

"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

class light(): 
    """ Class for an individual light. Takes starting positions and axis, sets up light source (patches.circle object),
    and light beam (pyplot.fill object). These should be edited via the light_series class.
    sourcePozzie should be the horizontal position of the light, 0 to 500

    stage should be an instance of the generate_stage class

    colour... surely you know what that is, but it has to be a string

    side is either 't' or 'b', indicating whether the light is at the top or the bottom of the stage.
    
    returns the light beam object and the light source object.
    """
    def __init__(self, sourcePozzie, stage, colour, side):
        self.sourcePozzie = sourcePozzie
        
        circle = plt.Circle([self.sourcePozzie, 25], 20, color=colour, alpha=0.5) # set up the patches.circle object, allowing
                                                                  # for colour to be changed later
        self.stage = stage
        self.side = side

        if side == 't': 
            self.source = stage.top.add_patch(circle)
            self.yPositions = [510, 510, -75, -75]
            zorder = 3
        elif side == 'b':
            self.source = stage.bottom.add_patch(circle)
            self.yPositions = [-10, -10, 650, 650]
            zorder = 12
        else: raise NameError("side must be either 't' or 'b'")
        
        self.angle = 0  
        self.beam, = stage.centre.fill([self.sourcePozzie-10, self.sourcePozzie+10, self.sourcePozzie+50, self.sourcePozzie-50], 
                                   self.yPositions, color=colour, alpha=0.5, zorder=zorder) # set up pyplot.fill object, allowing for direction,
                                                                              # width and colour to be changed later.

    


class lightSeries():
    """Class for a whole series of lights. Takes an array of all light objects
    and each method is used to adjust the property of selected lights, using indexing.

    If you are creating light objects on the bottom of the stage, consider putting them in a different instance of this class
    
    To changew all lights at a time without having to pass a list of 0 through 8 every time,
    type 'all' in the indexes argument. Otherwise pass a list of each light index that is to be changed."""
    def __init__(self, series):
        self.series = series # an array of all light objects
        try:
            for item in series:
                if item.angle == 0: # This will raise an error if any of the items in the list aren't an instance of the light class.
                    pass
        except:
            raise TypeError('The argument must be a list of light objects.')
    
    
    def ifAll(self, indexin):
        """
        takes a list of integers and returns an iterable containing each light object.
        the string 'all' can also be used to reference all light objects in the light series.
        Only intended to be used within the class."""
        try:
            if indexin == 'all': 
                return self.series
            else:
                return [self.series[x] for x in indexin]
        except: raise NameError(f'index should be a list containing the indexes of the list that was passed into this class [0 - {len(self.series) - 1}]')

    # Adjusts the opacity of the light object. 
    def setIntensity(self, i, indexes): 
        """Adjust intensity between 0 and 1. Sets opacity of beam. Set if intensity is set to 1.1, add some
        wacky adjustment to the lights"""
        for light in self.ifAll(indexes):
            light.source.set_alpha(float(i))
            light.beam.set_alpha(float(i))
    
    # Updates colour of both the circle object and the polygon object
    def setColour(self, colour, indexes):
        """Change the colour of selected lights."""
        for light in self.ifAll(indexes):
            light.source.set_color(colour)
            light.beam.set_color(colour)
    
    # SetDirection uses matplotlib.transform to pivot the light beam, which is a polygon object, around a point.
    # that data is saved in the transform variable which is then applied using set_transform()
    def setDirection(self, ang, indexes): 
        '''Adjust the direction of the light in degrees. positive angle will move light towards the right, and vice versa,
        for both bottom and top lights.'''
        for light in self.ifAll(indexes):
            light.angle = ang
            
            angle = [-ang if light.side =='b' else ang]
            a = mpl.transforms.Affine2D().rotate_deg_around(light.sourcePozzie, light.yPositions[0], float(angle[0]))
            b = light.stage.transData
            
            transform = a + b # I can't understand why you have to add the transData for this to work properly.
            light.beam.set_transform(transform)
    
    # setFocus uses the polygon.set_xy() function which takes a 2D array containining the coordinates of the fill object,
    # updating the properties of the object which is reflected in the next frame. 
    def setFocus(self, foc, indexes): 
        """Focus from 10 to 200. anything less than 10 isn't allowed because
        it looks weird after that."""
        for light in self.ifAll(indexes):
            light.beam.set_xy(np.array([[light.sourcePozzie-10, light.yPositions[0]], 
                                        [light.sourcePozzie+10, light.yPositions[1]], 
                                        [light.sourcePozzie+foc, light.yPositions[2]], 
                                        [light.sourcePozzie-foc, light.yPositions[3]]])) 
            self.setDirection(light.angle, indexes) # Readjust angle to previous after replotting

