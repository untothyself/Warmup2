import sys
import math
import random
from typing import cast

from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from panda3d.core import NodePath

class Warmup2(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # asset loader
        loader = cast(Loader, self.loader)

        # checks for escape key
        self.accept('escape', self.quit)

        # load the fighter model and position
        self.fighter: NodePath = cast(
            NodePath,
            loader.loadModel('Assets/sphere.egg')
        )
        #scene to graph
        self.fighter.reparentTo(self.render)
        # object color
        self.fighter.setColorScale(1.0, 0.0, 0.0, 1.0)

        self.parent: NodePath = cast(
            NodePath,
            loader.loadModel('Assets/cube.egg')
        )


        x = 0.0
        for i in range(100):
            theta = x
            placeholder = self.render.attachNewNode('placeholder2')

            placeholder.setPos(
                50.0 * math.cos(theta),
                50.0 * math.sin(theta),
                0.0
            )

            red = 0.6 + random.random() * 0.4
            green = 0.6 + random.random() * 0.4
            blue = 0.6 + random.random() * 0.4
            placeholder.setColorScale(red, green, blue, 1.0)

            self.parent.instanceTo(placeholder)
            x += 0.06

        assert self.camera is not None
            
        self.camera.setPos(0.0, 0.0, 258.0)
        self.camera.setHpr(0.0, -90.0, 0.0)

        self.disableMouse()       
        
        self.accept('arrow_left', self.negativeX, [1])
        self.accept('arrow_left-up', self.negativeX, [0])

        self.accept('arrow_right', self.positiveX, [1])
        self.accept('arrow_right-up', self.positiveX, [0])

        self.accept('arrow_up', self.positiveY, [1])
        self.accept('arrow_up-up', self.positiveY, [0])

        self.accept('arrow_down', self.negativeY, [1])
        self.accept('arrow_down-up', self.negativeY, [0])

    def negativeX(self, keydown):
        if keydown:
            self.taskMgr.add(self.moveNegativeX, 'moveNegativeX')
        else:
            self.taskMgr.remove('moveNegativeX')

    def moveNegativeX(self, task):
        self.fighter.setX(self.fighter.getX() - 1)
        return task.cont

    def negativeY(self, keydown):
        if keydown:
            self.taskMgr.add(self.moveNegativeY, 'moveNegativeY')
        else:
            self.taskMgr.remove('moveNegativeY')

    def moveNegativeY(self, task):
        self.fighter.setY(self.fighter.getY() - 1)
        return task.cont

    def positiveX(self, keydown):
        if keydown:
            self.taskMgr.add(self.movePositiveX, 'movePositiveX')
        else:
            self.taskMgr.remove('movePositiveX')

    def movePositiveX(self, task):
        self.fighter.setX(self.fighter.getX() + 1)
        return task.cont

    def positiveY(self, keydown):
        if keydown:
            self.taskMgr.add(self.movePositiveY, 'movePositiveY')
        else:
            self.taskMgr.remove('movePositiveY')

    def movePositiveY(self, task):
        self.fighter.setY(self.fighter.getY() + 1)
        return task.cont

    def quit(self):
        # exits the app
        sys.exit()

app = Warmup2()
app.run()