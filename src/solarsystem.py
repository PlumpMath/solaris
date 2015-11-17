from math import pi, sin, cos

from direct.task import Task
from panda3d.core import *
from direct.gui.DirectGui import *

from universe import Sky, CelestialBody

import sys

class Solarsystem:

    speed = 0.1
    animRunning = True
    textures = True
    light = True

    suns = {
        "Sun": {"texture": "sun.jpg", "scale": 20, "speed_self": 10, "speed": 0, "pos": (0,0,0)}
    }
    planets = {
        "Mercury": {"texture": "mercury.jpg", "scale": .3, "distance": 2, "speed_self": 10, "speed": 100, "sun":"Sun"},
        "Venus": {"texture": "venus.jpg", "scale": .45, "distance": 4, "speed_self": 2, "speed": 80, "sun":"Sun"},
        "Earth": {"texture": "earth.jpg", "scale": .47, "distance": 6, "speed_self": 15, "speed": 70, "sun":"Sun"},
        "Mars": {"texture": "mars.jpg", "scale": .35, "distance": 8, "speed_self": 16, "speed": 60, "sun":"Sun"},
        "Jupiter": {"texture": "jupiter.jpg", "scale": .85, "distance": 12, "speed_self": 18, "speed": 40, "sun":"Sun"},
        "Saturn": {"texture": "saturn.jpg", "scale": .75, "distance": 14, "speed_self": 17, "speed": 30, "sun":"Sun"},
        "Uranus": {"texture": "uranus.jpg", "scale": .65, "distance": 17, "speed_self": 13, "speed": 20, "sun":"Sun"},
        "Neptune": {"texture": "neptune.jpg", "scale": .6, "distance": 20, "speed_self": 12, "speed": 10, "sun":"Sun"}
    }

    moons = {
        "Moon": {"texture": "moon.jpg", "scale": .1, "distance": 1, "speed_self": 10, "speed": 10, "planet": "Earth"}
    }

    nodes = {}
    pointNodes = {}

    def __init__(self, app, menu):
        self.app = app
        self.models_folder = self.app.models_folder
        self.textures_folder = self.app.textures_folder
        self.menu = menu
        self.app.setBackgroundColor(0, 0, 0)

        # Sky
        self.sky = Sky(app=self.app, model=self.models_folder+"solar_sky_sphere",
                       texture=self.textures_folder+"stars.jpg", scale=1000)
        self.sky.create_sky()

        # Suns
        for name, s in self.suns.items():
            sun = CelestialBody(app=self.app, solarsystem=self, name=name, model=self.models_folder+"planet_sphere",
                                texture=self.textures_folder+s['texture'], scale=s['scale'],
                                speed_self=s['speed_self'], speed=s['speed'], opt_pos=s['pos'])
            sun.create()
            sun.rotate()
            self.nodes[name] = sun

        # Planets
        for name, p in self.planets.items():
            planet = CelestialBody(app=self.app, solarsystem=self, name=name, model=self.models_folder+"planet_sphere",
                                 texture=self.textures_folder+p['texture'], scale=p['scale'], rotating_around=self.nodes[p['sun']],
                                 distance_from_rotate_center=p['distance'], speed_self=p['speed_self'], speed=p['speed'])
            planet.create()
            planet.rotate()
            self.nodes[name] = planet

        # Moons
        for name, m in self.moons.items():
            moon = CelestialBody(app=self.app, solarsystem=self, name=name, model=self.models_folder+"planet_sphere",
                                 texture=self.textures_folder+m['texture'], scale=m['scale'], rotating_around=self.nodes[m['planet']],
                                 distance_from_rotate_center=m['distance'], speed_self=m['speed_self'], speed=m['speed'])
            moon.create()
            moon.rotate()
            self.nodes[name] = moon


        # Light
        self.ambLight = AmbientLight("ambientlight")
        self.ambLight.setColor(Vec4(0.2, 0.1, 0.1, 1.0))
        self.ambNode = self.app.render.attachNewNode(self.ambLight)

        plight = PointLight('pointlight')
        for name in self.suns.keys():
            self.pointNodes[name] = self.nodes[name].get_node().attachNewNode(plight)
            self.pointNodes[name].setPos(0, 0, 0)

        self.app.render.setShaderAuto()

        self.makeLight()

        # Key Inputs
        self.app.accept("escape", self.backToMainMenu)
        self.app.accept("+", self.speed_change, ['+'])
        self.app.accept("-", self.speed_change, ['-'])
        self.app.accept("space", self.stopPlaySimulation)
        self.app.accept("t", self.toggleTextures)
        self.app.accept("l", self.toggleLight)

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

    def toggleTextures(self):
        self.textures = not self.textures
        for n in self.nodes.values():
            n.showTexture(self.textures)

    def toggleLight(self):
        self.light = not self.light
        if self.light:
            self.makeLight()
        else:
            self.removeLight()


    def makeLight(self):
        for key, value in self.nodes.items():
            sun = False
            for s in self.suns.keys():
                if key == s:
                    sun = True
            if not sun:
                try:
                    value.get_node().setLight(self.pointNodes[self.planets[key]['sun']])
                except:
                    value.get_node().setLight(self.pointNodes[self.planets[self.moons[key]['planet']]['sun']])

    def removeLight(self):
        for key, value in self.nodes.items():
            sun = False
            for s in self.suns.keys():
                if key == s:
                    sun = True
            if not sun:
                try:
                    value.get_node().clearLight(self.pointNodes[self.planets[key]['sun']])
                except:
                    value.get_node().clearLight(self.pointNodes[self.planets[self.moons[key]['planet']]['sun']])

    def destroy_solarsystem(self):
        self.app.ignoreAll()
        self.sky.destroy()
        for n in self.nodes.values():
            n.destroy()

    def backToMainMenu(self):
        self.destroy_solarsystem()
        self.menu.__init__(self.app)
        self.menu.create_main_menu()