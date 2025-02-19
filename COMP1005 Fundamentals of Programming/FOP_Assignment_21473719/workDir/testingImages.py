from images import *
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.animation import FuncAnimation

fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 10]},
                              figsize = (10,10)) # taken from starter code from assignment briefing


ax0.set_aspect("equal")     # set up the top axis that contains the light sources
ax0.set_facecolor('black')
ax0.set_xlim(0,500)
ax0.set_ylim(0,50)

ax1.set_aspect('equal')     # set up the main axis that contains all objects that interract
ax1.set_ylim(0,500)         # for the duration of the animation
ax1.set_xlim(0,500)

renderStage(ax1)
renderBackDrop(ax1)
x = bandAnimate(ax1)


for frame in range(500):
    x.nextFrame(frame)
    plt.pause(0.1)