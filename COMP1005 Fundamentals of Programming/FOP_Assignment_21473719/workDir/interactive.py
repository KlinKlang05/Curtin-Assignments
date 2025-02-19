"""
interactive.py - Provides a gui to interact with and view the functionality of different stage features.

Edits: made and finished the day before that this is due. So not really many edits.
"""

from matplotlib.animation import FuncAnimation
import matplotlib.widgets as wid
import mpl_toolkits.axes_grid1
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

class animate(FuncAnimation):
    """Provides a gui to modify and interact with different objects that are plotted onto the stage.
    
    stage should be an instance of generate_Stage
    
    func should be an update function that takes one frame parameter, and passes that frame (an int) to any method used for updating frames.
    Main ones are images.bandAnimate.nextFrame and smoke.smokeMachine.nextFrame.
    
    lightSer should be an instance of lightSeries class
    
    lightSer should be an instance of laserSeries class
    
    smokeMac should be an instance of smokeMachine class
    
    band should be an instance of bandAnimate class"""
    def __init__(self, stage, func, lightSer, lasers, smokeMac, band, init_func=None, fargs=None, save_count=None, **kwargs) -> None:
        self.smokeState = False # Smoke is not running by default
        self.lightSer = lightSer
        self.lasers = lasers
        self.smokeMac = smokeMac
        self.band = band
        self.stage = stage
        self.func = func
        self.setup()    

        self.colours = ['yellow', 'blue', 'red', 'purple',
                    'orange', 'goldenrod', 'khaki', 'white', 
                    'darkred', 'chocolate', 'lightskyblue', 'steelblue', 
                    'hotpink', 'lime', 'forestgreen', 'navy', 'indigo']

        super().__init__(stage.fig, func, 2000, init_func, fargs, save_count, interval=20, **kwargs)

    def setup(self):
        fig, ((widgetArea1, widgetArea2, widgetArea3),(widgetArea4, widgetArea5, widgetArea6)) = plt.subplots(2, 3, figsize=(15,10))
        for widget in [widgetArea1, widgetArea2, widgetArea3, widgetArea4, widgetArea5, widgetArea6]:
            widget.axis('off')

        # access the subplot so that it can be split into seperate axes for each widget
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(widgetArea1)
        divider2 = mpl_toolkits.axes_grid1.make_axes_locatable(widgetArea2)
        divider3 = mpl_toolkits.axes_grid1.make_axes_locatable(widgetArea3)
        divider4 = mpl_toolkits.axes_grid1.make_axes_locatable(widgetArea4)
        divider5 = mpl_toolkits.axes_grid1.make_axes_locatable(widgetArea5)
        
        # set up 24 sliders for 8 lights and their direction and width and intensity.
        self.lightDirectionAxes = []
        self.lightDirectionSliders = []
        self.lightFocusAxes = []
        self.lightFocusSliders = []
        self.lightIntensityAxes = []
        self.lightIntensitySliders = []

        for x in range(8):
            # Direction
            self.lightDirectionAxes.append(divider.append_axes("bottom", size="200%", pad=0.1))
            self.lightDirectionSliders.append(wid.Slider(self.lightDirectionAxes[x], f'light {x} Direction', -90, 90, valinit=0))
            shift = mpl.transforms.Affine2D().translate(-30, 0)
            self.lightDirectionSliders[x].label.set_transform(shift + self.lightDirectionAxes[x].transData)

            # Width 
            self.lightFocusAxes.append(divider2.append_axes("bottom", size="200%", pad=0.1))
            self.lightFocusSliders.append(wid.Slider(self.lightFocusAxes[x], f'light {x} Focus', 10, 200, valinit=45))
            shift = mpl.transforms.Affine2D().translate(60, 0)
            self.lightFocusSliders[x].label.set_transform(shift + self.lightFocusAxes[x].transData)

            # Intensity
            self.lightIntensityAxes.append(divider3.append_axes("bottom", size="200%", pad=0.1))
            self.lightIntensitySliders.append(wid.Slider(self.lightIntensityAxes[x], f'light {x} Intensity', 0, 1, valinit=0.4))
            shift = mpl.transforms.Affine2D().translate(0.4, 0)
            self.lightIntensitySliders[x].label.set_transform(shift + self.lightIntensityAxes[x].transData)

            for slider in self.lightDirectionSliders + self.lightFocusSliders + self.lightIntensitySliders:
                slider.on_changed(self.applyChange)


        toggle1 = divider4.append_axes("bottom", size="100%", pad=0.1)
        self.smoke = wid.Button(toggle1, label='Toggle Smoke Machine')
        self.smoke.on_clicked(self.toggleSmoke)

        lasers = divider4.append_axes("bottom", size="200%", pad=0.1)
        self.laserSlider = wid.Slider(lasers, 'laser direction', -90, 90, valinit=0)
        self.laserSlider.on_changed(self.applyChange)

        colours = divider4.append_axes("bottom", size="100%", pad=0.1)
        self.colour = wid.Button(colours, label='Randomize Light colours')
        self.colour.on_clicked(self.randomizeLightColours)

        toggle2 = divider4.append_axes("bottom", size ="100%", pad=0.1)
        self.laserToggle = wid.Button(toggle2, label='Randomize Laser colours')
        self.laserToggle.on_clicked(self.randomizerLaserColours)

        toggle3 = divider5.append_axes("bottom", size ="100%", pad=0.1)
        self.laserColourToggle = wid.Button(toggle3, label='Toggle Lasers')
        self.laserColourToggle.on_clicked(self.toggleLasers)

    def applyChange(self, i):
        for x in range(8):
            # Update Direction
            self.lightSer.setDirection(self.lightDirectionSliders[x].val, [x])
            # Update Focus 
            self.lightSer.setFocus(self.lightFocusSliders[x].val, [x])
            # Update Intensity 
            self.lightSer.setIntensity(self.lightIntensitySliders[x].val, [x])
        
        self.lasers.setDirection(self.laserSlider.val)
    
    def toggleSmoke(self, i):
        self.smokeState = not self.smokeState
        self.smokeMac.state = self.smokeState

    def toggleLasers(self, i):
        self.lasers.toggle()

    def randomizerLaserColours(self, i):
        self.lasers.setColour(np.random.choice(self.colours))

    def randomizeLightColours(self, i):
        for x in range(8):
            self.lightSer.setColour(np.random.choice(self.colours), [x])

        
        



