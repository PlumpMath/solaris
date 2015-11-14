from menu import Menu
from solarsystem import Solarsystem
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from panda3d.core import Vec3
from pandac.PandaModules import WindowProperties


class Solaris(ShowBase):

    textures_folder = "textures/"
    models_folder = "models/"
    audio_folder = "audio/"
    image_folder = "img/"

    def __init__(self):
        ShowBase.__init__(self)
        props = WindowProperties( )
        props.setTitle('Solaris')
        self.win.requestProperties( props )
        menu = Menu(self)
        menu.create_main_menu()
        #solarsystem = Solarsystem(self)

app = Solaris()
app.run()