from plots import *
from extras import *
from lights import *

stage = generate_stage()

laser1 = laser(stage, 'l', 200, 'purple', 16, 20)
laser2 = laser(stage, 'r', 400, 'red', 14, 30)

bottomLight1 = light(300, stage, 'green', 'b')

plt.pause(1)

allMyLasers = laserSeries([laser1, laser2])

allMyLights = lightSeries([bottomLight1])

allMyLights.setFocus(int(input('set focus width 10 to 200 ')), 'all')
allMyLasers.setColour('red')

plt.pause(1) 

for x in range(3):
    allMyLasers.setDirection(int(input('set angle direction for lasers ')))
    plt.pause(2)

plt.pause(2)

allMyLights.setDirection(int(input('set angle direction for light ')), 'all')

plt.pause(2)

allMyLights.setIntensity(float(input('set intensity 0.1 to 1 ')), 'all')

plt.pause(2)

