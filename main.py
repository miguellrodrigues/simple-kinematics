from math import radians

from lib.frame import Frame, FrameDrawer

zero = Frame(0, 0, 0)

f1 = Frame(0, 0, 0)


def update():
  zero.rotate(0, 0, radians(1))
  

drawer = FrameDrawer([zero, f1], update)
drawer.show()
