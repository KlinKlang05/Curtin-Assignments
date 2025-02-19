"""
plots.py - generates the main stage plot that contains the axes that all other classes use to plot onto.
Allows for other classes to access the attributes of an instance of this class.

edits:
18/5/23 - added generate_stage class and implemented functionality 
"""


import matplotlib.pyplot as plt 

class generate_stage():
    """
    creates the subplots required for other functions to plot their stage features. 
    See documentation and report for diagram.
                   
    """ 
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(10, 10))
        self.gs = self.fig.add_gridspec(3, 3,  width_ratios=(1,10,1), height_ratios=(1, 10, 1), wspace=0.05, hspace =0.05)

        self.top = self.fig.add_subplot(self.gs[0, 1])
        self.left = self.fig.add_subplot(self.gs[1, 0])
        self.centre = self.fig.add_subplot(self.gs[1, 1], sharex=self.top, sharey=self.left)
        self.right = self.fig.add_subplot(self.gs[1, 2], sharex=self.left, sharey=self.left)
        self.bottom = self.fig.add_subplot(self.gs[2, 1], sharex=self.top, sharey=self.top)

        for side in [self.top, self.left, self.right, self.bottom]:
            side.set_facecolor('black')

        for c, ax in enumerate([self.top, self.left]):  # set up correct axis size and remove axis ticks. Using a for loop to avoid repitive lines
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(0, [500,50][c])
            ax.set_ylim(0, [50,500][c])

        self.transData = self.centre.transData