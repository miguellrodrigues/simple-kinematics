import numpy as np

from lib.frame import Frame, FrameDrawer

zero = Frame(0, 0, 0)
f1 = Frame(1, 1, 0)
f2 = Frame(3, 3, 0)

f2.rotate_around_arbitrary_vector(1.57, [0, 1, 0])


def update():
  f1.translate_to(f2)

  r = np.abs(f1.rotation_to(f2))
  f1.rotate(r[0]*.01, r[1]*.01, r[2]*.01)


drawer = FrameDrawer([zero, f1, f2], update)
drawer.show()
