from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-title Solaris")
loadPrcFileData("", "win-size 800 600")
loadPrcFileData("", "icon-filename img/logo.ico")

from menu import Menu
from solarsystem import Solarsystem
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import Vec3


class Solaris(ShowBase):

    textures_folder = "textures/"
    models_folder = "models/"
    audio_folder = "audio/"
    image_folder = "img/"

    def __init__(self):
        ShowBase.__init__(self)
        menu = Menu(self)
        menu.create_main_menu()

app = Solaris()
app.run()