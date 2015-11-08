from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec3

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the sphere model.
        self.sphere = self.loader.loadModel("models/sphere")
        self.sphere2 = self.loader.loadModel("models/purplesphere")
        # Reparent the model to render.
        self.sphere2root = self.render.attachNewNode('sphere2root')
        self.sphere.reparentTo(self.render)
        self.sphere2.reparentTo(self.sphere2root)
        # Apply scale and position transforms on the model.
        self.sphere.setScale(2, 2, 2)
        self.sphere.setPos(0, 0, 0)
        self.sphere2.setScale(1, 1, 1)
        self.sphere2.setPos(10, 0, 0)
        self.trackball.node().setPos(0,40,0)

        self.rotateSphere2 = self.sphere2root.hprInterval((0.241 * 10), Vec3(360, 0, 0))
        self.rotateSphere2.loop()

app = MyApp()
app.run()