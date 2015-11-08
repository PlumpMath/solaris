from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the sphere model.
        self.environ = self.loader.loadModel("models/sphere")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(2, 2, 2)
        self.environ.setPos(0, 0, 0)

app = MyApp()
app.run()