from panda3d.core import Vec3, Point3
from direct.task import Task

from math import cos, sin, pi

class Planet():

    def __init__(self, app, name, model, texture=None, scale=1, distance_from_sun=0, speed_self=1, speed=1):
        self.app = app
        self.name = name
        self.model = model
        self.texture = texture
        self.scale = scale
        self.distance_from_sun = distance_from_sun
        self.speed_self = speed_self
        self.speed = speed
        self.angle = self.speed * self.app.speed
        self.rotation = self.speed * self.app.speed * self.speed_self

    def create_planet(self):
        self.planet = self.app.loader.loadModel(self.model)
        if self.texture:
            tex = self.app.loader.loadTexture(self.texture)
            self.planet.setTexture(tex, 1)
        self.root = self.app.render.attachNewNode(self.name+'_root')
        self.planet.setScale(self.scale, self.scale, self.scale)
        self.planet.setPos(self.distance_from_sun, 0, 0)
        self.planet.reparentTo(self.root)
        return self.app

    def rotate_planet(self):
        self.app.taskMgr.add(self.rotateTask, self.name+"RotateTask")

    def rotateTask(self, task):
        if self.app.animRunning:
            if self.distance_from_sun != 0:
                self.angle = self.angle + (self.speed * self.app.speed/10)
                angleRadians = self.angle * (pi / 180.0)
                self.planet.setPos(self.distance_from_sun * cos(angleRadians), (self.distance_from_sun+4) * sin(angleRadians), self.root.getZ())
            self.rotation = self.rotation + (self.speed*self.app.speed/10*self.speed_self)
            self.planet.setHpr(self.rotation, 0, 0)
        return Task.cont

    def get_planet_node(self):
        return self.planet

class Moon():
    def __init__(self, app, planet, name, model, texture=None, scale=1, distance_from_planet=1):
        self.app = app
        self.planet = planet
        self.name = name
        self.model = model
        self.texture = texture
        self.scale = scale
        self.distance_from_planet = distance_from_planet

    def create_moon(self):
        self.moon = self.app.loader.loadModel(self.model)
        if self.texture:
            tex = self.app.loader.loadTexture(self.texture)
            self.moon.setTexture(tex, 1)
        self.root = self.app.render.attachNewNode(self.name+'_root')
        self.root.reparentTo(self.planet.get_planet_node())
        self.moon.setScale(self.scale, self.scale, self.scale)
        self.moon.setPos(self.distance_from_planet, 0, 0)
        self.moon.reparentTo(self.root)
        return self.app

    def rotate_moon(self):
        self.app.taskMgr.add(self.rotateTask, self.name+"RotateTask")

    def rotateTask(self, task):
        angleDegrees = task.time * self.app.speed*8
        angleRadians = angleDegrees * (pi / 180.0)
        self.moon.setPos((self.distance_from_planet+0.3) * cos(angleRadians), (self.distance_from_planet+0.8) * sin(angleRadians), self.root.getZ())
        self.moon.setHpr(task.time*self.app.speed*16, 0, 0)
        return Task.cont

    def get_moon_node(self):
        return self.moon

class Sky():
    def __init__(self, app, model, texture=None, scale=1):
        self.app = app
        self.model = model
        self.texture = texture
        self.scale = scale

    def create_sky(self):
        self.sky = self.app.loader.loadModel(self.model)
        if self.texture:
            tex = self.app.loader.loadTexture(self.texture)
            self.sky.setTexture(tex, 1)
        self.sky.reparentTo(self.app.render)
        self.sky.setScale(self.scale, self.scale, self.scale)
        self.sky.setPos(0, 0, 0)
        return self.app
