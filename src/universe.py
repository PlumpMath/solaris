from panda3d.core import Vec3, Point3
from direct.task import Task

from math import cos, sin, pi

class CelestialBody():

    def __init__(self, app, solarsystem, name, model, texture=None, scale=1, rotating_around=None,
                 distance_from_rotate_center=0, speed_self=0, speed=0, opt_pos=None):
        self.app = app
        self.solarsystem = solarsystem
        self.name = name
        self.model = model
        self.texture = texture
        self.scale = scale
        self.rotating_around = rotating_around
        self.distance_from_rotate_center = distance_from_rotate_center
        self.speed_self = speed_self
        self.speed = speed
        self.opt_pos = opt_pos
        self.angle = self.speed * self.solarsystem.speed
        self.rotation = self.speed * self.solarsystem.speed * self.speed_self

    def create(self):
        self.celestial_body = self.app.loader.loadModel(self.model)
        if self.texture is not None:
            tex = self.app.loader.loadTexture(self.texture)
            self.celestial_body.setTexture(tex, 1)
        self.root = self.app.render.attachNewNode(self.name+'_root')
        if self.rotating_around is not None:
            self.root.reparentTo(self.rotating_around.get_node())
        self.celestial_body.setScale(self.scale, self.scale, self.scale)
        if self.opt_pos is not None:
            self.celestial_body.setPos(self.opt_pos[0], self.opt_pos[1], self.opt_pos[2])
        else:
            self.celestial_body.setPos(self.distance_from_rotate_center, 0, 0)
        self.celestial_body.reparentTo(self.root)
        return self.app

    def rotate(self):
        self.app.taskMgr.add(self.rotate_task, self.name+"_RotateTask")

    def rotate_task(self, task):
        if self.solarsystem.animRunning:
            if self.speed != 0:
                self.angle = self.angle + (self.speed * self.solarsystem.speed/10)
                angleRadians = self.angle * (pi / 180.0)
                self.celestial_body.setPos(self.distance_from_rotate_center * cos(angleRadians), (self.distance_from_rotate_center+2) * sin(angleRadians), self.root.getZ())
            if self.speed_self != 0:
                self.rotation = self.rotation + (self.speed*self.solarsystem.speed/10*self.speed_self)
                self.celestial_body.setHpr(self.rotation, 0, 0)
        return Task.cont

    def get_node(self):
        return self.celestial_body

    def showTexture(self, bool):
        if bool:
            self.celestial_body.setTextureOff(1)
            tex = self.app.loader.loadTexture(self.texture)
            self.celestial_body.setTexture(tex, 1)
        else:
            self.celestial_body.setTextureOff(1)

    def destroy(self):
        self.app.ignoreAll()
        self.app.taskMgr.remove(self.name+'_RotateTask')
        self.celestial_body.remove()


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

    def destroy(self):
        self.app.ignoreAll()
        self.sky.remove()
