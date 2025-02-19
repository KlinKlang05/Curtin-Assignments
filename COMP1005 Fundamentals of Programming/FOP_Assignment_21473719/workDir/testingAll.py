from plots import generate_stage
from smoke import smokeMachine
from images import bandAnimate, renderBackDrop, renderStage
from lights import light, lightSeries
from extras import laser, laserSeries
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

def init():
    stage = generate_stage()
    
    renderStage(stage)
    band = bandAnimate(stage)
    lightObjects = np.empty(8, dtype=object)
    for c, lightPosition in enumerate(np.linspace(40,460,8)):
        lightObjects[c] = light(lightPosition, stage, 'purple', 't')
    allLights = lightSeries(lightObjects)
    allLasers = laserSeries([laser(stage, 'l', 400, 'blue', 5, 50), laser(stage, 'r', 400, 'blue', 5, 50)])
    renderBackDrop(stage)
    bLight1 = light(100, stage, 'blue', 'b')
    bLight2 = light(400, stage, 'blue', 'b')
    bottomLights = lightSeries([bLight1, bLight2])
    
    smokeLeft = smokeMachine(stage, 'l')
    renderStage(stage)
    return smokeLeft,band,allLasers,allLights
    
s, b, l, lighht = init()
for x in range(1000):     
    s.nextFrame('on')   
    b.nextFrame(x) 
    if x % 4 == 0:
        l.setDirection(-x)

    plt.pause(0.1)
    



