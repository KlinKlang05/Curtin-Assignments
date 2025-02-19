""" 
Smoke.py - Contains class that sets up smoke source and performs diffusion calculation, via Moore Neighbourhood.

edits:
 7/5/23 - set up source for smoke machine and initial calculation
11/5/23 - after many attempts at implementing a smoke update function that is fast enough for the purposes of animation,
          one has finally been found. It invovled shifting the values in self.air by 1, in all directions, and saving each 
          one in an array, then performing operations on those arrays. That is faster than any iterative method.
15/5/23 - That was the most unrealistic simulation of smoke I've ever seen. This next method will be much better.
21/5/23 - As you can see in the time between this entry and the last one, making a smoke machine using Moore Neighbourhood was hard.
          But I did it. See the report for explanations.
        - Refactored code to work with the rest of the program 
22/5/23 - added support for setting up the smoke machine on either the left or the right side.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class smokeMachine(): 
    def __init__(self, stage, side, state=True):
        """Renders a smoke effect onto the stage. 
        
        stage should be an instance of generate_stage
        
        side should be the side of the stage you want the smoke machine positioned. 

        State is whether the smoke machine is off or on. On by default.
        DO NOT add more than one smoke machine in a plot. Just don't."""

        self.state = state
        self.size = 50 # the resolution of the image, each 'pixel' is a space where a smoke particle can go.
        self.air = np.zeros((self.size+30,self.size+20))
        self.max = 10

        circle = plt.Circle([25, 170], 20, color='grey')

        self.side = side 
        if side == 'l':
            self.air[11,10] = self.max
            self.source = stage.left.add_patch(circle)
        elif side == 'r':
            self.air[11,59] = self.max
            self.source = stage.right.add_patch(circle)
        else:
            raise NameError("side must be either 'l' or 'r'")

        # change the colourmap so that "zero" values are completely transparent
        grey = mpl.cm.get_cmap('Greys', 256)
        newcolours = grey(np.linspace(0,0.5,256))
        # make transparency colourmap
        transparentCmap = mpl.colors.LinearSegmentedColormap.from_list('transparent', newcolours, 256)
        transparentCmap._init()
        alphas = np.linspace(0, 1, transparentCmap.N+3) # create alpha array
        transparentCmap._lut[:,-1] = alphas # fill colourmap with alpha array to make the cmap transparent


        upscale = np.kron(self.air[0:51, 10:61], np.ones((10,10))) # upscale 50x50 array to 500x500
        self.smoke = stage.centre.imshow(upscale, interpolation='none', cmap=transparentCmap, alpha=1, zorder=20)

        
            
    def nextFrame(self):
        """Calculates the next frame of the smoke simulation. 
        
        self.state must be True for the smoke source to be re-plotted and create a constant source of smoke."""
        # shift the self.air array up, down, left, right, up+down, up+left, down+left, down+right and save them to a list.
        shifted_arrays = []
        for x in range(-1,2):
             for y in range(-1,2):
                  shifted_arrays.append(np.roll(self.air, (x, y), axis=(1, 0))) # x is horizontal shift, y is vertical shift

        if self.side == 'l':
            del shifted_arrays[0] # remove first two entries in the list, see documents for details
            del shifted_arrays[0]
            shifted_arrays.append(shifted_arrays[4])
        else:
            del shifted_arrays[7]
            del shifted_arrays[6]
            shifted_arrays.append(shifted_arrays[2])

        # Calculate each updated value
        self.air = (sum(shifted_arrays))/8
        self.air = np.around(self.air, decimals=3, out=None)

        # clear all edge values in the array to stop the smoke from teleporting from one side to the other
        self.air[::self.size+30-1] = 0
        self.air[:, ::self.size+20-1] = 0

        if self.state:
            if self.side == 'l':
                self.air[14:21, 0:10] = self.max
            else:
                self.air[14:21, 61:70] = self.max
        
        
        upscale = np.kron(self.air[0:51, 10:61], np.ones((10,10)))
        self.smoke.set_data(upscale)


