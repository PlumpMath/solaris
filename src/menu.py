from direct.gui.DirectGui import *
from panda3d.core import *
from pandac.PandaModules import *
import sys

from solarsystem import Solarsystem


class Menu:

    sound = True
    animBackground = True

    def __init__(self, app):
        self.app = app
        self.textures_folder = self.app.textures_folder
        self.audio_folder = self.app.audio_folder
        self.image_folder = self.app.image_folder
        self.app.disableMouse()
        self.app.setBackgroundColor(0, 0, 0)
        if self.animBackground:
            self.set_animated_background()
        else:
            self.set_static_background()

        self.set_sound()
        if self.sound:
            self.bg_sound.play()

        # Button Texture
        cm = CardMaker('OnscreenImage')
        cm.setFrame(-6, 6, -1, 1.5)
        self.buttonNorm = NodePath(cm.generate())
        self.buttonNorm.setTexture( self.app.loader.loadTexture(self.image_folder+"button.png") )
        self.buttonNorm.setTransparency(TransparencyAttrib.MAlpha)

    def set_sound(self):
        self.hover_sound = self.app.loader.loadSfx(self.audio_folder+"button_hover.mp3")
        self.click_sound = self.app.loader.loadSfx(self.audio_folder+"button_click.mp3")
        self.bg_sound = self.app.loader.loadSfx(self.audio_folder+"bg.mp3")

    def set_animated_background(self):
        self.tex = MovieTexture("background")
        assert self.tex.read(self.textures_folder+"background.mp4"), "Failed to load background!"
        cm = CardMaker("Card");
        cm.setFrameFullscreenQuad()
        cm.setUvRange(self.tex)
        self.card = NodePath(cm.generate())
        self.card.reparentTo(self.app.render2d)
        self.card.setTexture(self.tex)
        self.card.setTexScale(TextureStage.getDefault(), self.tex.getTexScale())

    def set_static_background(self):
        self.backgroundImage = OnscreenImage(image = self.textures_folder+"stars.jpg", pos = (0, 0, 0), scale=1.4)

    def create_main_menu(self):
        self.textHeader = OnscreenImage(image=self.image_folder+"solaris.png", pos=(0,0,0.6), scale=(0.6,0,0.15))
        self.textHeader.setTransparency(1)

        self.buttonStart = DirectButton(pos = Vec3(0,0,0.2), text = "Start Simulation",
                   scale = .1, relief=None,
                   rolloverSound = None, clickSound = None,
                   command = self.startSimulation, frameColor=(1,1,1,1), geom=(self.buttonNorm))

        self.buttonOptions = DirectButton(pos = Vec3(0,0,-.2), text = "Options",
                   scale = .1, relief=None,
                   rolloverSound = None, clickSound = None,
                   command = self.showOptions, frameColor=(1,1,1,1), geom=(self.buttonNorm))
        self.buttonQuit = DirectButton(pos = Vec3(0,0,-.6), text = "Quit",
                   scale = .1, relief=None,
                   rolloverSound = None, clickSound = None,
                   command = self.quitProgram, frameColor=(1,1,1,1), geom=(self.buttonNorm))
        if self.sound:
            self.buttonStart['clickSound']=self.click_sound
            self.buttonOptions['clickSound']=self.click_sound
            self.buttonQuit['clickSound']=self.click_sound
            self.buttonStart['rolloverSound']=self.hover_sound
            self.buttonOptions['rolloverSound']=self.hover_sound
            self.buttonQuit['rolloverSound']=self.hover_sound


    def destroy_main_menu(self):
        self.buttonStart.destroy()
        self.buttonOptions.destroy()
        self.buttonQuit.destroy()
        self.textHeader.destroy()

    def create_options_menu(self):
        self.textHeader = OnscreenImage(image=self.image_folder+"options.png", pos=(0,0,0.6), scale=(0.6,0,0.15))
        self.textHeader.setTransparency(1)
        self.buttonSound = DirectButton(pos = Vec3(0,0,.2), text = "Sounds",
                   scale = .1, relief=None,
                   rolloverSound = None, clickSound = None,
                   command = self.toggleSound, geom=(self.buttonNorm))
        self.labelSound = DirectLabel(pos = Vec3(.8,0,.19), text = "Off",
                   scale = .12, pad = (.5, .5), frameColor=self.getColor(self.sound))
        self.labelSound["text"] = self.getText(self.sound)
        self.buttonAnimBackground = DirectButton(pos = Vec3(0,0,-.2), text = "Animated Background",
                   scale = .1, relief=None,
                   rolloverSound = None, clickSound = None,
                   command = self.toggleAnimBackground, geom=(self.buttonNorm))
        self.labelAnimBackground = DirectLabel(pos = Vec3(.8,0,-.21), text = "Off",
                   scale = .12, pad = (.5, .5), frameColor=self.getColor(self.animBackground))
        self.labelAnimBackground["text"] = self.getText(self.animBackground)
        self.buttonSave = DirectButton(pos = Vec3(0,0,-.6), text = "Save",
                   scale = .1, relief=None,
                   rolloverSound = None, clickSound = None,
                   command = self.saveOptions, geom=(self.buttonNorm))
        if self.sound:
            self.buttonSound['clickSound']=self.click_sound
            self.buttonAnimBackground['clickSound']=self.click_sound
            self.buttonSave['clickSound']=self.click_sound
            self.buttonSound['rolloverSound']=self.hover_sound
            self.buttonAnimBackground['rolloverSound']=self.hover_sound
            self.buttonSave['rolloverSound']=self.hover_sound

    def destroy_options_menu(self):
        self.buttonSound.destroy()
        self.buttonAnimBackground.destroy()
        self.buttonSave.destroy()
        self.labelSound.destroy()
        self.labelAnimBackground.destroy()
        self.textHeader.destroy()

    def getText(self, boolValue):
        if boolValue:
            return "On"
        else:
            return "Off"

    def getColor(self, boolValue):
        if boolValue:
            return (0,1,0,1)
        else:
            return (1,0,0,1)

    def startSimulation(self):
        self.destroy_main_menu()
        if self.animBackground:
            self.card.remove()
        else:
            self.backgroundImage.destroy()
        self.textHeader.destroy()
        self.app.enableMouse()
        solarsystem = Solarsystem(self.app, self)

    def showOptions(self):
        self.destroy_main_menu()
        self.create_options_menu()

    def quitProgram(self):
        sys.exit()

    def toggleSound(self):
        self.sound = not self.sound
        self.labelSound["frameColor"] = self.getColor(self.sound)
        self.labelSound["text"] = self.getText(self.sound)
        if self.sound:
            self.bg_sound.play()
            self.click_sound.play()
            self.buttonSound['clickSound']=self.click_sound
            self.buttonAnimBackground['clickSound']=self.click_sound
            self.buttonSave['clickSound']=self.click_sound
            self.buttonSound['rolloverSound']=self.hover_sound
            self.buttonAnimBackground['rolloverSound']=self.hover_sound
            self.buttonSave['rolloverSound']=self.hover_sound
        else:
            self.bg_sound.stop()
            self.buttonSound['clickSound']=None
            self.buttonAnimBackground['clickSound']=None
            self.buttonSave['clickSound']=None
            self.buttonSound['rolloverSound']=None
            self.buttonAnimBackground['rolloverSound']=None
            self.buttonSave['rolloverSound']=None

    def toggleAnimBackground(self):
        self.animBackground = not self.animBackground
        self.labelAnimBackground["frameColor"] = self.getColor(self.animBackground)
        self.labelAnimBackground["text"] = self.getText(self.animBackground)
        if self.animBackground:
            self.backgroundImage.destroy()
            self.set_animated_background()
        else:
            self.card.remove()
            self.set_static_background()
            self.destroy_options_menu()
            self.create_options_menu()

    def saveOptions(self):
        self.destroy_options_menu()
        self.create_main_menu()