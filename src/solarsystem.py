from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

from universe import Planet, Moon, Sky

class Solaris(ShowBase):

    speed = 1
    animRunning = True

    def __init__(self):
        ShowBase.__init__(self)

        #self.useDrive()
        #self.camera.setPos(-40,-40,0)
        #self.enableMouse()
        self.setBackgroundColor(0, 0, 0)

        # Models laden
        self.sky = Sky(app=self, model="models/solar_sky_sphere", texture="models/stars_1k_tex.jpg", scale=100)
        self.sky.create_sky()

        self.sun = Planet(app=self, name="Sun", model="models/planet_sphere", texture="models/sun_1k_tex.jpg", scale=2, distance_from_sun=0)
        self = self.sun.create_planet()
        self.sun.rotate_planet()

        self.earth = Planet(app=self, name="Earth", model="models/planet_sphere", texture="models/earth_1k_tex.jpg", scale=1, distance_from_sun=10)
        self = self.earth.create_planet()
        self.earth.rotate_planet()

        self.moon = Moon(app=self, planet=self.earth, name="Earth Moon", model="models/planet_sphere", texture="models/moon_1k_tex.jpg", scale=0.2, distance_from_planet=2)
        self.moon.create_moon()
        self.moon.rotate_moon()

        self.mars = Planet(app=self, name="Mars", model="models/planet_sphere", texture="models/mars_1k_tex.jpg", scale=1, distance_from_sun=20)
        self = self.mars.create_planet()
        self.mars.rotate_planet()

        self.ambLight = AmbientLight("ambientlight")
        self.ambLight.setColor(Vec4(0.2, 0.1, 0.1, 1.0))
        self.ambNode = self.render.attachNewNode(self.ambLight)
        self.render.setLight(self.ambNode)

        plight = PointLight('pointlight')
        self.pointNode = self.sun.get_planet_node().attachNewNode(plight)
        self.pointNode.setPos(0, 0, 0)
        self.render.setLight(self.pointNode)

        self.render.setShaderAuto()

        # Kamera setzen
        #self.trackball.node().setPos(0,40,0)
        #self.camera.setPos(0,-40,0)
        # self.mouseLook = FirstPersonCamera(self, self.cam, self.render)

    def get_speed(self):
        return self.speed

    def get_lightnode(self):
        return self.dirNode


w = Solaris()
run()