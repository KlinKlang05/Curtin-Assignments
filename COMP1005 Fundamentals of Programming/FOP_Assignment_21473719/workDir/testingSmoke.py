from smoke import * 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.animation import FuncAnimation
from plots import generate_stage

stage = generate_stage()

sm2 = smokeMachine(stage, 'l')
plt.pause(2)

# plt.imshow(sm.air)
# plt.show()
# plt.clf()
# plt.imshow(sm.roller(sm.air, 1, 1))
# plt.show()


for x in range(1000):
    print(x)
    sm2.nextFrame(x)
    print("showing frame")
    plt.pause(0.1)
 

#sm2 = smokeMachinev2()
    
    



