from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

from universe import Planet, Moon, Sky

import sys

class Solaris(ShowBase):

    speed = 0.1
    animRunning = True

    def __init__(self):
        ShowBase.__init__(self)

        #self.useDrive()
        #self.camera.setPos(-40,-40,0)
        #self.enableMouse()
        self.setBackgroundColor(0, 0, 0)

        # Models laden
        self.sky = Sky(app=self, model="models/solar_sky_sphere", texture="models/stars.jpg", scale=1000)
        self.sky.create_sky()

        self.sun = Planet(app=self, name="Sun", model="models/planet_sphere", texture="models/sun.jpg", scale=20, distance_from_sun=0, speed_self=10)
        self = self.sun.create_planet()
        self.sun.rotate_planet()

        self.mercury = Planet(app=self, name="Mercury", model="models/planet_sphere", texture="models/mercury.jpg", scale=1.6, distance_from_sun=30, speed_self=10, speed=100)
        self = self.mercury.create_planet()
        self.mercury.rotate_planet()

        self.venus = Planet(app=self, name="Venus", model="models/planet_sphere", texture="models/venus.jpg", scale=2.7, distance_from_sun=40, speed_self=2, speed=80)
        self = self.venus.create_planet()
        self.venus.rotate_planet()

        self.earth = Planet(app=self, name="Earth", model="models/planet_sphere", texture="models/earth.jpg", scale=2.8, distance_from_sun=50, speed_self=15, speed=70)
        self = self.earth.create_planet()
        self.earth.rotate_planet()

        self.moon = Moon(app=self, planet=self.earth, name="Earth Moon", model="models/planet_sphere", texture="models/moon.jpg", scale=0.1, distance_from_planet=1)
        self.moon.create_moon()
        self.moon.rotate_moon()

        self.mars = Planet(app=self, name="Mars", model="models/planet_sphere", texture="models/mars.jpg", scale=1.9, distance_from_sun=57, speed_self=16, speed=60)
        self = self.mars.create_planet()
        self.mars.rotate_planet()

        self.jupiter = Planet(app=self, name="Jupiter", model="models/planet_sphere", texture="models/jupiter.jpg", scale=12, distance_from_sun=85, speed_self=18, speed=40)
        self = self.jupiter.create_planet()
        self.jupiter.rotate_planet()

        self.saturn = Planet(app=self, name="Saturn", model="models/planet_sphere", texture="models/saturn.jpg", scale=10, distance_from_sun=115, speed_self=17, speed=30)
        self = self.saturn.create_planet()
        self.saturn.rotate_planet()

        self.uranus = Planet(app=self, name="Uranus", model="models/planet_sphere", texture="models/uranus.jpg", scale=6.7, distance_from_sun=145, speed_self=13, speed=20)
        self = self.uranus.create_planet()
        self.uranus.rotate_planet()

        self.neptune = Planet(app=self, name="Neptune", model="models/planet_sphere", texture="models/neptune.jpg", scale=6.5, distance_from_sun=185, speed_self=12, speed=10)
        self = self.neptune.create_planet()
        self.neptune.rotate_planet()

        self.ambLight = AmbientLight("ambientlight")
        self.ambLight.setColor(Vec4(0.2, 0.1, 0.1, 1.0))
        self.ambNode = self.render.attachNewNode(self.ambLight)
        self.mercury.get_planet_node().setLight(self.ambNode)
        self.venus.get_planet_node().setLight(self.ambNode)
        self.earth.get_planet_node().setLight(self.ambNode)
        self.moon.get_moon_node().setLight(self.ambNode)
        self.mars.get_planet_node().setLight(self.ambNode)
        self.jupiter.get_planet_node().setLight(self.ambNode)
        self.saturn.get_planet_node().setLight(self.ambNode)
        self.uranus.get_planet_node().setLight(self.ambNode)
        self.neptune.get_planet_node().setLight(self.ambNode)

        plight = PointLight('pointlight')
        self.pointNode = self.sun.get_planet_node().attachNewNode(plight)
        self.pointNode.setPos(0, 0, 0)
        self.mercury.get_planet_node().setLight(self.pointNode)
        self.venus.get_planet_node().setLight(self.pointNode)
        self.earth.get_planet_node().setLight(self.pointNode)
        self.moon.get_moon_node().setLight(self.pointNode)
        self.mars.get_planet_node().setLight(self.pointNode)
        self.jupiter.get_planet_node().setLight(self.pointNode)
        self.saturn.get_planet_node().setLight(self.pointNode)
        self.uranus.get_planet_node().setLight(self.pointNode)
        self.neptune.get_planet_node().setLight(self.pointNode)

        self.render.setShaderAuto()

        self.accept("escape", sys.exit)
        self.accept("+", self.speed_change, ['+'])
        self.accept("-", self.speed_change, ['-'])
        self.accept("space", self.stopPlaySimulation)

        # Kamera setzen
        #self.trackball.node().setPos(0,40,0)
        #self.camera.setPos(0,-40,0)
        # self.mouseLook = FirstPersonCamera(self, self.cam, self.render)

    def speed_change(self,plus_minus):
        if plus_minus == '+' and self.speed < 1:
            self.speed += 0.1
        elif plus_minus == '-' and self.speed > 0.1:
            self.speed -= 0.1

    def stopPlaySimulation(self):
        self.animRunning = not self.animRunning

    def get_lightnode(self):
        return self.dirNode


w = Solaris()
run()