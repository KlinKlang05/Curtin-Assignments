""" 
images.py - Contains classes that render images on the screen such as stage, backdrop, and band
Credits - Band animation frames taken from https://en.picmix.com/stamp/Music-Rock-n-Roll-bp-1526520
other   - The following code was used to grab the original downloaded frames, and resize/rotate them 
          For use in the assignment:
               a = Image.open('bandFrames/{filename}')
               a = a.resize((307, 175), Image.ANTIALIAS)
               a = a.rotate(180, PIL.Image.NEAREST, expand = 1)
               a = a.save("bandFrames/{filename}")

edits:
15/5/23 - Created bandAnimate, renderStage and renderBackDrop. Finished writing them in the same day.

"""
import matplotlib.pyplot as plt
import matplotlib as mpl

class bandAnimate(): 
    """class used to create an imshow object which displays the band frame images, and then update the frame, to create
     the illusion of a moving image."""
    def __init__(self, stage):
        self.axis = stage.centre
        self.F1 = plt.imread('bandFrames/F1.png')
        self.F2 = plt.imread('bandFrames/F2.png')
        self.F3 = plt.imread('bandFrames/F3.png')

        self.transform = mpl.transforms.Affine2D().translate(95, 105) # the translation object that stores translation data used to move image

        self.frames = [self.F1, self.F2, self.F3] # save objects to a list to iterate over
        self.speed = 4 # band frame will update every self.speed frames
        self.count = 1 # self.count updates every time the band frame updates, then modulo divided by the amount of unique band frames (3) to 
                       # index self.frames, subsequently looping through each frame infinitely

        self.imgplot = self.axis.imshow(self.frames[0], zorder = 2) 
        self.imgplot.set_transform(self.transform + self.axis.transData) # positions the band on the correct spot on the stage 


    def nextFrame(self, frame): 
        """update the band frame every 4 frames by default. Use changeSpeed method to change how many frames between updates."""
        if frame % self.speed == 0:
            self.imgplot.set_data(self.frames[self.count % 3]) # update the imshow object to render the next band frame
            self.count += 1

    def changeSpeed(self, speed): 
        """change the speed at which the band frames update.
        speed should be an integer representing how many frames should pass until the band frame is updated."""
        self.speed = speed

def renderStage(stage):
    """renders the stage that is below the performers."""
    stg = plt.imread('stage2.1.png')
    stagePlot = stage.centre.imshow(stg, origin="lower", zorder=10)
    
def renderBackDrop(stage):
    """renders the backdrop that is behind the performers."""
    bd = plt.imread('backdrop.png')
    
    backdrop = stage.centre.imshow(bd, zorder=0)
    
    transform = mpl.transforms.Affine2D().translate(0, 130)
    backdrop.set_transform(transform + stage.centre.transData)
    
