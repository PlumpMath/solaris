from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec3

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Models laden
        self.sphere = self.loader.loadModel("models/sphere")
        self.sphere2 = self.loader.loadModel("models/sphere")
        # Models zu render reparenten
        self.sphere2root = self.render.attachNewNode('sphere2root')
        self.sphere.reparentTo(self.render)
        self.sphere2.reparentTo(self.sphere2root)
        # Scale und Position Transformationen auf Models anwenden
        self.sphere.setScale(2, 2, 2)
        self.sphere.setPos(0, 0, 0)
        self.sphere2.setScale(1, 1, 1)
        self.sphere2.setPos(10, 0, 0)
        # Kamera setzen
        self.trackball.node().setPos(0,40,0)
        # Sphere2 um Sphere rotieren lassen
        self.rotateSphere2 = self.sphere2root.hprInterval(3, Vec3(360, 0, 0))
        self.rotateSphere2.loop()

app = MyApp()
app.run()