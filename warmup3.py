import sys
import math
import random
from typing import cast

from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from panda3d.core import NodePath, CollisionTraverser, CollisionHandlerPusher, CollisionNode, CollisionSphere
class Warmup3(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Use Panda's loader to bring the scene models in.
        loader = cast(Loader, self.loader)

        # Let Escape close the game.
        self.accept('escape', self.quit)

        # Load the player sphere and give it a collision shape.
        self.fighter: NodePath = cast(
            NodePath,
            loader.loadModel('Assets/sphere.egg')
        )
        # Attach it to the scene so it can be drawn.
        self.fighter.reparentTo(self.render)
        # Make the player stand out in red.
        self.fighter.setColorScale(1.0, 0.0, 0.0, 1.0)

        self.fighterCnode = self.fighter.attachNewNode(CollisionNode('fcnode'))
        self.fighterCnode.node().addSolid(CollisionSphere(0,0,0,1.0))

        # Keep one cube model to reuse around the scene.
        self.parent: NodePath = cast(
            NodePath,
            loader.loadModel('Assets/cube.egg')
        )
        self.parentCnode = self.parent.attachNewNode(CollisionNode('pcnode'))
        self.parentCnode.node().addSolid(CollisionSphere(0,0,0,1.8))

        # Place 100 cubes along a circle, with a little color variation.
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

        # Set a top-down camera so the whole layout is visible.
        assert self.camera is not None
            
        self.camera.setPos(0.0, 0.0, 258.0)
        self.camera.setHpr(0.0, -90.0, 0.0)

        self.disableMouse()

        self.traverser = CollisionTraverser()
        self.cTrav = self.traverser

        # Push the player away from anything its collider hits.
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.fighterCnode, self.fighter)
        self.traverser.addCollider(self.fighterCnode, self.pusher)
        # Show collision shapes while testing the scene.
        self.traverser.showCollisions(self.render)
        self.fighterCnode.show()
        self.parentCnode.show()

        # Start moving when an arrow is pressed, and stop when released.
        self.accept('arrow_left', self.negativeX, [1])
        self.accept('arrow_left-up', self.negativeX, [0])

        self.accept('arrow_right', self.positiveX, [1])
        self.accept('arrow_right-up', self.positiveX, [0])

        self.accept('arrow_up', self.positiveY, [1])
        self.accept('arrow_up-up', self.positiveY, [0])

        self.accept('arrow_down', self.negativeY, [1])
        self.accept('arrow_down-up', self.negativeY, [0])

    def negativeX(self, keydown):
        # Run the movement task only while the key is held.
        if keydown:
            self.taskMgr.add(self.moveNegativeX, 'moveNegativeX')
        else:
            self.taskMgr.remove('moveNegativeX')

    def moveNegativeX(self, task):
        # Tasks repeat each frame until they return something else.
        self.fighter.setX(self.fighter.getX() - 1)
        return task.cont

    def negativeY(self, keydown):
        # Run the movement task only while the key is held.
        if keydown:
            self.taskMgr.add(self.moveNegativeY, 'moveNegativeY')
        else:
            self.taskMgr.remove('moveNegativeY')

    def moveNegativeY(self, task):
        self.fighter.setY(self.fighter.getY() - 1)
        return task.cont

    def positiveX(self, keydown):
        # Run the movement task only while the key is held.
        if keydown:
            self.taskMgr.add(self.movePositiveX, 'movePositiveX')
        else:
            self.taskMgr.remove('movePositiveX')

    def movePositiveX(self, task):
        self.fighter.setX(self.fighter.getX() + 1)
        return task.cont

    def positiveY(self, keydown):
        # Run the movement task only while the key is held.
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

app = Warmup3()
app.run()