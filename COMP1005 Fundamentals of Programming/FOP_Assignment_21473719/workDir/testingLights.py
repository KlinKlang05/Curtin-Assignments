#
# Testing.py - Test each class included within the program
#
from lights import light

from plots import generate_stage

from lights import lightSeries
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.animation import FuncAnimation

stage = generate_stage()

l = np.linspace(0,500,10)

print(l)

light0, light1 = light(l[1], stage, 'purple', 't'), light(l[2], stage, 'purple', 't')
light2, light3 = light(l[3], stage, 'purple', 't'), light(l[4], stage, 'purple', 't')
light4, light5 = light(l[5], stage, 'purple', 't'), light(l[6], stage, 'purple', 't')
light6, light7 = light(l[7], stage, 'purple', 't'), light(l[8], stage, 'purple', 't')

# Organise lights into an array for easy access via indexing
lights = np.array([light0, light1, light2, light3,
                   light4, light5, light6, light7])


AllMyLights = lightSeries(lights)

i = input('Select angle: ')
l = [1,3,4,7]
while i != "":
    AllMyLights.setDirection(i, l)
    plt.pause(1)
    AllMyLights.setColour(input("enter colour: "), [0,2,4,6])
    i = input('next direction selection, return to exit: ')
    l = [int(x) for x in input('list: ').split(',')]
    d = int(input('select width: '))
    AllMyLights.setFocus(d, l)



