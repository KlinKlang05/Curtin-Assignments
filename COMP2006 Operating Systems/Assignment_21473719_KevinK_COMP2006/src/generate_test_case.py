"""
This file was used to generate a few randomly generated 9x9 grids, which were then adjusted to have a few valid rows/cols/subgrids. This file isn't relevant.
"""

import os
import random
fname = "solution"

files = [f for f in os.listdir() if "solution" in f]
print(files)

def getlowestfilename(common_names:list, filename:str):
    if len(common_names) == 0:
        return filename + ".txt"
    next_lowest = 0
    for i in range(len(common_names)):
        if i == 0:
            if common_names[i] != filename + ".txt":
                return filename + ".txt"
            else: 
                next_lowest += 1
        elif common_names[i] != filename + str(i) + ".txt":
            return filename + str(i) + ".txt"
        else: 
            next_lowest += 1
        

    return filename + str(next_lowest) + ".txt"


f = open(getlowestfilename(files, fname), "w")

for i in range(9):
    for k in range(9):
        f.write(f"{random.randint(1,9)} ", )
    f.write("\n")

f.close()


     