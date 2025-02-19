"""spinal_tap.py - driver code for the 2023 FOP assignment.
Written by Kevin Kongo 21473719 on 23/5/23.
"""

from plots import generate_stage
from smoke import smokeMachine
from images import bandAnimate, renderBackDrop, renderStage
from lights import light, lightSeries
from extras import laser, laserSeries
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from interactive import animate
import sys

# Interactive GUI for modifying object properties
if sys.argv[1] == 'interactive':
    split = int(input('Select split for lasers, 1-20: '))
    while split <1 or split >20:
        split = int(input('Split must be 1-20, try again: '))

    spread = int(input('Select spread for lasers, should be an angle 5-60 degrees: '))
    while spread<5 or spread >60:
        spread = int(input('angle must be 5-60, try again: '))

    # generate all axes
    mainStage = generate_stage()

    # generate all plotting objects
    smoke = smokeMachine(mainStage, 'l', False)
    renderBackDrop(mainStage)
    renderStage(mainStage)
    band = bandAnimate(mainStage)

    # create 8 lights
    lightObjects = np.empty(8, dtype=object)
    for c, lightPosition in enumerate(np.linspace(40,460,8)):
        lightObjects[c] = light(lightPosition, mainStage, 'purple', 't')
    allLights = lightSeries(lightObjects)

    # create two lasers
    allLasers = laserSeries([laser(mainStage, 'l', 400, 'blue', split, spread), laser(mainStage, 'r', 400, 'blue', split, spread)])

    # called every frame
    def update(frame):
        band.nextFrame(frame)
        smoke.nextFrame()

    # funcAnimation to show plots 
    animation = animate(mainStage, update, allLights, allLasers, smoke, band)
    plt.show()

# CSV file function executor
else:
    try:
        with open(sys.argv[1], 'r') as file:
            csvContent = file.readlines()
    except FileNotFoundError:
        print('invalid file. Try again.\nIf you wanted to open the interactive gui, pass "interactive" as the argument.')
        exit()

    formatted = []
    for item in csvContent:
        if len(formatted) <= 7:
            formatted.append(item.strip().split(','))
        else:
            formatted.append(item.strip())


    mainStage = generate_stage()
    smoke = smokeMachine(mainStage, f'{formatted[3][1]}', False)
    renderBackDrop(mainStage)
    renderStage(mainStage)
    band = bandAnimate(mainStage)

    # create 8 lights
    lightObjects = np.empty(int(formatted[0][1]), dtype=object)
    for c, lightPosition in enumerate(np.linspace(40,460,int(formatted[0][1]))):
        lightObjects[c] = light(lightPosition, mainStage, 'purple', 't')
    allTopLights = lightSeries(lightObjects)

    # create bottom lights
    moreLightObjects = np.empty(int(formatted[1][1]), dtype=object)
    for c, lightPosition in enumerate(np.linspace(40,460,int(formatted[1][1]))):
        moreLightObjects[c] = light(lightPosition, mainStage, 'purple', 'b')
    allBottomLights = lightSeries(moreLightObjects)

    # create two lasers
    allLasers = laserSeries([laser(mainStage, 'l', int(formatted[2][1]), 'blue', int(formatted[4][1]), int(formatted[5][1])), laser(mainStage, 'r', int(formatted[2][1]), 'blue', int(formatted[4][1]), int(formatted[5][1]))])

    frame = 0
    index = 34
    speed = 0.2
    band.changeSpeed(1)
    consistent_wait = formatted[6][1]

    # Mainloop that executes the code.
    while True:
        index += 1
        try:
            for x in range(int(formatted[index])):
                band.nextFrame(frame)
                frame += 1
                print('nextsmoke')
                smoke.nextFrame() 
                plt.pause(speed)
        except:
            exec(formatted[index])
            for x in range(int(consistent_wait)):
                band.nextFrame(frame)
                frame += 1
                smoke.nextFrame()
                plt.pause(speed)
        
        if index == len(formatted)-1:
            break
            


